print("Starting targeted test...")
try:
    from MCPs.System.time_tool import time_mcp
    print("Imported time_mcp.")
    print(time_mcp.invoke({}))
    print("Success.")
except Exception as e:
    print(f"Failed: {e}")
