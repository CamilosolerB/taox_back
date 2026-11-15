"""
DTOs for Copilot (chat interno + Telegram)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ChatMessageRequest(BaseModel):
    """Solicitud de mensaje al copiloto desde el chat interno."""
    contenido: str = Field(..., min_length=1, max_length=4000, description="Mensaje del usuario")
    conversation_id: Optional[UUID] = Field(None, description="Conversación existente a continuar")
    alerta_id: Optional[int] = Field(None, description="Alerta de stock asociada")
    codigo_producto: Optional[str] = Field(None, max_length=50, description="Producto asociado")


class OpenConversationRequest(BaseModel):
    """Abre (o crea) una conversación desde el chat interno."""
    alerta_id: Optional[int] = Field(None, description="Alerta de stock asociada")
    codigo_producto: Optional[str] = Field(None, max_length=50, description="Producto asociado")
    titulo: Optional[str] = Field(None, max_length=200)


class CopilotMessageResponse(BaseModel):
    id_mensaje: int
    rol: str
    contenido: str
    canal: Optional[str]
    proveedor: Optional[str]
    modelo: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class CopilotConversationResponse(BaseModel):
    id_conversation: UUID
    canal: str
    canal_chat_id: Optional[str]
    alerta_id: Optional[int]
    codigo_producto: Optional[str]
    titulo: Optional[str]
    estado: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReplenishmentDraftResponse(BaseModel):
    id_borrador: int
    alerta_id: Optional[int]
    codigo_producto: str
    cantidad_sugerida: Optional[float]
    unidad_medida: Optional[str]
    proveedor_sugerido: Optional[str]
    notas: Optional[str]
    estado: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CopilotReplyResponse(BaseModel):
    reply: str
    provider: str
    model: str
    conversation_id: UUID
    replenishment_draft: Optional[ReplenishmentDraftResponse] = None


class LinkStartResponse(BaseModel):
    code: str
    expires_at: datetime
    bot_link: Optional[str]
    instructions: str


class LinkStatusResponse(BaseModel):
    linked: bool
    chat_id: Optional[int] = None
    telegram_username: Optional[str] = None


class ReplenishmentDraftCreateRequest(BaseModel):
    codigo_producto: str = Field(..., min_length=1, max_length=50)
    alerta_id: Optional[int] = None
    conversation_id: Optional[UUID] = None
    cantidad_sugerida: Optional[float] = Field(None, ge=0)
    unidad_medida: Optional[str] = Field(None, max_length=20)
    proveedor_sugerido: Optional[str] = Field(None, max_length=50)
    notas: Optional[str] = Field(None, max_length=500)


class ReplenishmentDraftUpdateRequest(BaseModel):
    cantidad_sugerida: Optional[float] = Field(None, ge=0)
    unidad_medida: Optional[str] = Field(None, max_length=20)
    proveedor_sugerido: Optional[str] = Field(None, max_length=50)
    notas: Optional[str] = Field(None, max_length=500)
    estado: Optional[str] = Field(None, max_length=30)
