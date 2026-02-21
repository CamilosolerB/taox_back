"""
Implementación de repositorio ORM para Stock
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.ports.out.stock_location_repository import StockLocationRepository
from app.domain.ports.out.stock_warehouse_repository import StockWarehouseRepository
from app.domain.entities.stock_location_model import StockLocation
from app.domain.entities.stock_warehouse_model import StockWarehouse
from app.infrastructure.db.models.stock_orm import StockLocationORM, StockWarehouseORM


class StockLocationRepositoryORM(StockLocationRepository):
    """Implementación del repositorio de Stock Ubicación"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _orm_to_entity(self, orm: StockLocationORM) -> StockLocation:
        """Convierte modelo ORM a entidad"""
        if not orm:
            return None
        return StockLocation(
            id_ubicacion=orm.id_ubicacion,
            codigo_producto=orm.codigo_producto,
            cantidad=orm.cantidad,
            id_empresa=orm.id_empresa,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: StockLocation) -> StockLocationORM:
        """Convierte entidad a modelo ORM"""
        return StockLocationORM(
            id_ubicacion=entity.id_ubicacion,
            codigo_producto=entity.codigo_producto,
            cantidad=entity.cantidad,
            id_empresa=entity.id_empresa
        )
    
    def get_all_stocks(self, company_id: str) -> List[StockLocation]:
        """Obtiene todos los stocks"""
        stocks = self.session.query(StockLocationORM).filter(
            StockLocationORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(s) for s in stocks]
    
    def get_stock_by_location_and_product(
        self, 
        location_id: int, 
        product_code: str,
        company_id: str
    ) -> Optional[StockLocation]:
        """Obtiene stock de ubicación y producto"""
        stock = self.session.query(StockLocationORM).filter(
            StockLocationORM.id_ubicacion == location_id,
            StockLocationORM.codigo_producto == product_code,
            StockLocationORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(stock)
    
    def get_stocks_by_location(self, location_id: int, company_id: str) -> List[StockLocation]:
        """Obtiene stocks de una ubicación"""
        stocks = self.session.query(StockLocationORM).filter(
            StockLocationORM.id_ubicacion == location_id,
            StockLocationORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(s) for s in stocks]
    
    def get_stocks_by_product(self, product_code: str, company_id: str) -> List[StockLocation]:
        """Obtiene ubicaciones de un producto"""
        stocks = self.session.query(StockLocationORM).filter(
            StockLocationORM.codigo_producto == product_code,
            StockLocationORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(s) for s in stocks]
    
    def create_stock(self, stock: StockLocation) -> StockLocation:
        """Crea un stock"""
        orm = self._entity_to_orm(stock)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def update_stock(
        self,
        location_id: int,
        product_code: str,
        stock: StockLocation
    ) -> Optional[StockLocation]:
        """Actualiza un stock"""
        orm = self.session.query(StockLocationORM).filter(
            StockLocationORM.id_ubicacion == location_id,
            StockLocationORM.codigo_producto == product_code
        ).first()
        
        if not orm:
            return None
        
        orm.cantidad = stock.cantidad
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def delete_stock(self, location_id: int, product_code: str, company_id: str) -> bool:
        """Elimina un stock"""
        result = self.session.query(StockLocationORM).filter(
            StockLocationORM.id_ubicacion == location_id,
            StockLocationORM.codigo_producto == product_code,
            StockLocationORM.id_empresa == company_id
        ).delete()
        self.session.commit()
        return result > 0


class StockWarehouseRepositoryORM(StockWarehouseRepository):
    """Implementación del repositorio de Stock Almacén"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _orm_to_entity(self, orm: StockWarehouseORM) -> StockWarehouse:
        """Convierte modelo ORM a entidad"""
        if not orm:
            return None
        return StockWarehouse(
            codigo_producto=orm.codigo_producto,
            cantidad=orm.cantidad,
            id_empresa=orm.id_empresa,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: StockWarehouse) -> StockWarehouseORM:
        """Convierte entidad a modelo ORM"""
        return StockWarehouseORM(
            codigo_producto=entity.codigo_producto,
            cantidad=entity.cantidad,
            id_empresa=entity.id_empresa
        )
    
    def get_all_stocks(self, company_id: str) -> List[StockWarehouse]:
        """Obtiene todos los stocks"""
        stocks = self.session.query(StockWarehouseORM).filter(
            StockWarehouseORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(s) for s in stocks]
    
    def get_stock_by_product(self, product_code: str, company_id: str) -> Optional[StockWarehouse]:
        """Obtiene stock de un producto"""
        stock = self.session.query(StockWarehouseORM).filter(
            StockWarehouseORM.codigo_producto == product_code,
            StockWarehouseORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(stock)
    
    def create_stock(self, stock: StockWarehouse) -> StockWarehouse:
        """Crea un stock"""
        orm = self._entity_to_orm(stock)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def update_stock(self, product_code: str, stock: StockWarehouse) -> Optional[StockWarehouse]:
        """Actualiza un stock"""
        orm = self.session.query(StockWarehouseORM).filter(
            StockWarehouseORM.codigo_producto == product_code
        ).first()
        
        if not orm:
            return None
        
        orm.cantidad = stock.cantidad
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def delete_stock(self, product_code: str, company_id: str) -> bool:
        """Elimina un stock"""
        result = self.session.query(StockWarehouseORM).filter(
            StockWarehouseORM.codigo_producto == product_code,
            StockWarehouseORM.id_empresa == company_id
        ).delete()
        self.session.commit()
        return result > 0
    
    def increment_stock(self, product_code: str, quantity: int, company_id: str) -> Optional[StockWarehouse]:
        """Incrementa el stock"""
        stock = self.get_stock_by_product(product_code, company_id)
        if stock:
            stock.cantidad += quantity
            return self.update_stock(product_code, stock)
        return None
    
    def decrement_stock(self, product_code: str, quantity: int, company_id: str) -> Optional[StockWarehouse]:
        """Decrementa el stock"""
        stock = self.get_stock_by_product(product_code, company_id)
        if stock and stock.cantidad >= quantity:
            stock.cantidad -= quantity
            return self.update_stock(product_code, stock)
        return None
