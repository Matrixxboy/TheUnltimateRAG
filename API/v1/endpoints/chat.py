from fastapi import APIRouter
from pydantic import BaseModel
from utils.Response_Helper import make_response
from utils.Response_Helper_Model import HTTPStatusCode, APICode
from core.rag_engine import RAGPipeline

router = APIRouter()
rag_engine = RAGPipeline()

from typing import Optional

class ChatRequest(BaseModel):
    query: str
    session_id: str
    user_id: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat with the RAG system using a session ID for memory context.
    """
    try:
        model_params = {
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }
        
        # Remove None values
        model_params = {k: v for k, v in model_params.items() if v is not None}
        
        response_data = rag_engine.query(
            session_id=request.session_id, 
            query_text=request.query, 
            system_prompt=request.system_prompt,
            user_id=request.user_id,
            model_params=model_params
        )
        
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message="Success",
            data={
                "answer": response_data["content"],
                "session_id": request.session_id,
                "metadata": {
                    "usage": response_data["usage_metadata"],
                    "params": response_data["params"]
                }
            }
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Failed to process chat request",
            error=str(e)
        )
