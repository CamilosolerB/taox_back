"""
Puerto de repositorio para borradores de reabastecimiento
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.copilot_models import ReplenishmentDraft


class ReplenishmentRepository(ABC):
    """Interfaz para persistencia de borradores de reabastecimiento."""

    @abstractmethod
    def create_draft(self, draft: ReplenishmentDraft) -> ReplenishmentDraft:
        pass

    @abstractmethod
    def get_drafts_by_company(self, company_id: str) -> List[ReplenishmentDraft]:
        pass

    @abstractmethod
    def get_draft_by_id(self, id_borrador: int, company_id: str) -> Optional[ReplenishmentDraft]:
        pass

    @abstractmethod
    def update_draft(self, id_borrador: int, company_id: str, data: dict) -> Optional[ReplenishmentDraft]:
        pass
