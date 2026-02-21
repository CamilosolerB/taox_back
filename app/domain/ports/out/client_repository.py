"""
Puerto de salida para repositorio de Cliente
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.client_model import Client


class ClientRepository(ABC):
    """
    Interfaz para el repositorio de Cliente
    """
    
    @abstractmethod
    def get_all_clients(self, company_id: str) -> List[Client]:
        """Obtiene todos los clientes de una empresa"""
        pass
    
    @abstractmethod
    def get_client_by_id(self, client_id: str, company_id: str) -> Optional[Client]:
        """Obtiene un cliente por su ID"""
        pass
    
    @abstractmethod
    def get_client_by_email(self, email: str, company_id: str) -> Optional[Client]:
        """Obtiene un cliente por su email"""
        pass
    
    @abstractmethod
    def get_clients_by_city(self, city: str, company_id: str) -> List[Client]:
        """Obtiene clientes de una ciudad"""
        pass
    
    @abstractmethod
    def create_client(self, client: Client) -> Client:
        """Crea un nuevo cliente"""
        pass
    
    @abstractmethod
    def update_client(self, client_id: str, client: Client) -> Optional[Client]:
        """Actualiza un cliente"""
        pass
    
    @abstractmethod
    def delete_client(self, client_id: str, company_id: str) -> bool:
        """Elimina un cliente"""
        pass
