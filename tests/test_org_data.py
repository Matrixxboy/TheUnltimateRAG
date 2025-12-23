import sys
sys.path.append(".")
import os
import asyncio
from core.rag_engine import RAGPipeline

async def test_org_data_workflow():
    print("--- Starting Organizational Data Test ---")
    
    rag = RAGPipeline()
    user_a = "user_A"
    user_b = "user_B"
    session_id = "org_test_session"
    
    # Create dummy files
    file_common = "doc_common.txt"
    file_private_a = "doc_private_A.txt"
    
    with open(file_common, "w") as f: f.write("COMPANY POLICY: All employees must wear hats.")
    with open(file_private_a, "w") as f: f.write("User A's Diary: I hate hats.")
    
    try:
        # 1. Ingest Common Data
        print(f"Ingesting Common Doc...")
        rag.ingest_file(file_common, user_id=None, access_level="common")
        
        # 2. Ingest Private Data for A
        print(f"Ingesting Private Doc for A...")
        rag.ingest_file(file_private_a, user_id=user_a, access_level="private")
        
        # 3. Query User A (Should see both)
        print(f"\nQuerying as {user_a} (Expecting: Policy + Diary)...")
        res_a_policy = rag.query(session_id, "What is the company policy?", user_id=user_a)
        res_a_private = rag.query(session_id, "What is in my diary?", user_id=user_a)
        print(f"User A - Policy: {res_a_policy['content']}")
        print(f"User A - Diary: {res_a_private['content']}")
        
        # 4. Query User B (Should see Policy, but NOT A's Diary)
        print(f"\nQuerying as {user_b} (Expecting: Policy ONLY)...")
        res_b_policy = rag.query(session_id, "What is the company policy?", user_id=user_b)
        res_b_private = rag.query(session_id, "What is in User A's diary?", user_id=user_b) # Should fail or hallucinate without context
        
        print(f"User B - Policy: {res_b_policy['content']}")
        print(f"User B - Diary (Should be unknown/irrelevant): {res_b_private['content']}")
        
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if os.path.exists(file_common): os.remove(file_common)
        if os.path.exists(file_private_a): os.remove(file_private_a)
    
    print("\n--- Test Finished ---")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set.")
    asyncio.run(test_org_data_workflow())
