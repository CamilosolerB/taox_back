"""
Use cases para Ubicación
"""
from typing import List
from app.domain.ports.out.location_repository import LocationRepository
from app.domain.entities.location_model import Location
import logging

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    """Use case para crear una ubicación"""
    
    def __init__(self, location_repository: LocationRepository):
        self.location_repository = location_repository
    
    def execute(
        self,
        ubicacion: str,
        posicion: str,
        nivel: str,
        tipo_ubicacion: str,
        localizador: str,
        id_empresa: str
    ) -> Location:
        """Crea una nueva ubicación"""
        logger.info(f"Creando ubicación: {localizador}")
        
        location = Location(
            ubicacion=ubicacion,
            posicion=posicion,
            nivel=nivel,
            tipo_ubicacion=tipo_ubicacion,
            localizador=localizador,
            id_empresa=id_empresa
        )
        
        created = self.location_repository.create_location(location)
        logger.info(f"Ubicación creada: {localizador}")
        return created


class GetLocationsUseCase:
    """Use case para obtener ubicaciones"""
    
    def __init__(self, location_repository: LocationRepository):
        self.location_repository = location_repository
    
    def get_all(self, company_id: str) -> List[Location]:
        """Obtiene todas las ubicaciones"""
        logger.info(f"Obteniendo ubicaciones de empresa: {company_id}")
        return self.location_repository.get_all_locations(company_id)
    
    def get_by_id(self, location_id: int, company_id: str) -> Location:
        """Obtiene una ubicación por ID"""
        location = self.location_repository.get_location_by_id(location_id, company_id)
        if not location:
            raise Exception(f"Location {location_id} not found")
        return location
    
    def get_by_code(self, localizador: str, company_id: str) -> Location:
        """Obtiene una ubicación por código"""
        location = self.location_repository.get_location_by_code(localizador, company_id)
        if not location:
            raise Exception(f"Location with code {localizador} not found")
        return location


class UpdateLocationUseCase:
    """Use case para actualizar una ubicación"""
    
    def __init__(self, location_repository: LocationRepository):
        self.location_repository = location_repository
    
    def execute(self, location_id: int, location: Location) -> Location:
        """Actualiza una ubicación"""
        logger.info(f"Actualizando ubicación: {location_id}")
        updated = self.location_repository.update_location(location_id, location)
        if not updated:
            raise Exception(f"Could not update location {location_id}")
        return updated


class DeleteLocationUseCase:
    """Use case para eliminar una ubicación"""
    
    def __init__(self, location_repository: LocationRepository):
        self.location_repository = location_repository
    
    def execute(self, location_id: int, company_id: str) -> bool:
        """Elimina una ubicación"""
        logger.info(f"Eliminando ubicación: {location_id}")
        deleted = self.location_repository.delete_location(location_id, company_id)
        if not deleted:
            raise Exception(f"Could not delete location {location_id}")
        return True
