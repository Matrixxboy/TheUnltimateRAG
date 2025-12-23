import sys
sys.path.append(".")
import os
import asyncio
from core.rag_engine import RAGPipeline
from config.settings import settings

async def test_security_config():
    print("--- Starting Security & Config Test ---")
    
    rag = RAGPipeline()
    
    # 1. Config Check
    print(f"Current Model Name from Settings: {settings.MODEL_NAME}")
    if rag.llm.model_name != settings.MODEL_NAME:
         print(f"FAIL: Logic uses {rag.llm.model_name}, expected {settings.MODEL_NAME}")
    else:
         print("PASS: LLM is using configured model name.")
         
    # 2. Security Check (Private Ingest without User ID)
    # Since we added validation at API layer, we test the core protection in VectorStore too if we used that tool directly.
    # But RAGPipeline.ingest_file calls VectorManager.add_documents which has our defensive check.
    
    file_path = "security_test_doc.txt"
    with open(file_path, "w") as f: f.write("Top Secret Data")
    
    print("\nAttempting Private Ingest WITHOUT User ID (Should Fail)...")
    try:
        rag.ingest_file(file_path, user_id=None, access_level="private")
        print("FAIL: Ingestion succeeded unexpectedly.")
    except ValueError as e:
        print(f"PASS: Caught expected error: {e}")
    except Exception as e:
        print(f"FAIL: Caught unexpected error: {e}")

    # 3. Security Check (Common Ingest without User ID)
    print("\nAttempting Common Ingest WITHOUT User ID (Should Pass)...")
    try:
        rag.ingest_file(file_path, user_id=None, access_level="common")
        print("PASS: Common ingestion succeeded.")
    except Exception as e:
        print(f"FAIL: Common ingestion failed: {e}")

    if os.path.exists(file_path): os.remove(file_path)
    print("\n--- Test Finished ---")

if __name__ == "__main__":
    asyncio.run(test_security_config())
