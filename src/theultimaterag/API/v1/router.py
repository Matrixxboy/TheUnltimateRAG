from theultimaterag.API.v1.endpoints import ingest, chat, memory, agent
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(memory.router, prefix="/memory", tags=["Memory"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
