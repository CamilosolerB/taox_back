"""
Puerto (Interfaz) de Repositorio para Product Movement
"""
from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.product_movement_model import ProductMovement
from typing import List


class ProductMovementRepository(ABC):
    """Interfaz para repositorio de movimientos de productos"""
    
    @abstractmethod
    def get_all_movements(self, company_id: str) -> List[ProductMovement]:
        """Obtiene todos los movimientos de una empresa"""
        pass
    
    @abstractmethod
    def get_movement_by_id(self, id_movimiento: int, company_id: str) -> ProductMovement:
        """Obtiene un movimiento por ID"""
        pass
    
    @abstractmethod
    def get_movements_by_product(self, codigo_producto: str, company_id: str) -> List[ProductMovement]:
        """Obtiene todos los movimientos de un producto"""
        pass
    
    @abstractmethod
    def get_movements_by_process(self, id_proceso: UUID, company_id: str) -> List[ProductMovement]:
        """Obtiene movimientos conectados a un proceso (origen o destino)"""
        pass
    
    @abstractmethod
    def get_movements_by_status(self, estado: str, company_id: str) -> List[ProductMovement]:
        """Obtiene movimientos por estado"""
        pass
    
    @abstractmethod
    def create_movement(self, movement: ProductMovement) -> ProductMovement:
        """Crea un nuevo movimiento"""
        pass
    
    @abstractmethod
    def update_movement(self, id_movimiento: int, movement_data: dict) -> ProductMovement:
        """Actualiza un movimiento"""
        pass
    
    @abstractmethod
    def update_movement_status(self, id_movimiento: int, nuevo_estado: str) -> ProductMovement:
        """Actualiza solo el estado de un movimiento"""
        pass
    
    @abstractmethod
    def delete_movement(self, id_movimiento: int, company_id: str) -> bool:
        """Elimina un movimiento"""
        pass
