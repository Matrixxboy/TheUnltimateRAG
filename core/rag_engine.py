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
        # Create a dynamic retriever with filter if user_id is provided
        search_kwargs = {}
        if user_id:
            search_kwargs["filter"] = {"user_id": user_id}
            
        retriever = self.vector_manager.get_retriever(search_kwargs=search_kwargs)
        docs = retriever.invoke(question)
        return "\n\n".join(d.page_content for d in docs)

    def _get_session_history(self, session_id: str):
        return self.memory_manager.get_session_memory(session_id)

    def ingest_file(self, file_path: str, user_id: str = None):
        from core.ingestion import IngestionManager
        ingester = IngestionManager()
        docs = ingester.process_and_split(file_path)
        self.vector_manager.add_documents(docs, user_id=user_id)
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
        
        # Return full metadata if needed via a dict, but current signature returns str.
        # User requested "show everything the token size and temperature".
        # LangChain response object usually contains usage metadata in response_metadata.
        
        return {
            "content": response.content,
            "usage_metadata": response.response_metadata if hasattr(response, "response_metadata") else {},
            "params": model_params
        }
