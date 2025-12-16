from MCPs import *
import sys

def test_tool(name, tool_func, kwargs=None):
    if kwargs is None:
        kwargs = {}
    print(f"\n--- Testing {name} ---")
    try:
        result = tool_func.invoke(kwargs)
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def main():
    print("Running MCP Test Suite...")
    
    # System
    test_tool("Time", time_mcp)
    test_tool("Battery", battery_mcp)
    test_tool("System", system_mcp)
    test_tool("Device", device_mcp)
    
    # Network
    test_tool("Network", network_mcp)
    test_tool("IP", ip_mcp)
    test_tool("Location", location_mcp)
    
    # User
    test_tool("User", user_mcp)
    test_tool("Active App", active_app_mcp)
    
    # Agent
    test_tool("Conversation", conversation_mcp, {"history_str": "User: Hello\nAssistant: Hi there!"})
    test_tool("Sentiment", sentiment_mcp, {"text": "I love this project, it is amazing!"})
    test_tool("Memory", memory_mcp, {"recent_memories": "checking functionality"})
    
    # Security
    test_tool("Permission", permission_mcp, {"action": "read"})
    test_tool("Rate Limit", rate_limit_mcp)
    
    # Productivity
    test_tool("Task", task_mcp, {"current_task": "Running tests"})
    test_tool("Calendar", calendar_mcp)
    
    # Aggregator
    print("\n--- Testing Aggregator ---")
    try:
        context = collect_mcp_context()
        print(f"Aggregated Context Keys: {list(context.keys())}")
        print(f"Sample (Time): {context.get('time')}")
    except Exception as e:
        print(f"Aggregator FAILED: {e}")

if __name__ == "__main__":
    main()
