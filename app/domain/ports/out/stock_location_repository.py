"""
Puerto de salida para repositorio de Stock Ubicación
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.stock_location_model import StockLocation


class StockLocationRepository(ABC):
    """
    Interfaz para el repositorio de Stock Ubicación
    """
    
    @abstractmethod
    def get_all_stocks(self, company_id: str) -> List[StockLocation]:
        """Obtiene todos los stocks de ubicaciones"""
        pass
    
    @abstractmethod
    def get_stock_by_location_and_product(
        self, 
        location_id: int, 
        product_code: str,
        company_id: str
    ) -> Optional[StockLocation]:
        """Obtiene el stock de un producto en una ubicación"""
        pass
    
    @abstractmethod
    def get_stocks_by_location(self, location_id: int, company_id: str) -> List[StockLocation]:
        """Obtiene todos los stocks de una ubicación"""
        pass
    
    @abstractmethod
    def get_stocks_by_product(self, product_code: str, company_id: str) -> List[StockLocation]:
        """Obtiene todas las ubicaciones de un producto"""
        pass
    
    @abstractmethod
    def create_stock(self, stock: StockLocation) -> StockLocation:
        """Crea un nuevo stock de ubicación"""
        pass
    
    @abstractmethod
    def update_stock(
        self,
        location_id: int,
        product_code: str,
        stock: StockLocation
    ) -> Optional[StockLocation]:
        """Actualiza un stock de ubicación"""
        pass
    
    @abstractmethod
    def delete_stock(self, location_id: int, product_code: str, company_id: str) -> bool:
        """Elimina un stock de ubicación"""
        pass
