from typing import Dict, List, Any
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from theultimaterag.config.settings import settings
from theultimaterag.Database.Connection import get_db_connection
from theultimaterag.LLM.connection import get_llm
from psycopg2.extras import DictCursor
import json
from langchain_community.chat_message_histories import RedisChatMessageHistory
import redis


class MemoryManager:
    def __init__(self):
        # Redis storage for active sessions.
        self.redis_url = settings.REDIS_URL
        self.window_size = settings.MEMORY_WINDOW_SIZE
        self.threshold = settings.MEMORY_WINDOW_LIMIT # N
        self._init_db()

    def _init_db(self):
        """Initialize the long-term memory table if it doesn't exist."""
        # Only initialize DB if we are using Postgres. 
        # If using Chroma, we simply skip long-term SQL memory for now or should implement valid fallback.
        if settings.VECTOR_DB_TYPE != "postgres":
            return

        try:
            conn = get_db_connection()
            if conn:
                with conn.cursor() as cur:
                    # Note: Path might need adjustment depending on where python is run
                    # We assume running from root
                    import os
                    schema_path = "src/theultimaterag/Database/schema.sql"
                    if not os.path.exists(schema_path):
                         # Fallback for dev environment or different CWD
                         schema_path = os.path.join(os.path.dirname(__file__), "../Database/schema.sql")
                         
                    if os.path.exists(schema_path):     
                        with open(schema_path, "r") as f:
                            schema_sql = f.read().replace("{{EMBEDDING_DIMENSION}}", str(settings.EMBEDDING_DIMENSION))
                            cur.execute(schema_sql)
                        conn.commit()
                    else:
                        print(f"Warning: Schema file not found at {schema_path}")
                conn.close()
        except Exception as e:
            print(f"Warning: Failed to init DB: {e}")

    def get_session_memory(self, session_id: str) -> RedisChatMessageHistory:
        """
        Get or create a memory buffer for a specific session using Redis.
        """
        return RedisChatMessageHistory(session_id=session_id, url=self.redis_url)

    def _apply_window(self, memory: RedisChatMessageHistory):
        """
        Enforce sliding window size on messages (handled by consolidation now, but kept for safety).
        """
        # RedisChatMessageHistory doesn't strictly enforce window on add, 
        # so we rely on enforce_memory_consolidation.
        pass

    def add_user_message(self, session_id: str, message: str):
        """
        Add a user message to the session memory.
        """
        memory = self.get_session_memory(session_id)
        memory.add_message(HumanMessage(content=message))
        self._apply_window(memory)

    def add_ai_message(self, session_id: str, message: str):
        """
        Add an AI message to the session memory.
        """
        memory = self.get_session_memory(session_id)
        memory.add_message(AIMessage(content=message))
        self._apply_window(memory)

    def get_history(self, session_id: str) -> List[Any]:
        """
        Retrieve chat history for a session.
        Returns messages compatible with LangChain prompts.
        """
        memory = self.get_session_memory(session_id)
        return memory.messages

    def clear_memory(self, session_id: str):
        """
        Clear memory for a specific session.
        """
        # Clear from Redis
        memory = self.get_session_memory(session_id)
        memory.clear()
            
        # Also clear from DB if using postgres
        if settings.VECTOR_DB_TYPE == "postgres":
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        cur.execute("DELETE FROM long_term_memories WHERE session_id = %s", (session_id,))
                    conn.commit()
                    print(f"Long-term memory cleared for {session_id}")
                except Exception as e:
                    print(f"Error clearing long-term memory: {e}")
                finally:
                    conn.close()

    def enforce_memory_consolidation(self, session_id: str):
        """
        Check if short-term memory exceeds limit N. If so, summarize oldest N and archive to DB.
        """
        memory = self.get_session_memory(session_id)
        messages = memory.messages
        
        # Check against threshold N (Total messages)
        # Assuming threshold counts individual messages (Human + AI)
        if len(messages) > self.threshold:
            print(f"Consolidating memory for session {session_id} (Size > {self.threshold})...")
            
            # 1. Slice: Oldest N messages
            messages_to_archive = messages[:self.threshold]
            remaining_messages = messages[self.threshold:]
            
            # 2. Transform: LLM Summarization
            llm = get_llm()
            conversation_text = "\n".join([f"{m.type}: {m.content}" for m in messages_to_archive])
            
            # Structured Prompt for JSON output
            prompt = f"""
            Analyze the following conversation segment and provide a result in JSON format with two keys:
            1. "summary": A concise paragraph summarizing the key facts and context.
            2. "key_concepts": A list of strings representing the main entities or topics discussed.

            Conversation:
            {conversation_text}
            
            Output JSON only.
            """
            
            try:
                # Add json mode or simple parsing (OpenAI usually handles json well if asked)
                response = llm.invoke([HumanMessage(content=prompt)])
                content = response.content.strip()
                
                # Basic cleanup if markdown is included
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "")
                
                data = json.loads(content)
                summary = data.get("summary", "")
                key_concepts = data.get("key_concepts", [])
                
                if not summary:
                    summary = content # Fallback
                
                # 3. Persist to DB (Only if Postgres)
                if settings.VECTOR_DB_TYPE == "postgres":
                    conn = get_db_connection()
                    if conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                "INSERT INTO long_term_memories (session_id, summary_chunk, key_concepts) VALUES (%s, %s, %s)",
                                (session_id, summary, json.dumps(key_concepts))
                            )
                        conn.commit()
                        conn.close()
                        print("Summary and Key Concepts stored in DB.")
                    
                    print("Summary and Key Concepts stored in DB.")
                    
                    # 4. Flush & Reset: Remove the oldest N messages from Redis
                    # RedisChatMessageHistory stores messages in a LIST at key "message_store:{session_id}" (default prefix is 'message_store:')
                    # However, langchain-community's RedisChatMessageHistory might use a configurable key.
                    # Default key is just session_id or with prefix. Let's inspect or use a separate redis client connection.
                    
                    # We can use the redis client inside the memory object if exposed, or create a new one.
                    # Creating a lightweight connection here for the trim operation.
                    r_client = redis.Redis.from_url(self.redis_url)
                    redis_key = f"message_store:{session_id}" # Default langchain prefix
                    
                    # LPOP N times to remove the oldest N
                    # (Redis List: Left is Oldest, Right is Newest usually in LangChain implementation? 
                    # LangChain appends to the end (RPUSH), so index 0 is oldest. LPOP removes from left/oldest.)
                    for _ in range(self.threshold):
                        r_client.lpop(redis_key)
                        
                    print(f"Short-term memory flushed. Removed oldest {self.threshold} messages.")
                    
            except Exception as e:
                print(f"Error during memory consolidation: {e}")
