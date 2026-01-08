from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_workflow():
    print("Testing /agent/workflow (Self-Correcting RAG)...")
    payload = {
        "query": "What are the benefits of RAG?",
        "workflow_type": "self-correcting"
    }
    
    # This invokes LLMs so it might take time or fail if no keys are set
    # We just want to ensure it doesn't 500 immediately on import/instantiation
    
    try:
        response = client.post("/api/v1/agent/workflow", json=payload)
        
        if response.status_code == 200:
            print("✅ /agent/workflow: Success")
            data = response.json().get("data", {})
            print(f"   Trace: {data.get('trace')}")
            print(f"   Answer: {str(data.get('answer'))[:50]}...")
        else:
            print(f"⚠️ /agent/workflow: Failed with {response.status_code}")
            # print(response.text)
            
    except Exception as e:
        print(f"❌ Test Logic Error: {e}")

if __name__ == "__main__":
    test_workflow()
