"""
Repository ORM implementation para Chemical Stock
"""
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.chemical_stock_model import ChemicalStock
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository
from app.infrastructure.db.models.chemical_stock_orm import ChemicalStockORM
from typing import List


class ChemicalStockORMRepository(ChemicalStockRepository):
    """Implementación ORM del repositorio de stock de químicos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_stocks(self, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks de una empresa"""
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        stocks_orm = self.db.query(ChemicalStockORM).filter(ChemicalStockORM.id_empresa == company_uuid).all()
        return [self._orm_to_entity(s) for s in stocks_orm]
    
    def get_stock_by_id(self, id_stock_quimico: int, company_id: str) -> ChemicalStock:
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        stock_orm = self.db.query(ChemicalStockORM).filter(
            ChemicalStockORM.id_stock_quimico == id_stock_quimico,
            ChemicalStockORM.id_empresa == company_uuid
        ).first()
        return self._orm_to_entity(stock_orm) if stock_orm else None
    
    def get_stock_by_product_and_process(self, codigo_producto: str, id_processo: UUID, company_id: str) -> ChemicalStock:
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        processo_uuid = UUID(id_processo) if isinstance(id_processo, str) else id_processo
        stock_orm = self.db.query(ChemicalStockORM).filter(
            ChemicalStockORM.codigo_product == codigo_producto,
            ChemicalStockORM.id_processo == processo_uuid,
            ChemicalStockORM.id_empresa == company_uuid
        ).first()
        return self._orm_to_entity(stock_orm) if stock_orm else None
    
    def get_stocks_by_product(self, codigo_producto: str, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks de un producto"""
        stocks_orm = self.db.query(ChemicalStockORM).filter(
            ChemicalStockORM.codigo_producto == codigo_producto,
            ChemicalStockORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(s) for s in stocks_orm]
    
    def get_stocks_by_process(self, id_proceso: UUID, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks en un proceso"""
        stocks_orm = self.db.query(ChemicalStockORM).filter(
            ChemicalStockORM.id_proceso == id_proceso,
            ChemicalStockORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(s) for s in stocks_orm]
    
    def get_critical_stocks(self, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks en nivel crítico"""
        stocks_orm = self.db.query(ChemicalStockORM).filter(
            ChemicalStockORM.id_empresa == company_id,
            ChemicalStockORM.cantidad_actual < ChemicalStockORM.cantidad_minima
        ).all()
        return [self._orm_to_entity(s) for s in stocks_orm]
    
    def get_low_stocks(self, company_id: str) -> List[ChemicalStock]:
        """Obtiene stocks en nivel bajo (25-50% de mínimo)"""
        stocks_orm = self.db.query(ChemicalStockORM).filter(
            ChemicalStockORM.id_empresa == company_id,
            ChemicalStockORM.cantidad_actual >= (ChemicalStockORM.cantidad_minima * 0.25),
            ChemicalStockORM.cantidad_actual < (ChemicalStockORM.cantidad_minima * 0.5)
        ).all()
        return [self._orm_to_entity(s) for s in stocks_orm]
    
    def create_stock(self, stock: ChemicalStock) -> ChemicalStock:
        stock_orm = self._entity_to_orm(stock)
        self.db.add(stock_orm)
        self.db.commit()
        self.db.refresh(stock_orm)
        return self._orm_to_entity(stock_orm)
    
    def update_stock(self, id_stock_quimico: int, stock_data: dict) -> ChemicalStock:
        """Actualiza un stock"""
        stock_orm = self.db.query(ChemicalStockORM).filter(ChemicalStockORM.id_stock_quimico == id_stock_quimico).first()
        if not stock_orm:
            return None
        for key, value in stock_data.items():
            if value is not None:
                setattr(stock_orm, key, value)
        self.db.commit()
        self.db.refresh(stock_orm)
        return self._orm_to_entity(stock_orm)
    
    def update_stock_quantity(self, id_stock_quimico: int, nueva_cantidad: float) -> ChemicalStock:
        """Actualiza solo la cantidad de un stock"""
        stock_orm = self.db.query(ChemicalStockORM).filter(ChemicalStockORM.id_stock_quimico == id_stock_quimico).first()
        if not stock_orm:
            return None
        stock_orm.cantidad_actual = nueva_cantidad
        self.db.commit()
        self.db.refresh(stock_orm)
        return self._orm_to_entity(stock_orm)
    
    def delete_stock(self, id_stock_quimico: int, company_id: str) -> bool:
        """Elimina un stock"""
        stock_orm = self.db.query(ChemicalStockORM).filter(
            ChemicalStockORM.id_stock_quimico == id_stock_quimico,
            ChemicalStockORM.id_empresa == company_id
        ).first()
        if not stock_orm:
            return False
        self.db.delete(stock_orm)
        self.db.commit()
        return True
    
    def _orm_to_entity(self, stock_orm: ChemicalStockORM) -> ChemicalStock:
        """Convierte ORM a entidad de dominio"""
        if not stock_orm:
            return None
        return ChemicalStock(
            id_stock_quimico=stock_orm.id_stock_quimico,
            codigo_producto=stock_orm.codigo_producto,
            id_proceso=stock_orm.id_proceso,
            cantidad_actual=stock_orm.cantidad_actual,
            cantidad_minima=stock_orm.cantidad_minima,
            cantidad_maxima=stock_orm.cantidad_maxima,
            unidad_medida=stock_orm.unidad_medida,
            id_empresa=str(stock_orm.id_empresa),
            is_active=stock_orm.is_active,
            created_at=stock_orm.created_at,
            updated_at=stock_orm.updated_at
        )
    
    def _entity_to_orm(self, stock: ChemicalStock) -> ChemicalStockORM:
        """Convierte entidad de dominio a ORM"""
        return ChemicalStockORM(
            codigo_producto=stock.codigo_producto,
            id_proceso=stock.id_proceso,
            cantidad_actual=stock.cantidad_actual,
            cantidad_minima=stock.cantidad_minima,
            cantidad_maxima=stock.cantidad_maxima,
            unidad_medida=stock.unidad_medida,
            id_empresa=stock.id_empresa,
            is_active=stock.is_active
        )
