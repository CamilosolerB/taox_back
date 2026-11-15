"""
Use cases: gestión de conversaciones del copiloto desde el chat interno.
"""
from typing import List, Optional
from uuid import UUID

from app.domain.entities.copilot_models import CopilotConversation, CopilotMessage
from app.domain.ports.out.copilot_repository import CopilotRepository


class OpenConversationUseCase:
    """Abre (o crea) una conversación para el chat interno."""

    def __init__(self, copilot_repository: CopilotRepository):
        self.copilot_repository = copilot_repository

    def execute(
        self,
        company_id: str,
        user_id: Optional[str],
        alerta_id: Optional[int] = None,
        codigo_producto: Optional[str] = None,
        titulo: Optional[str] = None,
    ) -> CopilotConversation:
        return self.copilot_repository.create_conversation(
            CopilotConversation(
                id_empresa=company_id,
                id_usuario=user_id,
                canal="web",
                alerta_id=alerta_id,
                codigo_producto=codigo_producto,
                titulo=titulo or codigo_producto or "Conversación con el copiloto",
            )
        )


class GetConversationsUseCase:
    """Lista las conversaciones de la empresa."""

    def __init__(self, copilot_repository: CopilotRepository):
        self.copilot_repository = copilot_repository

    def execute(self, company_id: str) -> List[CopilotConversation]:
        return self.copilot_repository.get_conversations_by_company(company_id)


class GetConversationMessagesUseCase:
    """Lista los mensajes de una conversación (validando pertenencia a la empresa)."""

    def __init__(self, copilot_repository: CopilotRepository):
        self.copilot_repository = copilot_repository

    def execute(self, id_conversation: UUID, company_id: str) -> List[CopilotMessage]:
        conversation = self.copilot_repository.get_conversation(id_conversation, company_id)
        if conversation is None:
            raise ValueError("Conversación no encontrada para esta empresa")
        return self.copilot_repository.get_messages(id_conversation, company_id)
