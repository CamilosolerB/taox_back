"""
Use case para actualizar un proceso
"""
import logging
from uuid import UUID
from app.domain.entities.process_model import Process
from app.domain.ports.out.process_repository import ProcessRepository
from app.application.dto.process_dto import ProcessUpdateDTO

logger = logging.getLogger(__name__)


class UpdateProcessUseCase:
    """Caso de uso para actualizar un proceso"""
    
    def __init__(self, process_repository: ProcessRepository):
        self.process_repository = process_repository
    
    def execute(self, id_proceso: str, process_dto: ProcessUpdateDTO) -> Process:
        """
        Ejecuta el caso de uso
        
        Args:
            id_proceso: ID del proceso a actualizar
            process_dto: DTO con los datos a actualizar
            
        Returns:
            Proceso actualizado
            
        Raises:
            ValueError: Si el proceso no existe
        """
        logger.info(f"Actualizando proceso {id_proceso}")
        
        # Preparar datos para actualizar (solo campos no None)
        update_data = process_dto.model_dump(exclude_unset=True)
        
        if not update_data:
            logger.warning(f"No hay campos para actualizar en proceso {id_proceso}")
            raise ValueError("Se debe proporcionar al menos un campo para actualizar")
        
        updated_process = self.process_repository.update_process(id_proceso, update_data)
        logger.info(f"Proceso {id_proceso} actualizado exitosamente")
        return updated_process
