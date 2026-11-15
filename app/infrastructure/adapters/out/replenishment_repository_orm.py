"""
Implementación ORM del repositorio de borradores de reabastecimiento
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.copilot_models import ReplenishmentDraft
from app.domain.ports.out.replenishment_repository import ReplenishmentRepository
from app.infrastructure.db.models.replenishment_draft_orm import ReplenishmentDraftORM


class ReplenishmentORMRepository(ReplenishmentRepository):
    """Persistencia de borradores de reabastecimiento."""

    def __init__(self, db: Session):
        self.db = db

    def create_draft(self, draft: ReplenishmentDraft) -> ReplenishmentDraft:
        orm = ReplenishmentDraftORM(
            id_empresa=draft.id_empresa,
            alerta_id=draft.alerta_id,
            id_conversation=draft.id_conversation,
            codigo_producto=draft.codigo_producto,
            cantidad_sugerida=draft.cantidad_sugerida,
            unidad_medida=draft.unidad_medida,
            proveedor_sugerido=draft.proveedor_sugerido,
            notas=draft.notas,
            estado=draft.estado,
            created_by=draft.created_by,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._to_entity(orm)

    def get_drafts_by_company(self, company_id: str) -> List[ReplenishmentDraft]:
        rows = (
            self.db.query(ReplenishmentDraftORM)
            .filter(ReplenishmentDraftORM.id_empresa == company_id)
            .order_by(ReplenishmentDraftORM.created_at.desc())
            .all()
        )
        return [self._to_entity(r) for r in rows]

    def get_draft_by_id(self, id_borrador: int, company_id: str) -> Optional[ReplenishmentDraft]:
        orm = (
            self.db.query(ReplenishmentDraftORM)
            .filter(
                ReplenishmentDraftORM.id_borrador == id_borrador,
                ReplenishmentDraftORM.id_empresa == company_id,
            )
            .first()
        )
        return self._to_entity(orm) if orm else None

    def update_draft(self, id_borrador: int, company_id: str, data: dict) -> Optional[ReplenishmentDraft]:
        orm = (
            self.db.query(ReplenishmentDraftORM)
            .filter(
                ReplenishmentDraftORM.id_borrador == id_borrador,
                ReplenishmentDraftORM.id_empresa == company_id,
            )
            .first()
        )
        if not orm:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(orm, key, value)
        self.db.commit()
        self.db.refresh(orm)
        return self._to_entity(orm)

    def _to_entity(self, orm: ReplenishmentDraftORM) -> ReplenishmentDraft:
        return ReplenishmentDraft(
            id_borrador=orm.id_borrador,
            id_empresa=orm.id_empresa,
            alerta_id=orm.alerta_id,
            id_conversation=orm.id_conversation,
            codigo_producto=orm.codigo_producto,
            cantidad_sugerida=orm.cantidad_sugerida,
            unidad_medida=orm.unidad_medida,
            proveedor_sugerido=orm.proveedor_sugerido,
            notas=orm.notas,
            estado=orm.estado,
            created_by=orm.created_by,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
