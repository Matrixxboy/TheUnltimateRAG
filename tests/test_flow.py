import sys
sys.path.append(".")
import os
import asyncio
from core.rag_engine import RAGPipeline

# Create a dummy file for testing
def create_dummy_pdf():
    with open("test_doc.txt", "w", encoding="utf-8") as f:
        f.write("The Ultimate RAG system is designed to be a boilerplate for future applications.\nIt supports short-term and long-term memory.\nEfficiency is key.")
    return "test_doc.txt"

async def test_workflow():
    print("--- Starting RAG Workflow Test ---")
    
    # 1. Setup
    rag = RAGPipeline()
    file_path = create_dummy_pdf()
    session_id = "test_session_123"
    
    try:
        # 2. Ingestion
        print(f"Ingesting {file_path}...")
        count = rag.ingest_file(file_path)
        print(f"Ingested {count} chunks.")
        
        # 3. Query (No Context) - Should ideally fail or struggle, but RAG retrieves.
        print("\nQuery 1: What is the Ultimate RAG system designed for?")
        ans1 = rag.query(session_id, "What is the Ultimate RAG system designed for?")
        print(f"Answer 1: {ans1}")
        
        # 4. Memory Test
        print("\nQuery 2: Does it support memory? (Asking based on context)")
        ans2 = rag.query(session_id, "Does it support memory?")
        print(f"Answer 2: {ans2}")
        
        # 5. History Check
        print("\nChecking Memory...")
        history = rag.memory_manager.get_history(session_id)
        print(f"History length: {len(history)} messages")
        for msg in history:
            print(f"- {msg.type}: {msg.content[:50]}...")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    
    print("\n--- Test Finished ---")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set. Test might fail if not reading from .env correctly or if key is missing.")
    asyncio.run(test_workflow())
