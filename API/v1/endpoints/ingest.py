import shutil
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from utils.Response_Helper import make_response
from utils.Response_Helper_Model import HTTPStatusCode, APICode
from core.rag_engine import RAGPipeline

router = APIRouter()
rag_engine = RAGPipeline()

@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    user_id: Optional[str] = Form(None),
    access_level: str = Form("private")  # "private" or "common"
):
    """
    Upload and ingest a document (PDF or TXT) into the vector store.
    """
    # Security Validation
    if access_level == "private" and not user_id:
        return make_response(
            status=HTTPStatusCode.BAD_REQUEST,
            code=APICode.BAD_REQUEST,
            message="User ID is required for private documents.",
            error="Missing user_id"
        )

    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    
    file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        chunks_count = rag_engine.ingest_file(file_path, user_id=user_id, access_level=access_level)
        
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message=f"Successfully ingested {file.filename}",
            data={"chunks_count": chunks_count}
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Failed to ingest document",
            error=str(e)
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
