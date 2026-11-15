"""
Canal de notificación Telegram (Bot API)
"""
import logging

import requests

from app.domain.ports.out.notification_channel import NotificationChannel

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE = "https://api.telegram.org"


class TelegramChannel(NotificationChannel):
    """Implementación del canal Telegram usando la Bot API oficial."""

    def __init__(self, bot_token: str | None, timeout: int = 15):
        self.bot_token = bot_token
        self.timeout = timeout

    @property
    def channel_name(self) -> str:
        return "telegram"

    @property
    def is_enabled(self) -> bool:
        return bool(self.bot_token)

    def send_message(self, chat_id: str, text: str) -> bool:
        if not self.is_enabled:
            logger.warning("Telegram deshabilitado: TELEGRAM_BOT_TOKEN no configurado")
            return False

        url = f"{TELEGRAM_API_BASE}/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
        except requests.RequestException as exc:
            logger.error(f"Error de red enviando mensaje de Telegram: {exc}")
            return False

        if response.status_code >= 400:
            logger.warning(
                f"Telegram respondió {response.status_code} con parse_mode HTML; "
                f"se reintenta en texto plano: {response.text[:300]}"
            )
            # El contenido dinámico (p. ej. descripciones con '<' o '&') puede romper
            # el parseo HTML de Telegram; se reintenta sin formato para no perder el aviso.
            payload.pop("parse_mode", None)
            try:
                response = requests.post(url, json=payload, timeout=self.timeout)
            except requests.RequestException as exc:
                logger.error(f"Error de red reintentando mensaje de Telegram: {exc}")
                return False
            if response.status_code >= 400:
                logger.error(
                    f"Telegram respondió {response.status_code}: {response.text[:500]}"
                )
                return False
        return True
