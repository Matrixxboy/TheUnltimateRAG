from fastapi import APIRouter
from pydantic import BaseModel
from utils.Response_Helper import make_response
from utils.Response_Helper_Model import HTTPStatusCode, APICode
from core.rag_engine import RAGPipeline

router = APIRouter()
rag_engine = RAGPipeline()

class ChatRequest(BaseModel):
    query: str
    session_id: str

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat with the RAG system using a session ID for memory context.
    """
    try:
        response = rag_engine.query(request.session_id, request.query)
        
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message="Success",
            data={"answer": response, "session_id": request.session_id}
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Failed to process chat request",
            error=str(e)
        )
