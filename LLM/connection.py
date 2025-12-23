from langchain_openai import ChatOpenAI
from config.settings import settings

def get_llm():
    return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )