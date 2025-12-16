import socket
import requests
from langchain_core.tools import tool

@tool
def network_mcp():
    """Checks internet connectivity by attempting to reach a public DNS."""
    try:
        # Connect to Google's public DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return {"internet": "connected"}
    except OSError:
        return {"internet": "disconnected"}

@tool
def ip_mcp():
    """Returns the local IP address of the machine."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return {"hostname": hostname, "local_ip": local_ip}
    except Exception as e:
        return {"error": str(e)}

@tool
def location_mcp():
    """Returns location information. Currently returns static/default values."""
    # In a real scenario, this could use an IP geolocation API
    # But for offline safety/simplicity as requested:
    return {
        "country": "India",
        "timezone": "Asia/Kolkata",
        "note": "Static location (offline-safe)"
    }