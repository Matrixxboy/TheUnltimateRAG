import os
import sys

# Mock settings for testing logic if env vars not set, but better to rely on actual loading
from theultimaterag.config.settings import settings
from theultimaterag.LLM.connection import get_llm
from theultimaterag.LLM.embeddings import get_embedding_model

def test_providers():
    print(f"Current LLM Provider: {settings.LLM_PROVIDER}")
    print(f"Current Embedding Provider: {settings.EMBEDDING_PROVIDER}")

    try:
        llm = get_llm()
        print(f"✅ LLM Factory returned: {type(llm).__name__}")
    except Exception as e:
        print(f"❌ LLM Factory failed: {e}")

    try:
        embeddings = get_embedding_model()
        print(f"✅ Embedding Factory returned: {type(embeddings).__name__}")
    except Exception as e:
        print(f"❌ Embedding Factory failed: {e}")

if __name__ == "__main__":
    test_providers()
