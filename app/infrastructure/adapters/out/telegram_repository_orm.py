"""
Implementación ORM del repositorio de Telegram (cuentas, códigos e idempotencia)
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.entities.copilot_models import TelegramAccount, TelegramLinkCode
from app.domain.ports.out.telegram_repository import TelegramRepository
from app.infrastructure.db.models.telegram_account_orm import TelegramAccountORM
from app.infrastructure.db.models.telegram_link_code_orm import TelegramLinkCodeORM
from app.infrastructure.db.models.telegram_update_orm import TelegramUpdateORM


class TelegramORMRepository(TelegramRepository):
    """Persistencia de cuentas Telegram, códigos de vinculación y updates."""

    def __init__(self, db: Session):
        self.db = db

    def create_link_code(self, link_code: TelegramLinkCode) -> TelegramLinkCode:
        orm = TelegramLinkCodeORM(
            code=link_code.code,
            user_id=link_code.user_id,
            id_empresa=link_code.id_empresa,
            expires_at=link_code.expires_at,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._code_to_entity(orm)

    def get_link_code(self, code: str) -> Optional[TelegramLinkCode]:
        orm = self.db.query(TelegramLinkCodeORM).filter(TelegramLinkCodeORM.code == code).first()
        return self._code_to_entity(orm) if orm else None

    def mark_link_code_used(self, code: str) -> None:
        orm = self.db.query(TelegramLinkCodeORM).filter(TelegramLinkCodeORM.code == code).first()
        if orm:
            from datetime import datetime

            orm.used_at = datetime.utcnow()
            self.db.commit()

    def upsert_account(self, account: TelegramAccount) -> TelegramAccount:
        orm = self.db.query(TelegramAccountORM).filter(
            TelegramAccountORM.user_id == account.user_id
        ).first()
        if orm is None:
            # Si el chat ya estaba vinculado a otro usuario, se reasigna al actual.
            orm = self.db.query(TelegramAccountORM).filter(
                TelegramAccountORM.chat_id == account.chat_id
            ).first()
        if orm:
            orm.user_id = account.user_id
            orm.chat_id = account.chat_id
            orm.telegram_username = account.telegram_username
            orm.id_empresa = account.id_empresa
        else:
            orm = TelegramAccountORM(
                user_id=account.user_id,
                chat_id=account.chat_id,
                telegram_username=account.telegram_username,
                id_empresa=account.id_empresa,
            )
            self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._acc_to_entity(orm)

    def get_account_by_user(self, user_id: UUID) -> Optional[TelegramAccount]:
        orm = self.db.query(TelegramAccountORM).filter(TelegramAccountORM.user_id == user_id).first()
        return self._acc_to_entity(orm) if orm else None

    def get_account_by_chat(self, chat_id: int) -> Optional[TelegramAccount]:
        orm = self.db.query(TelegramAccountORM).filter(TelegramAccountORM.chat_id == chat_id).first()
        return self._acc_to_entity(orm) if orm else None

    def get_accounts_by_company(self, company_id: str) -> List[TelegramAccount]:
        rows = self.db.query(TelegramAccountORM).filter(
            TelegramAccountORM.id_empresa == company_id
        ).all()
        return [self._acc_to_entity(r) for r in rows]

    def delete_account_by_user(self, user_id: UUID) -> bool:
        orm = self.db.query(TelegramAccountORM).filter(TelegramAccountORM.user_id == user_id).first()
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True

    def register_update(self, update_id: int) -> bool:
        orm = TelegramUpdateORM(update_id=update_id)
        self.db.add(orm)
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def _code_to_entity(self, orm: TelegramLinkCodeORM) -> TelegramLinkCode:
        return TelegramLinkCode(
            code=orm.code,
            user_id=orm.user_id,
            id_empresa=orm.id_empresa,
            expires_at=orm.expires_at,
            created_at=orm.created_at,
            used_at=orm.used_at,
        )

    def _acc_to_entity(self, orm: TelegramAccountORM) -> TelegramAccount:
        return TelegramAccount(
            id_cuenta=orm.id_cuenta,
            user_id=orm.user_id,
            chat_id=orm.chat_id,
            telegram_username=orm.telegram_username,
            id_empresa=orm.id_empresa,
            linked_at=orm.linked_at,
        )
