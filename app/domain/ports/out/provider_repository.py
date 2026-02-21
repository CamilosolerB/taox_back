"""
Puerto de salida para repositorio de Proveedor
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.provider_model import Provider


class ProviderRepository(ABC):
    """
    Interfaz para el repositorio de Proveedor
    
    Define el contrato que debe cumplir cualquier implementación del repositorio.
    """
    
    @abstractmethod
    def get_all_providers(self, company_id: str) -> List[Provider]:
        """Obtiene todos los proveedores de una empresa"""
        pass
    
    @abstractmethod
    def get_provider_by_id(self, provider_id: str, company_id: str) -> Optional[Provider]:
        """Obtiene un proveedor por su ID"""
        pass
    
    @abstractmethod
    def get_provider_by_email(self, email: str, company_id: str) -> Optional[Provider]:
        """Obtiene un proveedor por su email"""
        pass
    
    @abstractmethod
    def create_provider(self, provider: Provider) -> Provider:
        """Crea un nuevo proveedor"""
        pass
    
    @abstractmethod
    def update_provider(self, provider_id: str, provider: Provider) -> Optional[Provider]:
        """Actualiza un proveedor existente"""
        pass
    
    @abstractmethod
    def delete_provider(self, provider_id: str, company_id: str) -> bool:
        """Elimina un proveedor"""
        pass
