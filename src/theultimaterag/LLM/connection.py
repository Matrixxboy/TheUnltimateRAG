from langchain_core.language_models import BaseChatModel
from theultimaterag.config.settings import settings

def get_llm() -> BaseChatModel:
    """
    Factory to get the Chat Model based on configuration.
    """
    provider = settings.LLM_PROVIDER
    
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=0.7
        )
        
    elif provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.MODEL_NAME,
            temperature=0.7
        )
        
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model_name=settings.MODEL_NAME,
            temperature=0.7
            # api_key is read from env ANTHROPIC_API_KEY automatically usually
        )
        
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
