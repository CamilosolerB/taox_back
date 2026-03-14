"""
Use case para obtener un proceso por ID
"""
import logging
from uuid import UUID
from app.domain.entities.process_model import Process
from app.domain.ports.out.process_repository import ProcessRepository

logger = logging.getLogger(__name__)


class GetProcessByIdUseCase:
    """Caso de uso para obtener un proceso por ID"""
    
    def __init__(self, process_repository: ProcessRepository):
        self.process_repository = process_repository
    
    def execute(self, id_proceso: str, company_id: str) -> Process:
        """
        Ejecuta el caso de uso
        
        Args:
            id_proceso: ID del proceso
            company_id: ID de la empresa
            
        Returns:
            Proceso encontrado
            
        Raises:
            ValueError: Si el proceso no existe
        """
        logger.info(f"Obteniendo proceso {id_proceso} de la empresa {company_id}")
        process = self.process_repository.get_process_by_id(id_proceso, company_id)
        if not process:
            logger.error(f"Proceso {id_proceso} no encontrado")
            raise ValueError(f"Proceso con ID {id_proceso} no existe")
        return process
