import psutil
from langchain_core.tools import tool

@tool
def system_mcp():
    """Returns current system CPU and Memory usage percentages."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2)
    }
