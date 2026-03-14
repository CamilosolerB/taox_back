"""
Use case para crear un nuevo proceso
"""
import logging
from app.domain.entities.process_model import Process
from app.domain.ports.out.process_repository import ProcessRepository
from app.application.dto.process_dto import ProcessCreateDTO

logger = logging.getLogger(__name__)


class CreateProcessUseCase:
    """Caso de uso para crear un nuevo proceso"""
    
    def __init__(self, process_repository: ProcessRepository):
        self.process_repository = process_repository
    
    def execute(self, process_dto: ProcessCreateDTO) -> Process:
        """
        Ejecuta el caso de uso
        
        Args:
            process_dto: DTO con los datos del proceso
            
        Returns:
            Proceso creado
        """
        logger.info(f"Creando nuevo proceso: {process_dto.nombre}")
        
        process = Process(
            nombre=process_dto.nombre,
            descripcion=process_dto.descripcion,
            tipo_proceso=process_dto.tipo_proceso,
            id_empresa=process_dto.id_empresa,
            is_active=True
        )
        
        created_process = self.process_repository.create_process(process)
        logger.info(f"Proceso creado exitosamente con ID {created_process.id_proceso}")
        return created_process
