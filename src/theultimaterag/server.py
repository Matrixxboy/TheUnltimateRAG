from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from theultimaterag.config.settings import settings
from theultimaterag.API.v1.router import api_router
from contextlib import asynccontextmanager

def create_app() -> FastAPI:
    """
    Factory function to create the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="A Ultimate RAG system with memory and vector storage.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include Routers
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": f"Welcome to {settings.APP_NAME}"}
        
    return app

# Expose a default instance for uvicorn imports
app = create_app()

def start():
    """
    Entry point for CLI.
    """
    import uvicorn
    uvicorn.run("theultimaterag.server:app", host="0.0.0.0", port=8080, reload=True)
