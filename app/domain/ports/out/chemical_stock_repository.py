"""
Puerto (Interfaz) de Repositorio para Chemical Stock
"""
from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.chemical_stock_model import ChemicalStock
from typing import List


class ChemicalStockRepository(ABC):
    """Interfaz para repositorio de stock de químicos"""
    
    @abstractmethod
    def get_all_stocks(self, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks de una empresa"""
        pass
    
    @abstractmethod
    def get_stock_by_id(self, id_stock_quimico: int, company_id: str) -> ChemicalStock:
        """Obtiene un stock por ID"""
        pass
    
    @abstractmethod
    def get_stock_by_product_and_process(self, codigo_producto: str, id_proceso: UUID, company_id: str) -> ChemicalStock:
        """Obtiene el stock de un producto en un proceso específico"""
        pass
    
    @abstractmethod
    def get_stocks_by_product(self, codigo_producto: str, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks de un producto"""
        pass
    
    @abstractmethod
    def get_stocks_by_process(self, id_proceso: UUID, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks en un proceso"""
        pass
    
    @abstractmethod
    def get_critical_stocks(self, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks en nivel crítico (cantidad_actual < cantidad_minima)"""
        pass
    
    @abstractmethod
    def get_low_stocks(self, company_id: str) -> List[ChemicalStock]:
        """Obtiene todos los stocks en nivel bajo (25-50% de cantidad_minima)"""
        pass
    
    @abstractmethod
    def create_stock(self, stock: ChemicalStock) -> ChemicalStock:
        """Crea un nuevo stock"""
        pass
    
    @abstractmethod
    def update_stock(self, id_stock_quimico: int, stock_data: dict) -> ChemicalStock:
        """Actualiza un stock"""
        pass
    
    @abstractmethod
    def update_stock_quantity(self, id_stock_quimico: int, nueva_cantidad: float) -> ChemicalStock:
        """Actualiza solo la cantidad de un stock"""
        pass
    
    @abstractmethod
    def delete_stock(self, id_stock_quimico: int, company_id: str) -> bool:
        """Elimina un stock"""
        pass
