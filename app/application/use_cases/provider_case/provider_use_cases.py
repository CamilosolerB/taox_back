"""
Use cases para consultas y actualizaciones de proveedores
"""
from typing import List
from app.domain.ports.out.provider_repository import ProviderRepository
from app.domain.entities.provider_model import Provider
import logging

logger = logging.getLogger(__name__)


class GetProvidersUseCase:
    """Use case para obtener proveedores"""
    
    def __init__(self, provider_repository: ProviderRepository):
        self.provider_repository = provider_repository
    
    def get_all(self, company_id: str) -> List[Provider]:
        """Obtiene todos los proveedores de una empresa"""
        logger.info(f"Obteniendo proveedores de empresa: {company_id}")
        return self.provider_repository.get_all_providers(company_id)
    
    def get_by_id(self, provider_id: str, company_id: str) -> Provider:
        """Obtiene un proveedor por ID"""
        logger.info(f"Obteniendo proveedor: {provider_id}")
        provider = self.provider_repository.get_provider_by_id(provider_id, company_id)
        if not provider:
            logger.warning(f"Proveedor no encontrado: {provider_id}")
            raise Exception(f"Provider with id {provider_id} not found")
        return provider
    
    def get_by_email(self, email: str, company_id: str) -> Provider:
        """Obtiene un proveedor por email"""
        logger.info(f"Obteniendo proveedor por email: {email}")
        provider = self.provider_repository.get_provider_by_email(email, company_id)
        if not provider:
            logger.warning(f"Proveedor no encontrado con email: {email}")
            raise Exception(f"Provider with email {email} not found")
        return provider


class UpdateProviderUseCase:
    """Use case para actualizar un proveedor"""
    
    def __init__(self, provider_repository: ProviderRepository):
        self.provider_repository = provider_repository
    
    def execute(self, provider_id: str, provider: Provider) -> Provider:
        """Actualiza un proveedor existente"""
        logger.info(f"Actualizando proveedor: {provider_id}")
        updated_provider = self.provider_repository.update_provider(provider_id, provider)
        if not updated_provider:
            logger.error(f"No se pudo actualizar proveedor: {provider_id}")
            raise Exception(f"Could not update provider {provider_id}")
        logger.info(f"Proveedor actualizado exitosamente: {provider_id}")
        return updated_provider


class DeleteProviderUseCase:
    """Use case para eliminar un proveedor"""
    
    def __init__(self, provider_repository: ProviderRepository):
        self.provider_repository = provider_repository
    
    def execute(self, provider_id: str, company_id: str) -> bool:
        """Elimina un proveedor"""
        logger.info(f"Eliminando proveedor: {provider_id}")
        deleted = self.provider_repository.delete_provider(provider_id, company_id)
        if not deleted:
            logger.error(f"No se pudo eliminar proveedor: {provider_id}")
            raise Exception(f"Could not delete provider {provider_id}")
        logger.info(f"Proveedor eliminado exitosamente: {provider_id}")
        return True
