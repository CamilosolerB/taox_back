"""
Use cases para Cliente
"""
from typing import List
from app.domain.ports.out.client_repository import ClientRepository
from app.domain.entities.client_model import Client
import logging

logger = logging.getLogger(__name__)


class CreateClientUseCase:
    """Use case para crear cliente"""
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def execute(
        self,
        codigo_cliente: str,
        cliente: str,
        telefono1: str,
        telefono2: str,
        contacto: str,
        correo: str,
        ciudad: str,
        tipo_agua: str,
        cantidad_promedio_kg: float,
        id_empresa: str
    ) -> Client:
        """Crea un nuevo cliente"""
        logger.info(f"Creando cliente: {codigo_cliente}")
        
        client = Client(
            codigo_cliente=codigo_cliente,
            cliente=cliente,
            telefono1=telefono1,
            telefono2=telefono2,
            contacto=contacto,
            correo=correo,
            ciudad=ciudad,
            tipo_agua=tipo_agua,
            cantidad_promedio_kg=cantidad_promedio_kg,
            id_empresa=id_empresa
        )
        
        created = self.client_repository.create_client(client)
        logger.info(f"Cliente creado: {codigo_cliente}")
        return created


class GetClientsUseCase:
    """Use case para obtener clientes"""
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def get_all(self, company_id: str) -> List[Client]:
        """Obtiene todos los clientes"""
        logger.info(f"Obteniendo clientes de empresa: {company_id}")
        return self.client_repository.get_all_clients(company_id)
    
    def get_by_id(self, client_id: str, company_id: str) -> Client:
        """Obtiene un cliente por ID"""
        client = self.client_repository.get_client_by_id(client_id, company_id)
        if not client:
            raise Exception(f"Client {client_id} not found")
        return client
    
    def get_by_email(self, email: str, company_id: str) -> Client:
        """Obtiene un cliente por email"""
        client = self.client_repository.get_client_by_email(email, company_id)
        if not client:
            raise Exception(f"Client with email {email} not found")
        return client
    
    def get_by_city(self, city: str, company_id: str) -> List[Client]:
        """Obtiene clientes de una ciudad"""
        return self.client_repository.get_clients_by_city(city, company_id)


class UpdateClientUseCase:
    """Use case para actualizar cliente"""
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def execute(self, client_id: str, client: Client) -> Client:
        """Actualiza un cliente"""
        logger.info(f"Actualizando cliente: {client_id}")
        updated = self.client_repository.update_client(client_id, client)
        if not updated:
            raise Exception(f"Could not update client {client_id}")
        return updated


class DeleteClientUseCase:
    """Use case para eliminar cliente"""
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def execute(self, client_id: str, company_id: str) -> bool:
        """Elimina un cliente"""
        logger.info(f"Eliminando cliente: {client_id}")
        deleted = self.client_repository.delete_client(client_id, company_id)
        if not deleted:
            raise Exception(f"Could not delete client {client_id}")
        return True
