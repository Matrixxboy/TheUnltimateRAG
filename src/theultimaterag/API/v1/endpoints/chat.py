from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from theultimaterag.core.container import rag_engine
from theultimaterag.utils.Response_Helper import make_response
from theultimaterag.utils.Response_Helper_Model import HTTPStatusCode, APICode

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session ID for memory context")
    query: str = Field(..., description="User question")
    user_id: Optional[str] = Field(None, description="User ID for RBAC")
    system_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    include_visualization: Optional[bool] = False
    include_sources: Optional[bool] = True

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
        
        # Pass extra flags if rag_engine supports them, or handle here.
        # Currently query() returns a dict with keys.
         
        response_data = rag_engine.query(
            session_id=request.session_id, 
            query_text=request.query, 
            system_prompt=request.system_prompt,
            user_id=request.user_id,
            model_params=model_params
        )
        
        # Optimization: Remove visualization if not requested
        if not request.include_visualization and "visualization" in response_data:
            del response_data["visualization"]
            
        data = {
            "answer": response_data["content"],
            "session_id": request.session_id,
            "metadata": {
                "usage": response_data["usage_metadata"],
                "params": response_data["params"]
            }
        }
        
        if request.include_visualization:
            data["visualization"] = response_data.get("visualization", {})
            
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message="Success",
            data=data
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Failed to process chat request",
            error=str(e)
        )
