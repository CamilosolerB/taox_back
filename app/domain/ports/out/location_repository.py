"""
Puerto de salida para repositorio de Ubicación
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.location_model import Location


class LocationRepository(ABC):
    """
    Interfaz para el repositorio de Ubicación
    """
    
    @abstractmethod
    def get_all_locations(self, company_id: str) -> List[Location]:
        """Obtiene todas las ubicaciones de una empresa"""
        pass
    
    @abstractmethod
    def get_location_by_id(self, location_id: int, company_id: str) -> Optional[Location]:
        """Obtiene una ubicación por su ID"""
        pass
    
    @abstractmethod
    def get_location_by_code(self, localizador: str, company_id: str) -> Optional[Location]:
        """Obtiene una ubicación por su código localizador"""
        pass
    
    @abstractmethod
    def create_location(self, location: Location) -> Location:
        """Crea una nueva ubicación"""
        pass
    
    @abstractmethod
    def update_location(self, location_id: int, location: Location) -> Optional[Location]:
        """Actualiza una ubicación"""
        pass
    
    @abstractmethod
    def delete_location(self, location_id: int, company_id: str) -> bool:
        """Elimina una ubicación"""
        pass
