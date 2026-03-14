"""
Use case para eliminar un proceso
"""
import logging
from uuid import UUID
from app.domain.ports.out.process_repository import ProcessRepository

logger = logging.getLogger(__name__)


class DeleteProcessUseCase:
    """Caso de uso para eliminar un proceso"""
    
    def __init__(self, process_repository: ProcessRepository):
        self.process_repository = process_repository
    
    def execute(self, id_proceso: str, company_id: str) -> bool:
        """
        Ejecuta el caso de uso
        
        Args:
            id_proceso: ID del proceso a eliminar
            company_id: ID de la empresa
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            ValueError: Si el proceso no existe
        """
        logger.info(f"Eliminando proceso {id_proceso} de la empresa {company_id}")
        result = self.process_repository.delete_process(id_proceso, company_id)
        
        if not result:
            logger.error(f"No se pudo eliminar el proceso {id_proceso}")
            raise ValueError(f"Proceso con ID {id_proceso} no existe")
        
        logger.info(f"Proceso {id_proceso} eliminado exitosamente")
        return result
