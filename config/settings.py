import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "TheUltimateRAG"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    
    # Vector Store
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME")
    
    # Memory
    MEMORY_WINDOW_SIZE: int = int(os.getenv("MEMORY_WINDOW_SIZE", "10"))
    SHORT_TERM_MEMORY_LIMIT: int = int(os.getenv("SHORT_TERM_MEMORY_LIMIT", "5")) # N number of chats before consolidation

    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
