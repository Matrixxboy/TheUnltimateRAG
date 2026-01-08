from typing import List, Optional, Any, Tuple
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from theultimaterag.config.settings import settings
import numpy as np
from sklearn.decomposition import PCA
from theultimaterag.Database.Connection import get_db_connection
from pgvector.psycopg2 import register_vector
import json
from .base import VectorDBBase
from theultimaterag.LLM.embeddings import get_embedding_model

class CustomPostgresRetriever(BaseRetriever):
    vector_manager: Any
    search_kwargs: dict = {}

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return self.vector_manager.similarity_search(query, **self.search_kwargs)

class PostgresVectorDB(VectorDBBase):
    def __init__(self):
        self.embeddings = get_embedding_model()

    def _get_conn(self):
        conn = get_db_connection()
        if not conn:
            raise ConnectionError("Failed to connect to PostgreSQL")
        return conn

    def add_documents(self, documents: List[Document], user_id: Optional[str] = None, access_level: str = "private"):
        if not documents:
            return
        
        texts = [doc.page_content for doc in documents]
        embeddings = self.embeddings.embed_documents(texts)
        
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                for i, doc in enumerate(documents):
                    metadata = doc.metadata.copy()
                    if access_level == "private":
                        if not user_id:
                            raise ValueError("User ID must be provided for private documents.")
                        metadata["user_id"] = user_id
                    metadata["access_level"] = access_level
                    
                    cur.execute(
                        "INSERT INTO documents (content, metadata, embedding) VALUES (%s, %s, %s)",
                        (doc.page_content, json.dumps(metadata), embeddings[i])
                    )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _build_filter_clause(self, filter: Optional[dict]) -> Tuple[str, List[Any]]:
        if not filter:
            return "", []
        
        conditions = []
        params = []
        
        if "$or" in filter:
            or_conditions = []
            for sub_filter in filter["$or"]:
                for key, value in sub_filter.items():
                    or_conditions.append(f"metadata->>'{key}' = %s")
                    params.append(value)
            if or_conditions:
                conditions.append(f"({' OR '.join(or_conditions)})")
        
        for key, value in filter.items():
            if key == "$or":
                continue
            conditions.append(f"metadata->>'{key}' = %s")
            params.append(value)
            
        if not conditions:
            return "", []
            
        return " WHERE " + " AND ".join(conditions), params

    def similarity_search(self, query: str, k: int = 4, filter: Optional[dict] = None) -> List[Document]:
        query_embedding = self.embeddings.embed_query(query)
        where_clause, filter_params = self._build_filter_clause(filter)
        
        conn = self._get_conn()
        results = []
        try:
            register_vector(conn)
            with conn.cursor() as cur:
                sql = f"""
                    SELECT content, metadata, (embedding <=> %s) as distance
                    FROM documents
                    {where_clause}
                    ORDER BY distance ASC
                    LIMIT %s
                """
                params = [np.array(query_embedding)] + filter_params + [k]
                cur.execute(sql, tuple(params))
                
                rows = cur.fetchall()
                for row in rows:
                    content, metadata, distance = row
                    results.append(Document(page_content=content, metadata=metadata or {}))
        finally:
            conn.close()
            
        return results

    def get_retriever(self, search_kwargs: Optional[dict] = None):
        return CustomPostgresRetriever(vector_manager=self, search_kwargs=search_kwargs or {})

    def perform_pca(self, vectors: List[List[float]], n_components: int = 2) -> List[List[float]]:
        if len(vectors) < n_components:
            return vectors 
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(np.array(vectors))
        return reduced.tolist()

    def search_with_embeddings(self, query: str, user_id: str = None, k: int = 10) -> dict:
        query_embedding = self.embeddings.embed_query(query)
        conn = self._get_conn()
        try:
            register_vector(conn)
            with conn.cursor() as cur:
                sql = "SELECT content, metadata, embedding, (embedding <=> %s) as distance FROM documents"
                params = [np.array(query_embedding)]
                
                if user_id:
                    sql += " WHERE (metadata->>'user_id' = %s OR metadata->>'access_level' = 'common')"
                    params.append(user_id)
                else:
                    sql += " WHERE metadata->>'access_level' = 'common'"
                
                sql += " ORDER BY distance ASC LIMIT %s"
                params.append(k)
                
                cur.execute(sql, tuple(params))
                results = cur.fetchall()
                
                if not results:
                     return {"query_point": [0,0,0], "points": []} 

                documents = [r[0] for r in results]
                metadatas = [r[1] for r in results]
                retrieved_embeddings = [json.loads(r[2]) if isinstance(r[2], str) else np.array(r[2]).tolist() for r in results]
                retrieved_embeddings = [v.tolist() if hasattr(v, 'tolist') else v for v in retrieved_embeddings]

                all_vectors = [query_embedding] + retrieved_embeddings
                reduced_vectors = self.perform_pca(all_vectors, n_components=3) 
                
                query_point = {
                    "x": reduced_vectors[0][0], "y": reduced_vectors[0][1],
                    "z": reduced_vectors[0][2] if len(reduced_vectors[0]) > 2 else 0,
                    "type": "query", "text": query
                }
                
                doc_points = []
                for i, (vec, doc_text, meta) in enumerate(zip(reduced_vectors[1:], documents, metadatas)):
                    doc_points.append({
                        "x": vec[0], "y": vec[1],
                        "z": vec[2] if len(vec) > 2 else 0,
                        "type": "doc",
                        "text": doc_text[:100] + "..." if len(doc_text) > 100 else doc_text,
                        "metadata": meta or {}
                    })
                    
                return {"query_point": query_point, "points": doc_points}
        finally:
            conn.close()
