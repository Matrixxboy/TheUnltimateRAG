import sys
sys.path.append(".")
import os
import asyncio
from core.rag_engine import RAGPipeline

async def test_advanced_workflow():
    print("--- Starting Advanced RAG Test ---")
    
    rag = RAGPipeline()
    user_a = "user_A"
    user_b = "user_B"
    session_id = "adv_test_session"
    
    # Create dummy files
    file_a = "doc_user_A.txt"
    file_b = "doc_user_B.txt"
    
    with open(file_a, "w") as f: f.write("User A's secret code is 1234.")
    with open(file_b, "w") as f: f.write("User B's secret code is 9999.")
    
    try:
        # 1. Ingest with Isolation
        print(f"Ingesting for {user_a}...")
        rag.ingest_file(file_a, user_id=user_a)
        
        print(f"Ingesting for {user_b}...")
        rag.ingest_file(file_b, user_id=user_b)
        
        # 2. Query User A (Should find A's doc)
        print(f"\nQuerying as {user_a}...")
        res_a = rag.query(session_id, "What is the secret code?", user_id=user_a, model_params={"temperature": 0.1})
        print(f"User A Result: {res_a['content']}")
        print(f"Metadata: {res_a['usage_metadata']}")
        
        # 3. Query User B (Should find B's doc, NOT A's)
        print(f"\nQuerying as {user_b}...")
        res_b = rag.query(session_id, "What is the secret code?", user_id=user_b, model_params={"temperature": 0.9})
        print(f"User B Result: {res_b['content']}")
        
        # 4. Cross Access Check (User B tries to find User A's data - purely by context)
        # Ideally RAG should not retrieve A's doc.
        
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if os.path.exists(file_a): os.remove(file_a)
        if os.path.exists(file_b): os.remove(file_b)
    
    print("\n--- Test Finished ---")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set.")
    asyncio.run(test_advanced_workflow())
