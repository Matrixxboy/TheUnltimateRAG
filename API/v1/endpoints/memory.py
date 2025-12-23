from fastapi import APIRouter
from utils.Response_Helper import make_response
from utils.Response_Helper_Model import HTTPStatusCode, APICode
from core.rag_engine import RAGPipeline

router = APIRouter()
rag_engine = RAGPipeline()

@router.delete("/memory/{session_id}")
async def clear_memory(session_id: str):
    """
    Clear the chat history for a specific session.
    """
    try:
        rag_engine.memory_manager.clear_memory(session_id)
        
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message=f"Memory cleared for session {session_id}"
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Failed to clear memory",
            error=str(e)
        )

@router.get("/memory/{session_id}")
async def get_history(session_id: str):
    """
    Retrieve chat history for a session.
    """
    try:
        history = rag_engine.memory_manager.get_history(session_id)
        # Serialize history messages if needed, but return_messages=True gives BaseMessage objects.
        # We need to convert to string or dict for JSON response
        formatted_history = []
        for msg in history:
            # Check if msg is a LangChain Message object and convert to dict
            content = msg.content if hasattr(msg, "content") else str(msg)
            msg_type = msg.type if hasattr(msg, "type") else "unknown"
            
            formatted_history.append({
                "type": msg_type,
                "content": content,
                "data": msg.dict() if hasattr(msg, "dict") else {}
            })
            
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message="Success",
            data={"history": formatted_history}
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Failed to retrieve memory",
            error=str(e)
        )
