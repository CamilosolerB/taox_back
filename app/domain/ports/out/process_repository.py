"""
Puerto (Interfaz) de Repositorio para Process
"""
from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.process_model import Process
from typing import List


class ProcessRepository(ABC):
    """Interfaz para repositorio de procesos"""
    
    @abstractmethod
    def get_all_processes(self, company_id: str) -> List[Process]:
        """Obtiene todos los procesos de una empresa"""
        pass
    
    @abstractmethod
    def get_process_by_id(self, id_proceso: UUID, company_id: str) -> Process:
        """Obtiene un proceso por ID"""
        pass
    
    @abstractmethod
    def get_processes_by_type(self, tipo_proceso: str, company_id: str) -> List[Process]:
        """Obtiene procesos por tipo"""
        pass
    
    @abstractmethod
    def create_process(self, process: Process) -> Process:
        """Crea un nuevo proceso"""
        pass
    
    @abstractmethod
    def update_process(self, id_proceso: UUID, process_data: dict) -> Process:
        """Actualiza un proceso"""
        pass
    
    @abstractmethod
    def delete_process(self, id_proceso: UUID, company_id: str) -> bool:
        """Elimina un proceso"""
        pass
