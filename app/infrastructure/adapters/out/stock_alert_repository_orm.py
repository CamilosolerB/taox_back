"""
Repository ORM implementation para Stock Alert
"""
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.stock_alert_repository import StockAlertRepository
from app.infrastructure.db.models.stock_alert_orm import StockAlertORM
from typing import List
from datetime import datetime


class StockAlertORMRepository(StockAlertRepository):
    """Implementación ORM del repositorio de alertas de stock"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_alerts(self, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas de una empresa"""
        alerts_orm = self.db.query(StockAlertORM).filter(StockAlertORM.id_empresa == company_id).all()
        return [self._orm_to_entity(a) for a in alerts_orm]
    
    def get_alert_by_id(self, id_alerta: int, company_id: str) -> StockAlert:
        """Obtiene una alerta por ID"""
        alert_orm = self.db.query(StockAlertORM).filter(
            StockAlertORM.id_alerta == id_alerta,
            StockAlertORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(alert_orm) if alert_orm else None
    
    def get_alerts_by_product(self, codigo_producto: str, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas de un producto"""
        alerts_orm = self.db.query(StockAlertORM).filter(
            StockAlertORM.codigo_producto == codigo_producto,
            StockAlertORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(a) for a in alerts_orm]
    
    def get_alerts_by_process(self, id_proceso: UUID, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas en un proceso"""
        alerts_orm = self.db.query(StockAlertORM).filter(
            StockAlertORM.id_proceso == id_proceso,
            StockAlertORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(a) for a in alerts_orm]
    
    def get_active_alerts(self, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas activas"""
        alerts_orm = self.db.query(StockAlertORM).filter(
            StockAlertORM.id_empresa == company_id,
            StockAlertORM.estado == "activa"
        ).all()
        return [self._orm_to_entity(a) for a in alerts_orm]
    
    def get_alerts_by_type(self, tipo_alerta: str, company_id: str) -> List[StockAlert]:
        """Obtiene alertas por tipo"""
        alerts_orm = self.db.query(StockAlertORM).filter(
            StockAlertORM.tipo_alerta == tipo_alerta,
            StockAlertORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(a) for a in alerts_orm]
    
    def get_alerts_by_status(self, estado: str, company_id: str) -> List[StockAlert]:
        """Obtiene alertas por estado"""
        alerts_orm = self.db.query(StockAlertORM).filter(
            StockAlertORM.estado == estado,
            StockAlertORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(a) for a in alerts_orm]
    
    def create_alert(self, alert: StockAlert) -> StockAlert:
        """Crea una nueva alerta"""
        alert_orm = self._entity_to_orm(alert)
        self.db.add(alert_orm)
        self.db.commit()
        self.db.refresh(alert_orm)
        return self._orm_to_entity(alert_orm)
    
    def update_alert(self, id_alerta: int, alert_data: dict) -> StockAlert:
        """Actualiza una alerta"""
        alert_orm = self.db.query(StockAlertORM).filter(StockAlertORM.id_alerta == id_alerta).first()
        if not alert_orm:
            return None
        for key, value in alert_data.items():
            if value is not None:
                setattr(alert_orm, key, value)
        self.db.commit()
        self.db.refresh(alert_orm)
        return self._orm_to_entity(alert_orm)
    
    def resolve_alert(self, id_alerta: int) -> StockAlert:
        """Marca una alerta como resuelta"""
        alert_orm = self.db.query(StockAlertORM).filter(StockAlertORM.id_alerta == id_alerta).first()
        if not alert_orm:
            return None
        alert_orm.estado = "resuelta"
        alert_orm.resolved_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(alert_orm)
        return self._orm_to_entity(alert_orm)
    
    def delete_alert(self, id_alerta: int, company_id: str) -> bool:
        """Elimina una alerta"""
        alert_orm = self.db.query(StockAlertORM).filter(
            StockAlertORM.id_alerta == id_alerta,
            StockAlertORM.id_empresa == company_id
        ).first()
        if not alert_orm:
            return False
        self.db.delete(alert_orm)
        self.db.commit()
        return True
    
    def _orm_to_entity(self, alert_orm: StockAlertORM) -> StockAlert:
        """Convierte ORM a entidad de dominio"""
        if not alert_orm:
            return None
        return StockAlert(
            id_alerta=alert_orm.id_alerta,
            codigo_producto=alert_orm.codigo_producto,
            id_proceso=alert_orm.id_proceso,
            tipo_alerta=alert_orm.tipo_alerta,
            cantidad_actual=alert_orm.cantidad_actual,
            cantidad_referencia=alert_orm.cantidad_referencia,
            id_empresa=str(alert_orm.id_empresa),
            estado=alert_orm.estado,
            descripcion=alert_orm.descripcion,
            resolved_at=alert_orm.resolved_at,
            created_at=alert_orm.created_at,
            updated_at=alert_orm.updated_at
        )
    
    def _entity_to_orm(self, alert: StockAlert) -> StockAlertORM:
        """Convierte entidad de dominio a ORM"""
        return StockAlertORM(
            codigo_producto=alert.codigo_producto,
            id_proceso=alert.id_proceso,
            tipo_alerta=alert.tipo_alerta,
            cantidad_actual=alert.cantidad_actual,
            cantidad_referencia=alert.cantidad_referencia,
            id_empresa=alert.id_empresa,
            estado=alert.estado,
            descripcion=alert.descripcion
        )
