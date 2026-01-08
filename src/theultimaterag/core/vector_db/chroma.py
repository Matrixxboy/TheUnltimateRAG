from typing import List, Optional, Any
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from theultimaterag.config.settings import settings
import chromadb
from chromadb.config import Settings as ChromaSettings
from .base import VectorDBBase
from sklearn.decomposition import PCA
import numpy as np
from theultimaterag.LLM.embeddings import get_embedding_model

class CustomChromaRetriever(BaseRetriever):
    vector_manager: Any
    search_kwargs: dict = {}

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return self.vector_manager.similarity_search(query, **self.search_kwargs)

class ChromaVectorDB(VectorDBBase):
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH or "./chroma_db_data")
        self.embeddings = get_embedding_model()
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME or "rag_collection",
            metadata={"hnsw:space": "cosine"} # OpenAI embeddings are normalized
        )

    def add_documents(self, documents: List[Document], user_id: Optional[str] = None, access_level: str = "private"):
        if not documents:
            return
        
        ids = [str(i) for i in range(len(documents))] # TODO: Use better IDs
        documents_content = [doc.page_content for doc in documents]
        
        # Prepare metadata
        metadatas = []
        for doc in documents:
            m = doc.metadata.copy()
            if access_level == "private":
                if not user_id:
                    raise ValueError("User ID must be provided for private documents.")
                m["user_id"] = user_id
            m["access_level"] = access_level
            metadatas.append(m)
            
        # Embeddings are handled by Chroma if we don't provide them, OR we can provide them.
        # VectorManager uses OpenAIEmbeddings explicitly.
        embeddings = self.embeddings.embed_documents(documents_content)
        
        self.collection.add(
            ids=ids, # Chroma needs unique IDs. This is weak. Should use UUIDs or doc IDs.
            documents=documents_content,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def similarity_search(self, query: str, k: int = 4, filter: Optional[dict] = None) -> List[Document]:
        query_embedding = self.embeddings.embed_query(query)
        
        # Convert filter to Chroma format if possible
        # Chroma supports simple "where" dict.
        # Our filter format: {$or: [...], key: value}
        # Chroma: {key: value} or {$or: [{key: val}, ...]}
        # We need to adapt _build_filter_clause logic to Chroma dict
        
        chroma_filter = {}
        if filter:
            # Simplified translation
            if "$or" in filter:
                chroma_filter["$or"] = filter["$or"]
            
            for key, value in filter.items():
                if key != "$or":
                    chroma_filter[key] = value
                    
        if not chroma_filter:
            chroma_filter = None

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=chroma_filter
        )
        
        docs = []
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                content = results["documents"][0][i]
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                docs.append(Document(page_content=content, metadata=metadata))
                
        return docs

    def get_retriever(self, search_kwargs: Optional[dict] = None):
        return CustomChromaRetriever(vector_manager=self, search_kwargs=search_kwargs or {})

    def search_with_embeddings(self, query: str, user_id: str = None, k: int = 10) -> dict:
        # Chroma query includes embeddings if include=['embeddings']
        query_embedding = self.embeddings.embed_query(query)
        
        where = None
        if user_id:
             where = {"$or": [{"user_id": user_id}, {"access_level": "common"}]}
        else:
             where = {"access_level": "common"}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "embeddings"]
        )
        
        if not results["embeddings"]:
             return {"query_point": [0,0,0], "points": []} 
             
        retrieved_embeddings = results["embeddings"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        all_vectors = [query_embedding] + retrieved_embeddings
        
        # PCA
        pca = PCA(n_components=3)
        if len(all_vectors) >= 3:
             reduced_vectors = pca.fit_transform(np.array(all_vectors)).tolist()
        else:
             reduced_vectors = all_vectors # Fallback

        query_point = {
            "x": reduced_vectors[0][0], "y": reduced_vectors[0][1], "z": reduced_vectors[0][2] if len(reduced_vectors[0]) > 2 else 0,
            "type": "query", "text": query
        }
        
        doc_points = []
        for i, (vec, doc_text, meta) in enumerate(zip(reduced_vectors[1:], documents, metadatas)):
            doc_points.append({
                "x": vec[0], "y": vec[1], "z": vec[2] if len(vec) > 2 else 0,
                "type": "doc",
                "text": doc_text[:100] + "...",
                "metadata": meta
            })
            
        return {"query_point": query_point, "points": doc_points}
