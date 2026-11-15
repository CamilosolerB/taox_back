"""
Puerto de canal de notificación saliente (Telegram, WhatsApp en fase 2, etc.)
"""
from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    """Interfaz para canales de mensajería externa."""

    @property
    @abstractmethod
    def channel_name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_enabled(self) -> bool:
        """Indica si el canal está configurado y operativo."""
        pass

    @abstractmethod
    def send_message(self, chat_id: str, text: str) -> bool:
        """
        Envía un mensaje de texto a un destino del canal.

        Returns:
            True si el envío fue aceptado, False en caso contrario.
        """
        pass
