from MCPs.System.time_tool import time_mcp
from MCPs.System.battery_tool import battery_mcp
from MCPs.System.system_tool import system_mcp
from MCPs.Network.network_tool import network_mcp
from MCPs.User.user_tool import user_mcp
# Note: Some MCPs require arguments (like conversation, sentiment) so they aren't auto-collected here unless defaults exist.

def collect_mcp_context():
    """
    Collects context from all parameter-less MCPs to build a context snapshot.
    Useful for injecting into system prompts.
    """
    context = {}
    
    # helper for running simple tools
    def run_tool(name, tool_func):
        try:
            # invocating tool with empty dict if it takes no args
            result = tool_func.invoke({})
            context[name] = result
        except Exception as e:
            context[name] = {"error": str(e)}

    run_tool("time", time_mcp)
    run_tool("battery", battery_mcp)
    run_tool("system", system_mcp)
    run_tool("network", network_mcp)
    run_tool("user", user_mcp)
    
    return context
