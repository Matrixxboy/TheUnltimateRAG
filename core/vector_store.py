from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config.settings import settings
import chromadb

class VectorManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection_name = settings.COLLECTION_NAME
        
        self.vector_store = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
        )

    def add_documents(self, documents: List[Document], user_id: Optional[str] = None, access_level: str = "private"):
        """
        Add a list of documents to the vector store.
        """
        if not documents:
            return
        
        # Add metadata
        for doc in documents:
            if access_level == "private" and not user_id:
                raise ValueError("User ID must be provided for private documents.")
                
            if user_id:
                doc.metadata["user_id"] = user_id
            doc.metadata["access_level"] = access_level
        
        self.vector_store.add_documents(documents)
        # self.vector_store.persist()

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform a similarity search on the vector store.
        """
        return self.vector_store.similarity_search(query, k=k)

    def get_retriever(self, search_kwargs: Optional[dict] = None):
        """
        Get the retriever interface for LangChain chains.
        """
        _kwargs = {"k": 4}
        if search_kwargs:
            _kwargs.update(search_kwargs)
            
        return self.vector_store.as_retriever(search_kwargs=_kwargs)
