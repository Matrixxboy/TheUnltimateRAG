from langchain_openai import ChatOpenAI
from config.settings import settings

def get_llm():
    return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=0.7
        )