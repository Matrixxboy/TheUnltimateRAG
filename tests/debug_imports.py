print("Starting imports...")
try:
    print("Importing psutil...")
    import psutil
    print("Success.")
except ImportError as e:
    print(f"Failed: {e}")

try:
    print("Importing langchain_core...")
    import langchain_core
    from langchain_core.tools import tool
    print("Success.")
except ImportError as e:
    print(f"Failed: {e}")

try:
    print("Importing textblob...")
    from textblob import TextBlob
    print("Success.")
    print("Testing TextBlob polarity...")
    print(TextBlob("test").sentiment.polarity)
    print("Success.")
except Exception as e:
    print(f"Failed: {e}")

print("Done.")
