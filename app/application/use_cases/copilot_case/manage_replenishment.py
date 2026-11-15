"""
Use cases: gestión de borradores de reabastecimiento (siempre pendientes de revisión humana).
"""
from typing import List, Optional
from uuid import UUID

from app.domain.entities.copilot_models import ReplenishmentDraft
from app.domain.ports.out.replenishment_repository import ReplenishmentRepository


class CreateReplenishmentDraftUseCase:
    """Crea un borrador de reabastecimiento pendiente de revisión."""

    def __init__(self, replenishment_repository: ReplenishmentRepository):
        self.replenishment_repository = replenishment_repository

    def execute(
        self,
        company_id: str,
        user_id: Optional[str],
        codigo_producto: str,
        alerta_id: Optional[int] = None,
        id_conversation: Optional[UUID] = None,
        cantidad_sugerida: Optional[float] = None,
        unidad_medida: Optional[str] = None,
        proveedor_sugerido: Optional[str] = None,
        notas: Optional[str] = None,
    ) -> ReplenishmentDraft:
        return self.replenishment_repository.create_draft(
            ReplenishmentDraft(
                id_empresa=company_id,
                codigo_producto=codigo_producto,
                alerta_id=alerta_id,
                id_conversation=id_conversation,
                cantidad_sugerida=cantidad_sugerida,
                unidad_medida=unidad_medida,
                proveedor_sugerido=proveedor_sugerido,
                notas=notas,
                created_by=user_id,
            )
        )


class GetReplenishmentDraftsUseCase:
    """Lista los borradores de reabastecimiento de la empresa."""

    def __init__(self, replenishment_repository: ReplenishmentRepository):
        self.replenishment_repository = replenishment_repository

    def execute(self, company_id: str) -> List[ReplenishmentDraft]:
        return self.replenishment_repository.get_drafts_by_company(company_id)


class UpdateReplenishmentDraftUseCase:
    """Actualiza un borrador de reabastecimiento (revisión humana)."""

    def __init__(self, replenishment_repository: ReplenishmentRepository):
        self.replenishment_repository = replenishment_repository

    def execute(self, id_borrador: int, company_id: str, data: dict) -> ReplenishmentDraft:
        draft = self.replenishment_repository.update_draft(id_borrador, company_id, data)
        if draft is None:
            raise ValueError("Borrador no encontrado para esta empresa")
        return draft
