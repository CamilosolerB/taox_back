"""
Use case: procesar una actualización entrante de Telegram (webhook).

Garantiza idempotencia por update_id, resuelve la vinculación de la cuenta,
y enruta el mensaje al caso de uso de chat reutilizando la conversación del canal.
"""
import logging
from datetime import datetime
from typing import Optional

from app.domain.entities.copilot_models import CopilotConversation, TelegramAccount
from app.domain.ports.out.copilot_repository import CopilotRepository
from app.domain.ports.out.notification_channel import NotificationChannel
from app.domain.ports.out.telegram_repository import TelegramRepository
from app.application.use_cases.copilot_case.send_chat_message import SendChatMessageUseCase

logger = logging.getLogger(__name__)


class ProcessTelegramUpdateUseCase:
    """Procesa un update de Telegram y responde por el mismo canal."""

    def __init__(
        self,
        telegram_repository: TelegramRepository,
        copilot_repository: CopilotRepository,
        chat_use_case: SendChatMessageUseCase,
        channel: NotificationChannel,
    ):
        self.telegram_repository = telegram_repository
        self.copilot_repository = copilot_repository
        self.chat_use_case = chat_use_case
        self.channel = channel

    def execute(self, update: dict) -> dict:
        update_id = update.get("update_id")
        if update_id is not None:
            if not self.telegram_repository.register_update(int(update_id)):
                logger.info(f"Update {update_id} duplicado; se ignora")
                return {"ok": True, "duplicate": True}

        message = update.get("message") or update.get("edited_message")
        if not message:
            return {"ok": True, "ignored": "sin mensaje"}

        chat = message.get("chat") or {}
        chat_id = chat.get("id")
        text = (message.get("text") or "").strip()
        username = (message.get("from") or {}).get("username")

        if chat_id is None:
            return {"ok": True, "ignored": "sin chat_id"}

        if text.startswith("/start") or text.startswith("/vincular"):
            return self._handle_start(chat_id, username, text)

        if not text:
            self.channel.send_message(str(chat_id), "Por ahora solo proceso mensajes de texto.")
            return {"ok": True, "ignored": "texto vacío"}

        return self._handle_message(chat_id, text)

    def _handle_start(self, chat_id: int, username: Optional[str], text: str) -> dict:
        parts = text.split()
        code = parts[1].strip().upper() if len(parts) > 1 else None

        if not code:
            self.channel.send_message(
                str(chat_id),
                "Hola, soy el copiloto de TAOX. Para vincular tu cuenta abre TAOX, "
                "genera un código en la sección del copiloto y envíamelo así: "
                f"<code>/start TU_CODIGO</code>\nTu chat_id es <code>{chat_id}</code>.",
            )
            return {"ok": True, "action": "start_help"}

        link_code = self.telegram_repository.get_link_code(code)
        if link_code is None or link_code.used_at is not None:
            self.channel.send_message(str(chat_id), "Ese código no es válido o ya fue usado.")
            return {"ok": True, "action": "link_failed"}
        if link_code.expires_at < datetime.utcnow():
            self.channel.send_message(str(chat_id), "Ese código expiró. Genera uno nuevo en TAOX.")
            return {"ok": True, "action": "link_expired"}

        self.telegram_repository.upsert_account(
            TelegramAccount(
                user_id=link_code.user_id,
                chat_id=chat_id,
                telegram_username=username,
                id_empresa=link_code.id_empresa,
            )
        )
        self.telegram_repository.mark_link_code_used(code)
        self.channel.send_message(
            str(chat_id),
            "¡Listo! Tu cuenta de Telegram quedó vinculada al copiloto de TAOX. "
            "Te avisaré cuando se detecten alertas de stock y podrás conversar conmigo aquí.",
        )
        return {"ok": True, "action": "linked"}

    def _handle_message(self, chat_id: int, text: str) -> dict:
        account = self.telegram_repository.get_account_by_chat(chat_id)
        if account is None:
            self.channel.send_message(
                str(chat_id),
                "Tu cuenta de Telegram no está vinculada. Genera un código en TAOX y "
                "envíamelo con /start TU_CODIGO.",
            )
            return {"ok": True, "action": "not_linked"}

        if account.id_empresa is None:
            self.channel.send_message(
                str(chat_id),
                "Tu usuario no está asociado a una empresa, así que no puedo consultar inventario.",
            )
            return {"ok": True, "action": "no_company"}

        conversation = self.copilot_repository.get_latest_conversation_by_channel(
            "telegram", str(chat_id)
        )
        if conversation is None:
            conversation = self.copilot_repository.create_conversation(
                CopilotConversation(
                    id_empresa=account.id_empresa,
                    id_usuario=account.user_id,
                    canal="telegram",
                    canal_chat_id=str(chat_id),
                    titulo="Conversación por Telegram",
                )
            )

        result = self.chat_use_case.execute(
            company_id=str(account.id_empresa),
            user_id=str(account.user_id),
            message=text,
            conversation_id=conversation.id_conversation,
            canal="telegram",
        )
        self.channel.send_message(str(chat_id), result.reply)
        return {"ok": True, "action": "replied", "conversation_id": str(result.conversation_id)}
