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

        # Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}\n\nContext:\n{context}")
        ])

        # Retriever runnable
        retriever = self.vector_manager.get_retriever()

        def retrieve(inputs):
            docs = retriever.invoke(inputs["question"])
            context = "\n\n".join(d.page_content for d in docs)
            return {**inputs, "context": context}

        # Build RAG pipeline manually
        self.rag_chain = (
            RunnablePassthrough()
            | RunnableLambda(retrieve)
            | self.prompt
            | self.llm
        )

        # Add memory
        self.rag_with_memory = RunnableWithMessageHistory(
            self.rag_chain,
            self._get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

    def _get_session_history(self, session_id: str):
        return self.memory_manager.get_session_memory(session_id)

    def ingest_file(self, file_path: str):
        from core.ingestion import IngestionManager
        ingester = IngestionManager()
        docs = ingester.process_and_split(file_path)
        self.vector_manager.add_documents(docs)
        return len(docs)

    def query(self, session_id: str, query_text: str) -> str:
        response = self.rag_with_memory.invoke(
            {
                "question": query_text,
                "llm_persona": SYSTEM_PROMPT,
            },
            config={"configurable": {"session_id": session_id}},
        )
        return response.content
