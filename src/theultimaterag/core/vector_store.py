from typing import List, Optional, Any
from langchain_core.documents import Document
from theultimaterag.config.settings import settings
from .vector_db.base import VectorDBBase
from .vector_db.postgres import PostgresVectorDB
from .vector_db.chroma import ChromaVectorDB

class VectorManager:
    def __init__(self):
        db_type = settings.VECTOR_DB_TYPE.lower()
        self.db: VectorDBBase
        
        if db_type == "postgres":
            self.db = PostgresVectorDB()
        elif db_type == "chroma":
            self.db = ChromaVectorDB()
        else:
            raise ValueError(f"Unsupported VECTOR_DB_TYPE: {db_type}")

    def add_documents(self, documents: List[Document], user_id: Optional[str] = None, access_level: str = "private"):
        return self.db.add_documents(documents, user_id, access_level)

    def similarity_search(self, query: str, k: int = 4, filter: Optional[dict] = None) -> List[Document]:
        return self.db.similarity_search(query, k, filter)

    def get_retriever(self, search_kwargs: Optional[dict] = None):
        return self.db.get_retriever(search_kwargs)

    def search_with_embeddings(self, query: str, user_id: str = None, k: int = 10) -> dict:
        return self.db.search_with_embeddings(query, user_id, k)
