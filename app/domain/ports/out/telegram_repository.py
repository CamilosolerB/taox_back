"""
Puerto de repositorio para cuentas Telegram, códigos de vinculación e idempotencia de updates
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.copilot_models import TelegramAccount, TelegramLinkCode


class TelegramRepository(ABC):
    """Interfaz para la persistencia relacionada con Telegram."""

    # --- Vinculación ---
    @abstractmethod
    def create_link_code(self, link_code: TelegramLinkCode) -> TelegramLinkCode:
        pass

    @abstractmethod
    def get_link_code(self, code: str) -> Optional[TelegramLinkCode]:
        pass

    @abstractmethod
    def mark_link_code_used(self, code: str) -> None:
        pass

    # --- Cuentas ---
    @abstractmethod
    def upsert_account(self, account: TelegramAccount) -> TelegramAccount:
        pass

    @abstractmethod
    def get_account_by_user(self, user_id: UUID) -> Optional[TelegramAccount]:
        pass

    @abstractmethod
    def get_account_by_chat(self, chat_id: int) -> Optional[TelegramAccount]:
        pass

    @abstractmethod
    def get_accounts_by_company(self, company_id: str) -> List[TelegramAccount]:
        pass

    @abstractmethod
    def delete_account_by_user(self, user_id: UUID) -> bool:
        pass

    # --- Idempotencia ---
    @abstractmethod
    def register_update(self, update_id: int) -> bool:
        """Registra un update_id. Retorna False si ya había sido procesado."""
        pass
