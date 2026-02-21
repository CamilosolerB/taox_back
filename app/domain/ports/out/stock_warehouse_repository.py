"""
Puerto de salida para repositorio de Stock Almacén
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.stock_warehouse_model import StockWarehouse


class StockWarehouseRepository(ABC):
    """
    Interfaz para el repositorio de Stock Almacén
    """
    
    @abstractmethod
    def get_all_stocks(self, company_id: str) -> List[StockWarehouse]:
        """Obtiene todos los stocks del almacén"""
        pass
    
    @abstractmethod
    def get_stock_by_product(
        self,
        product_code: str,
        company_id: str
    ) -> Optional[StockWarehouse]:
        """Obtiene el stock total de un producto"""
        pass
    
    @abstractmethod
    def create_stock(self, stock: StockWarehouse) -> StockWarehouse:
        """Crea un nuevo stock de almacén"""
        pass
    
    @abstractmethod
    def update_stock(
        self,
        product_code: str,
        stock: StockWarehouse
    ) -> Optional[StockWarehouse]:
        """Actualiza el stock de un producto"""
        pass
    
    @abstractmethod
    def delete_stock(self, product_code: str, company_id: str) -> bool:
        """Elimina el stock de un producto"""
        pass
    
    @abstractmethod
    def increment_stock(self, product_code: str, quantity: int, company_id: str) -> Optional[StockWarehouse]:
        """Incrementa el stock de un producto"""
        pass
    
    @abstractmethod
    def decrement_stock(self, product_code: str, quantity: int, company_id: str) -> Optional[StockWarehouse]:
        """Decrementa el stock de un producto"""
        pass
