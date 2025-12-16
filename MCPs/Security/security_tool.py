import time
from langchain_core.tools import tool

@tool
def permission_mcp(action: str):
    """Checks if a specific action is allowed."""
    # Placeholder logic
    allowed_actions = ["read", "search", "calculate", "time", "battery"]
    is_allowed = action.lower() in allowed_actions
    return {"action": action, "allowed": is_allowed}

# Simple in-memory rate limit valid for the runtime of the process
last_call_timestamp = 0

@tool
def rate_limit_mcp():
    """Checks if the current request is within the rate limit (1 call per 2 seconds)."""
    global last_call_timestamp
    now = time.time()
    allowed = (now - last_call_timestamp) > 2

    if allowed:
        last_call_timestamp = now

    return {"rate_limit_ok": allowed, "wait_seconds": 0 if allowed else 2 - (now - last_call_timestamp)}
