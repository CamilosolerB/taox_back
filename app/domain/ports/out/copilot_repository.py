"""
Puerto de repositorio para conversaciones y mensajes del copiloto
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.copilot_models import CopilotConversation, CopilotMessage


class CopilotRepository(ABC):
    """Interfaz para persistencia de conversaciones y mensajes del copiloto."""

    @abstractmethod
    def create_conversation(self, conversation: CopilotConversation) -> CopilotConversation:
        pass

    @abstractmethod
    def get_conversation(self, id_conversation: UUID, company_id: Optional[str] = None) -> Optional[CopilotConversation]:
        pass

    @abstractmethod
    def get_conversations_by_company(self, company_id: str) -> List[CopilotConversation]:
        pass

    @abstractmethod
    def get_latest_conversation_by_channel(
        self, canal: str, canal_chat_id: str
    ) -> Optional[CopilotConversation]:
        pass

    @abstractmethod
    def update_conversation(self, id_conversation: UUID, data: dict) -> Optional[CopilotConversation]:
        pass

    @abstractmethod
    def add_message(self, message: CopilotMessage) -> CopilotMessage:
        pass

    @abstractmethod
    def get_messages(self, id_conversation: UUID, company_id: Optional[str] = None) -> List[CopilotMessage]:
        pass

    @abstractmethod
    def get_recent_messages(self, id_conversation: UUID, limit: int = 20) -> List[CopilotMessage]:
        pass
