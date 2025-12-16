from langchain_core.tools import tool
from textblob import TextBlob

@tool
def conversation_mcp(history_str: str):
    """
    Analyzes conversation history string to provide stats.
    Expects history to be passed as a string representation or summary.
    """
    # Note: Complex history object passing might be tricky with simple tool interface,
    # so we accept a string or checking length if it was a list (but inputs must be str/serializable usually).
    # For this implementation, we assume we receive a text chunk or we just return metadata if we can't process.
    
    return {
        "input_length": len(history_str),
        "approx_messages": history_str.count("User:") + history_str.count("Assistant:") # Rough heuristic
    }

@tool
def sentiment_mcp(text: str):
    """Analyzes the sentiment of the given text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    sentiment_label = "positive" if polarity > 0.1 else "neutral" if polarity > -0.1 else "negative"
    
    return {
        "polarity": round(polarity, 2),
        "subjectivity": round(blob.sentiment.subjectivity, 2),
        "sentiment": sentiment_label
    }

@tool
def memory_mcp(recent_memories: str):
    """
    Echoes back recent memories or parses them. 
    This is a placeholder for a more complex memory retrieval system.
    """
    # In a real agent, this would query a vector DB or list.
    return {
        "recent_memories_count": 0, # Placeholder
        "status": "ready"
    }
