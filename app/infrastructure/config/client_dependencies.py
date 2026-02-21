"""
Client dependencies configuration
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.client_repository_orm import ClientRepositoryORM
from app.application.use_cases.client_case.client_use_cases import (
    CreateClientUseCase,
    GetClientsUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase
)
from app.domain.ports.out.client_repository import ClientRepository


def get_client_repository(session: Session = Depends(get_session)) -> ClientRepository:
    return ClientRepositoryORM(session)


def get_create_client_use_case(client_repository: ClientRepository = Depends(get_client_repository)) -> CreateClientUseCase:
    return CreateClientUseCase(client_repository)


def get_clients_use_case(client_repository: ClientRepository = Depends(get_client_repository)) -> GetClientsUseCase:
    return GetClientsUseCase(client_repository)


def get_update_client_use_case(client_repository: ClientRepository = Depends(get_client_repository)) -> UpdateClientUseCase:
    return UpdateClientUseCase(client_repository)


def get_delete_client_use_case(client_repository: ClientRepository = Depends(get_client_repository)) -> DeleteClientUseCase:
    return DeleteClientUseCase(client_repository)
