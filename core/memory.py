from typing import Dict, List, Any
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config.settings import settings
from Database.Connection import get_db_connection
from LLM.connection import get_llm
from psycopg2.extras import DictCursor


class MemoryManager:
    def __init__(self):
        # In-memory storage for active sessions.
        # In production, replace with Redis or DB.
        self._sessions: Dict[str, InMemoryChatMessageHistory] = {}
        self.window_size = settings.MEMORY_WINDOW_SIZE
        self.short_term_limit = settings.SHORT_TERM_MEMORY_LIMIT
        self._init_db()

    def _init_db(self):
        """Initialize the long-term memory table if it doesn't exist."""
        try:
            conn = get_db_connection()
            if conn:
                with conn.cursor() as cur:
                    with open("Database/schema.sql", "r") as f:
                        cur.execute(f.read())
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"Warning: Failed to init DB: {e}")

    def get_session_memory(self, session_id: str) -> InMemoryChatMessageHistory:
        """
        Get or create a memory buffer for a specific session.
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = InMemoryChatMessageHistory()
        return self._sessions[session_id]

    def _apply_window(self, memory: InMemoryChatMessageHistory):
        """
        Enforce sliding window size on messages.
        """
        if self.window_size <= 0:
            return

        messages = memory.messages
        if len(messages) > self.window_size * 2:
            # keep last N human+AI turns
            memory.messages = messages[-self.window_size * 2 :]

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
        if session_id in self._sessions:
            self._sessions[session_id].clear()

    def enforce_memory_consolidation(self, session_id: str):
        """
        Check if short-term memory exceeds limit. If so, summarize and archive to DB.
        """
        memory = self.get_session_memory(session_id)
        messages = memory.messages
        
        # Count user messages or total messages? 
        # Requirement: "n numbers of chat" -> usually pairs. 
        # If limit is 5, we wait for 5 pairs (10 messages).
        # Let's count pairs (User messages).
        user_msg_count = sum(1 for m in messages if isinstance(m, HumanMessage))

        if user_msg_count > self.short_term_limit:
            print(f"Consolidating memory for session {session_id}...")
            
            # 1. Summarize
            llm = get_llm()
            # Convert messages to string
            conversation_text = "\n".join([f"{m.type}: {m.content}" for m in messages])
            prompt = f"""
            Summarize the following conversation into a concise paragraph (word chunks/key points) 
            to be stored as long-term memory. Retain key facts and context.
            
            Conversation:
            {conversation_text}
            
            Summary:
            """
            response = llm.invoke([HumanMessage(content=prompt)])
            summary = response.content

            # 2. Store in DB
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO long_term_memories (session_id, summary_chunk) VALUES (%s, %s)",
                            (session_id, summary)
                        )
                    conn.commit()
                    print("Summary stored in DB.")
                except Exception as e:
                    print(f"Error storing summary: {e}")
                finally:
                    conn.close()

            # 3. Clear Short-Term Memory
            # We might want to keep the SYSTEM prompt if we had one, but InMemoryChatMessageHistory is usually just chat.
            # We'll clear it completely as requested ("deleted the short term memory").
            memory.clear()
            print("Short-term memory cleared.")
