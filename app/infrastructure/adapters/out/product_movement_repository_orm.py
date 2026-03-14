"""
Repository ORM implementation para Product Movement
"""
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.product_movement_model import ProductMovement
from app.domain.ports.out.product_movement_repository import ProductMovementRepository
from app.infrastructure.db.models.product_movement_orm import ProductMovementORM
from typing import List


class ProductMovementORMRepository(ProductMovementRepository):
    """Implementación ORM del repositorio de movimientos de productos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_movements(self, company_id: str) -> List[ProductMovement]:
        """Obtiene todos los movimientos de una empresa"""
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        movements_orm = self.db.query(ProductMovementORM).filter(ProductMovementORM.id_empresa == company_uuid).all()
        return [self._orm_to_entity(m) for m in movements_orm]
    
    def get_movement_by_id(self, id_movimiento: int, company_id: str) -> ProductMovement:
        """Obtiene un movimiento por ID"""
        movement_orm = self.db.query(ProductMovementORM).filter(
            ProductMovementORM.id_movimiento == id_movimiento,
            ProductMovementORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(movement_orm) if movement_orm else None
    
    def get_movements_by_product(self, codigo_producto: str, company_id: str) -> List[ProductMovement]:
        """Obtiene todos los movimientos de un producto"""
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        movements_orm = self.db.query(ProductMovementORM).filter(
            ProductMovementORM.codigo_producto == codigo_producto,
            ProductMovementORM.id_empresa == company_uuid
        ).all()
        return [self._orm_to_entity(m) for m in movements_orm]
    
    def get_movements_by_process(self, id_proceso: UUID, company_id: str) -> List[ProductMovement]:
        """Obtiene movimientos conectados a un proceso (origen o destino)"""
        movements_orm = self.db.query(ProductMovementORM).filter(
            ProductMovementORM.id_empresa == company_id,
            ((ProductMovementORM.id_proceso_origen == id_proceso) | (ProductMovementORM.id_proceso_destino == id_proceso))
        ).all()
        return [self._orm_to_entity(m) for m in movements_orm]
    
    def get_movements_by_status(self, estado: str, company_id: str) -> List[ProductMovement]:
        """Obtiene movimientos por estado"""
        movements_orm = self.db.query(ProductMovementORM).filter(
            ProductMovementORM.estado == estado,
            ProductMovementORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(m) for m in movements_orm]
    
    def create_movement(self, movement: ProductMovement) -> ProductMovement:
        """Crea un nuevo movimiento"""
        movement_orm = self._entity_to_orm(movement)
        self.db.add(movement_orm)
        self.db.commit()
        self.db.refresh(movement_orm)
        return self._orm_to_entity(movement_orm)
    
    def update_movement(self, id_movimiento: int, movement_data: dict) -> ProductMovement:
        """Actualiza un movimiento"""
        movement_orm = self.db.query(ProductMovementORM).filter(ProductMovementORM.id_movimiento == id_movimiento).first()
        if not movement_orm:
            return None
        for key, value in movement_data.items():
            if value is not None:
                setattr(movement_orm, key, value)
        self.db.commit()
        self.db.refresh(movement_orm)
        return self._orm_to_entity(movement_orm)
    
    def update_movement_status(self, id_movimiento: int, nuevo_estado: str) -> ProductMovement:
        """Actualiza solo el estado de un movimiento"""
        movement_orm = self.db.query(ProductMovementORM).filter(ProductMovementORM.id_movimiento == id_movimiento).first()
        if not movement_orm:
            return None
        movement_orm.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(movement_orm)
        return self._orm_to_entity(movement_orm)
    
    def delete_movement(self, id_movimiento: int, company_id: str) -> bool:
        """Elimina un movimiento"""
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        movement_orm = self.db.query(ProductMovementORM).filter(
            ProductMovementORM.id_movimiento == id_movimiento,
            ProductMovementORM.id_empresa == company_uuid
        ).first()
        if not movement_orm:
            return False
        self.db.delete(movement_orm)
        self.db.commit()
        return True
    
    def _orm_to_entity(self, movement_orm: ProductMovementORM) -> ProductMovement:
        """Convierte ORM a entidad de dominio"""
        if not movement_orm:
            return None
        return ProductMovement(
            id_movimiento=movement_orm.id_movimiento,
            codigo_producto=movement_orm.codigo_producto,
            id_proceso_origen=movement_orm.id_proceso_origen,
            id_proceso_destino=movement_orm.id_proceso_destino,
            cantidad=movement_orm.cantidad,
            notas=movement_orm.notas,
            id_empresa=movement_orm.id_empresa,
            estado=movement_orm.estado,
            created_at=movement_orm.created_at,
            updated_at=movement_orm.updated_at
        )
    
    def _entity_to_orm(self, movement: ProductMovement) -> ProductMovementORM:
        """Convierte entidad de dominio a ORM"""
        return ProductMovementORM(
            codigo_producto=movement.codigo_producto,
            id_proceso_origen=movement.id_proceso_origen,
            id_proceso_destino=movement.id_proceso_destino,
            cantidad=movement.cantidad,
            notas=movement.notas,
            id_empresa=movement.id_empresa,
            estado=movement.estado,
            created_at=movement.created_at,
            updated_at=movement.updated_at
        )
