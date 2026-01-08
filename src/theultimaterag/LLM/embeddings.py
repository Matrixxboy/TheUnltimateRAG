from typing import Any
from theultimaterag.config.settings import settings

def get_embedding_model() -> Any:
    """
    Factory to get the embedding model based on configuration.
    """
    provider = settings.EMBEDDING_PROVIDER
    
    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
    
    elif provider == "ollama":
        from langchain_community.embeddings import OllamaEmbeddings
        return OllamaEmbeddings(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.MODEL_NAME # Users likely use same model name var or we need a separate one
        )
    
    elif provider == "huggingface":
        # Example for local HuggingFace
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=settings.MODEL_NAME or "all-MiniLM-L6-v2")

    else:
        raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {provider}")
