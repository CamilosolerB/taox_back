"""
Use cases: gestión de la vinculación de la cuenta de Telegram.
"""
import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional

from app.domain.entities.copilot_models import TelegramLinkCode
from app.domain.ports.out.telegram_repository import TelegramRepository

logger = logging.getLogger(__name__)

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
CODE_LENGTH = 8
CODE_TTL_MINUTES = 15


class CreateLinkCodeUseCase:
    """Genera un código temporal para vincular Telegram con el usuario."""

    def __init__(self, telegram_repository: TelegramRepository, bot_link: Optional[str] = None):
        self.telegram_repository = telegram_repository
        self.bot_link = bot_link

    def execute(self, user_id: str, company_id: Optional[str]) -> TelegramLinkCode:
        code = self._generate_unique_code()
        entity = TelegramLinkCode(
            code=code,
            user_id=user_id,
            id_empresa=company_id,
            expires_at=datetime.utcnow() + timedelta(minutes=CODE_TTL_MINUTES),
        )
        return self.telegram_repository.create_link_code(entity)

    def _generate_unique_code(self) -> str:
        for _ in range(10):
            code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
            if self.telegram_repository.get_link_code(code) is None:
                return code
        raise RuntimeError("No se pudo generar un código de vinculación único")


class GetLinkStatusUseCase:
    """Consulta si el usuario tiene Telegram vinculado."""

    def __init__(self, telegram_repository: TelegramRepository):
        self.telegram_repository = telegram_repository

    def execute(self, user_id: str):
        return self.telegram_repository.get_account_by_user(user_id)


class UnlinkTelegramUseCase:
    """Desvincula la cuenta de Telegram del usuario."""

    def __init__(self, telegram_repository: TelegramRepository):
        self.telegram_repository = telegram_repository

    def execute(self, user_id: str) -> bool:
        return self.telegram_repository.delete_account_by_user(user_id)
