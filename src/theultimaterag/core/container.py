from theultimaterag.core.rag_engine import RAGPipeline

# Singleton instance of the RAG Pipeline
# This ensures that all API endpoints share the same memory manager instance.
rag_engine = RAGPipeline()
