from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from theultimaterag.core.container import rag_engine
from theultimaterag.utils.Response_Helper import make_response
from theultimaterag.utils.Response_Helper_Model import HTTPStatusCode, APICode

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: Optional[str] = Form(None),
    access_level: str = Form("private") # private or common
):
    """
    Upload a file, split it, and ingest into the vector store.
    """
    tmp_path = f"tmp/{file.filename}"
    os.makedirs("tmp", exist_ok=True)
    
    try:
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ingest
        num_docs = rag_engine.ingest_file(tmp_path, user_id=user_id, access_level=access_level)
        
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message=f"Successfully ingested {num_docs} chunks from {file.filename}",
            data={"filename": file.filename, "chunks": num_docs}
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Ingestion failed",
            error=str(e)
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
