from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory

from core.vector_store import VectorManager
from core.memory import MemoryManager
from config.settings import settings
from LLM.connection import get_llm
from Prompts.SystemPrompt import SYSTEM_PROMPT

class RAGPipeline:
    def __init__(self):
        self.vector_manager = VectorManager()
        self.memory_manager = MemoryManager()
        self.llm = get_llm()

        # Retriever runnable (Default)
        # We will generate specific retrievers per query for filtering
        self.base_retriever = self.vector_manager.get_retriever()

    def _retrieve_context(self, question: str, user_id: str = None):
        # Create a dynamic retriever with filter
        # Logic: (user_id == current_user) OR (access_level == "common")
        
        filter_criteria = {}
        
        if user_id:
            filter_criteria = {
                "$or": [
                    {"user_id": user_id},
                    {"access_level": "common"}
                ]
            }
        else:
            # If no user_id, only show common data (public access)
            filter_criteria = {"access_level": "common"}
            
        retriever = self.vector_manager.get_retriever(search_kwargs={"filter": filter_criteria})
        docs = retriever.invoke(question)
        return "\n\n".join(d.page_content for d in docs)

    def _get_session_history(self, session_id: str):
        return self.memory_manager.get_session_memory(session_id)

    def ingest_file(self, file_path: str, user_id: str = None, access_level: str = "private"):
        from core.ingestion import IngestionManager
        ingester = IngestionManager()
        docs = ingester.process_and_split(file_path)
        self.vector_manager.add_documents(docs, user_id=user_id, access_level=access_level)
        return len(docs)

    def query(self, session_id: str, query_text: str, system_prompt: str = None, 
              user_id: str = None, model_params: dict = None) -> dict:
        
        # 0. Configure LLM with params
        _llm = self.llm
        if model_params:
            if "temperature" in model_params:
                _llm = _llm.bind(temperature=model_params["temperature"])
            # Add other params like max_tokens if needed by the provider
            # OpenAI supports max_tokens via bind as well usually, or we recreate the object
        
        # 1. Build Prompt dynamically
        from Prompts.manager import PromptManager
        prompt_template = PromptManager.get_chat_prompt(system_prompt)

        # 2. Define Chain
        def retrieve(inputs):
            context = self._retrieve_context(inputs["question"], user_id=user_id)
            return {**inputs, "context": context}

        rag_chain = (
            RunnablePassthrough()
            | RunnableLambda(retrieve)
            | prompt_template
            | _llm
        )

        rag_with_memory = RunnableWithMessageHistory(
            rag_chain,
            self._get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

        response = rag_with_memory.invoke(
            {"question": query_text},
            config={"configurable": {"session_id": session_id}},
        )
        
        # 3. Get Visualization Data
        # We perform a separate search to get the embeddings for visualization
        # This ensures we get the exact points in vector space
        viz_data = self.vector_manager.search_with_embeddings(
            query=query_text,
            user_id=user_id,
            k=10 # Visualize top 10
        )
        
        # 4. Check & Consolidate Memory (Fire and forget, or sync)
        # We do this after response generation to not latency the user (ideally async, but sync for now)
        try:
            self.memory_manager.enforce_memory_consolidation(session_id)
        except Exception as e:
            print(f"Memory consolidation failed: {e}")

        return {
            "content": response.content,
            "usage_metadata": response.response_metadata if hasattr(response, "response_metadata") else {},
            "params": model_params,
            "visualization": viz_data
        }

