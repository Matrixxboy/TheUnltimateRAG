import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, model_validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application Settings managed by Pydantic.
    """
    # --- core ---
    APP_NAME: str = Field("TheUltimateRAG", description="Name of the application")
    APP_ENV: str = Field("development", description="Environment: development, production")
    DEBUG: bool = Field(True, description="Debug mode")
    
    # --- LLM Provider ---
    LLM_PROVIDER: str = Field("openai", description="llm provider: openai, ollama, anthropic")
    EMBEDDING_PROVIDER: str = Field("openai", description="embedding provider: openai, ollama, huggingface")
    MODEL_NAME: str = Field("gpt-3.5-turbo", description="Model name to use")
    
    # --- API Keys ---
    OPENAI_API_KEY: str | None = Field(None, description="OpenAI API Key")
    ANTHROPIC_API_KEY: str | None = Field(None, description="Anthropic API Key")
    
    # --- Ollama Config ---
    OLLAMA_BASE_URL: str = Field("http://localhost:11434", description="Ollama API URL")
    
    # --- Vector Store ---
    VECTOR_DB_TYPE: str = Field("chroma", description="Vector DB: postgres, chroma")
    VECTOR_DB_PATH: str = Field("./chroma_db_data", description="Path for local ChromaDB")
    COLLECTION_NAME: str = Field("rag_collection", description="Unused currently but reserved")
    EMBEDDING_DIMENSION: int = Field(1536, description="Dimension of embeddings")
    
    # --- Postgres (PGVector) ---
    POSTGRES_HOST: str = Field("localhost", description="DB Host")
    POSTGRES_DB: str = Field("vector_db", description="DB Name")
    POSTGRES_USER: str = Field("postgres", description="DB User")
    POSTGRES_PASSWORD: str = Field("postgres", description="DB Password")
    POSTGRES_PORT: str = Field("5432", description="DB Port")
    
    # --- Memory (Redis + Params) ---
    MEMORY_WINDOW_SIZE: int = Field(10, description="Chat history window size")
    MEMORY_WINDOW_LIMIT: int = Field(10, description="Memory window limit")
    REDIS_HOST: str = Field("localhost", description="Redis Host")
    REDIS_PORT: int = Field(6379, description="Redis Port")
    REDIS_PASSWORD: str | None = Field(None, description="Redis Password")
    REDIS_USER: str = Field("default", description="Redis User")
    REDIS_DB: str = Field("0", description="Redis DB Index")

    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL from components."""
        if self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # --- Validators ---
    
    @model_validator(mode='after')
    def validate_providers(self):
        """Ensure keys exist for selected providers."""
        # Check OpenAI
        if self.LLM_PROVIDER == 'openai' or self.EMBEDDING_PROVIDER == 'openai':
            if not self.OPENAI_API_KEY:
                # We warn instead of fail to allow import, but this is a good practice
                print("⚠️ WARNING: OpenAI Provider selected but OPENAI_API_KEY is missing.")
        
        # Check Postgres
        if self.VECTOR_DB_TYPE == 'postgres':
            # Basic check is implicit by defaults, but we could add connection checks here
            pass
            
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

settings = Settings()
