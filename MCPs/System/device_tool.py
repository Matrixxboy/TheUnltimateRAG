import platform
from langchain_core.tools import tool

@tool
def device_mcp():
    """Returns information about the operating system and device architecture."""
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "node_name": platform.node()
    }
