"""
Entidades de dominio del Copiloto IA (chat interno + Telegram)
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


@dataclass
class CopilotConversation:
    """Conversación del copiloto, compartida entre el chat interno y canales externos."""

    id_conversation: Optional[UUID] = None
    id_empresa: Optional[UUID] = None
    id_usuario: Optional[UUID] = None
    canal: str = "web"
    canal_chat_id: Optional[str] = None
    alerta_id: Optional[int] = None
    codigo_producto: Optional[str] = None
    titulo: Optional[str] = None
    estado: str = "activa"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CopilotMessage:
    """Mensaje individual de una conversación."""

    id_conversation: UUID
    rol: str  # user | assistant | system
    contenido: str
    id_mensaje: Optional[int] = None
    canal: Optional[str] = None
    proveedor: Optional[str] = None
    modelo: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class TelegramAccount:
    """Vinculación entre un chat de Telegram y un usuario/empresa de TAOX."""

    user_id: UUID
    chat_id: int
    id_cuenta: Optional[int] = None
    telegram_username: Optional[str] = None
    id_empresa: Optional[UUID] = None
    linked_at: Optional[datetime] = None


@dataclass
class TelegramLinkCode:
    """Código de un solo uso para vincular Telegram."""

    code: str
    user_id: UUID
    expires_at: datetime
    id_empresa: Optional[UUID] = None
    created_at: Optional[datetime] = None
    used_at: Optional[datetime] = None


@dataclass
class ReplenishmentDraft:
    """Borrador revisable de reabastecimiento (no genera órdenes de compra)."""

    id_empresa: UUID
    codigo_producto: str
    id_borrador: Optional[int] = None
    alerta_id: Optional[int] = None
    id_conversation: Optional[UUID] = None
    cantidad_sugerida: Optional[float] = None
    unidad_medida: Optional[str] = None
    proveedor_sugerido: Optional[str] = None
    notas: Optional[str] = None
    estado: str = "pendiente_revision"
    created_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class LlmResult:
    """Resultado de una generación del proveedor LLM."""

    content: str
    provider: str
    model: str


@dataclass
class CopilotReply:
    """Respuesta del copiloto junto con metadatos del turno."""

    reply: str
    provider: str
    model: str
    conversation_id: UUID
    replenishment_draft: Optional[ReplenishmentDraft] = None
    used_alerts: List[int] = field(default_factory=list)
