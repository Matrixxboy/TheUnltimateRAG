from abc import ABC, abstractmethod
from typing import List, Optional, Any
from langchain_core.documents import Document

class VectorDBBase(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document], user_id: Optional[str] = None, access_level: str = "private"):
        """Add documents to the vector store."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4, filter: Optional[dict] = None) -> List[Document]:
        """Search for similar documents."""
        pass

    @abstractmethod
    def search_with_embeddings(self, query: str, user_id: str = None, k: int = 10) -> dict:
        """Search and return documents with embeddings for visualization."""
        pass
    
    @abstractmethod
    def get_retriever(self, search_kwargs: Optional[dict] = None):
        """Get LangChain retriever."""
        pass
