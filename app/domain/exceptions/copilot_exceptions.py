"""
Excepciones de dominio del Copiloto IA
"""


class CopilotError(Exception):
    """Error base del copiloto."""


class LlmProviderError(CopilotError):
    """Falla al comunicarse con el proveedor LLM (red, auth, cuota o formato)."""


class ChannelDeliveryError(CopilotError):
    """Falla al entregar un mensaje por un canal externo (p.ej. Telegram)."""


class CopilotNotLinkedError(CopilotError):
    """El usuario o chat no tiene una vinculación válida con el copiloto."""


class TelegramLinkError(CopilotError):
    """El código de vinculación es inválido, expirado o ya usado."""
