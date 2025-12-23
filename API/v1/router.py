from fastapi import APIRouter
from API.v1.endpoints import ingest, chat, memory

api_router = APIRouter()

api_router.include_router(ingest.router, tags=["Ingestion"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(memory.router, tags=["Memory"])
