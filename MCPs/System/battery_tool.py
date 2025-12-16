import psutil
from langchain_core.tools import tool

@tool
def battery_mcp():
    """Returns battery status including percentage and plugged-in state."""
    if not hasattr(psutil, "sensors_battery"):
        return {"battery": "Not available (platform not supported)"}

    battery = psutil.sensors_battery()
    if not battery:
        return {"battery": "Not available"}

    return {
        "battery_percent": battery.percent,
        "plugged_in": battery.power_plugged,
        "time_left_secs": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
    }