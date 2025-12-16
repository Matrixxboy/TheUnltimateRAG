from datetime import datetime
from langchain_core.tools import tool

@tool
def time_mcp():
    """Returns the current date, time, and day of the week."""
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "day": datetime.now().strftime("%A")
    }