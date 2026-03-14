"""
Configuración de dependencias para Process
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.process_repository_orm import ProcessORMRepository
from app.application.use_cases.process_case import (
    GetAllProcessesUseCase,
    GetProcessByIdUseCase,
    CreateProcessUseCase,
    UpdateProcessUseCase,
    DeleteProcessUseCase
)
from app.domain.ports.out.process_repository import ProcessRepository


def get_process_repository(session: Session = Depends(get_session)) -> ProcessRepository:
    """Inyecta el repositorio de procesos"""
    return ProcessORMRepository(session)


def get_get_all_processes_use_case(
    repository: ProcessRepository = Depends(get_process_repository)
) -> GetAllProcessesUseCase:
    """Inyecta el caso de uso para obtener todos los procesos"""
    return GetAllProcessesUseCase(repository)


def get_get_process_by_id_use_case(
    repository: ProcessRepository = Depends(get_process_repository)
) -> GetProcessByIdUseCase:
    """Inyecta el caso de uso para obtener un proceso por ID"""
    return GetProcessByIdUseCase(repository)


def get_create_process_use_case(
    repository: ProcessRepository = Depends(get_process_repository)
) -> CreateProcessUseCase:
    """Inyecta el caso de uso para crear un proceso"""
    return CreateProcessUseCase(repository)


def get_update_process_use_case(
    repository: ProcessRepository = Depends(get_process_repository)
) -> UpdateProcessUseCase:
    """Inyecta el caso de uso para actualizar un proceso"""
    return UpdateProcessUseCase(repository)


def get_delete_process_use_case(
    repository: ProcessRepository = Depends(get_process_repository)
) -> DeleteProcessUseCase:
    """Inyecta el caso de uso para eliminar un proceso"""
    return DeleteProcessUseCase(repository)
