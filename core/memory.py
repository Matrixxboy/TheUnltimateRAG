from typing import Dict, List, Any
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from config.settings import settings


class MemoryManager:
    def __init__(self):
        # In-memory storage for active sessions.
        # In production, replace with Redis or DB.
        self._sessions: Dict[str, InMemoryChatMessageHistory] = {}
        self.window_size = settings.MEMORY_WINDOW_SIZE

    def get_session_memory(self, session_id: str) -> InMemoryChatMessageHistory:
        """
        Get or create a memory buffer for a specific session.
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = InMemoryChatMessageHistory()
        return self._sessions[session_id]

    def _apply_window(self, memory: InMemoryChatMessageHistory):
        """
        Enforce sliding window size on messages.
        """
        if self.window_size <= 0:
            return

        messages = memory.messages
        if len(messages) > self.window_size * 2:
            # keep last N human+AI turns
            memory.messages = messages[-self.window_size * 2 :]

    def add_user_message(self, session_id: str, message: str):
        """
        Add a user message to the session memory.
        """
        memory = self.get_session_memory(session_id)
        memory.add_message(HumanMessage(content=message))
        self._apply_window(memory)

    def add_ai_message(self, session_id: str, message: str):
        """
        Add an AI message to the session memory.
        """
        memory = self.get_session_memory(session_id)
        memory.add_message(AIMessage(content=message))
        self._apply_window(memory)

    def get_history(self, session_id: str) -> List[Any]:
        """
        Retrieve chat history for a session.
        Returns messages compatible with LangChain prompts.
        """
        memory = self.get_session_memory(session_id)
        return memory.messages

    def clear_memory(self, session_id: str):
        """
        Clear memory for a specific session.
        """
        if session_id in self._sessions:
            self._sessions[session_id].clear()
