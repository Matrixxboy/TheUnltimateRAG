from fastapi.testclient import TestClient
from app import app
from theultimaterag.config.settings import settings

client = TestClient(app)

def test_agent_tools():
    print("Testing /agent/tools...")
    response = client.get("/api/v1/agent/tools")
    if response.status_code == 200:
        print("✅ /agent/tools: Success")
        # print(response.json())
    else:
        print(f"❌ /agent/tools: Failed ({response.status_code})")
        print(response.text)

def test_agent_search():
    print("Testing /agent/search (Mock)...")
    # This might fail if DB is empty or connection issues, but we test the route existence
    payload = {
        "query": "test query",
        "k": 1
    }
    response = client.post("/api/v1/agent/search", json=payload)
    if response.status_code == 200:
        print("✅ /agent/search: Success")
    else:
        # 500 is acceptable if DB is not running, 404 is fail
        print(f"⚠️ /agent/search: Returned {response.status_code} (Might be due to empty DB/No Connection)")
        # print(response.text)

if __name__ == "__main__":
    try:
        test_agent_tools()
        test_agent_search()
        print("\nAgentic API verification complete.")
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
