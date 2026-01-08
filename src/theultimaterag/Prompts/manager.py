from typing import Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from theultimaterag.Prompts.SystemPrompt import SYSTEM_PROMPT as DEFAULT_SYSTEM_PROMPT

class PromptManager:
    @staticmethod
    def get_chat_prompt(system_prompt: Optional[str] = None) -> ChatPromptTemplate:
        """
        Generates a ChatPromptTemplate with a dynamic system prompt.
        """
        _system_prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT
        
        return ChatPromptTemplate.from_messages([
            ("system", _system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}\n\nContext:\n{context}")
        ])
