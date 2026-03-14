"""
Use case para obtener todos los procesos
"""
import logging
from typing import List
from app.domain.entities.process_model import Process
from app.domain.ports.out.process_repository import ProcessRepository

logger = logging.getLogger(__name__)


class GetAllProcessesUseCase:
    """Caso de uso para obtener todos los procesos de una empresa"""
    
    def __init__(self, process_repository: ProcessRepository):
        self.process_repository = process_repository
    
    def execute(self, company_id: str) -> List[Process]:
        """
        Ejecuta el caso de uso
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de procesos
        """
        logger.info(f"Obteniendo todos los procesos para la empresa {company_id}")
        processes = self.process_repository.get_all_processes(company_id)
        logger.info(f"Se encontraron {len(processes)} procesos")
        return processes
