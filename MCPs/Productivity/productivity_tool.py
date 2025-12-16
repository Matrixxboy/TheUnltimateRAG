from langchain_core.tools import tool

@tool
def task_mcp(current_task: str):
    """Updates or returns information about the current task context."""
    return {"current_task": current_task, "status": "tracked"}

@tool
def calendar_mcp():
    """Returns today's calendar events."""
    # Placeholder for calendar integration (e.g. Google Calendar API)
    return {"today_events": [], "status": "no events found"}
