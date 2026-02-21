"""
Use case para crear un proveedor
"""
from app.domain.ports.out.provider_repository import ProviderRepository
from app.domain.entities.provider_model import Provider
import logging

logger = logging.getLogger(__name__)


class CreateProviderUseCase:
    """Use case para crear un nuevo proveedor"""
    
    def __init__(self, provider_repository: ProviderRepository):
        self.provider_repository = provider_repository
    
    def execute(
        self,
        cad_proveedor: str,
        nombre: str,
        contacto: str,
        direccion: str,
        telefono: str,
        celular: str,
        web: str,
        correo: str,
        id_empresa: str
    ) -> Provider:
        """
        Crea un nuevo proveedor
        
        Args:
            cad_proveedor: Código único del proveedor
            nombre: Nombre del proveedor
            contacto: Persona de contacto
            direccion: Dirección
            telefono: Teléfono
            celular: Celular
            web: Sitio web (opcional)
            correo: Email
            id_empresa: UUID de la empresa
            
        Returns:
            Proveedor creado
        """
        logger.info(f"Creando proveedor: {cad_proveedor}")
        
        provider = Provider(
            cad_proveedor=cad_proveedor,
            nombre=nombre,
            contacto=contacto,
            direccion=direccion,
            telefono=telefono,
            celular=celular,
            web=web,
            correo=correo,
            id_empresa=id_empresa
        )
        
        created_provider = self.provider_repository.create_provider(provider)
        logger.info(f"Proveedor creado exitosamente: {cad_proveedor}")
        
        return created_provider
