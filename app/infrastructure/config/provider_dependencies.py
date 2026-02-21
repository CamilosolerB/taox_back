"""
Provider dependencies configuration
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.provider_repository_orm import ProviderRepositoryORM
from app.application.use_cases.provider_case.create_provider import CreateProviderUseCase
from app.application.use_cases.provider_case.provider_use_cases import (
    GetProvidersUseCase,
    UpdateProviderUseCase,
    DeleteProviderUseCase
)
from app.domain.ports.out.provider_repository import ProviderRepository


def get_provider_repository(session: Session = Depends(get_session)) -> ProviderRepository:
    return ProviderRepositoryORM(session)


def get_create_provider_use_case(provider_repository: ProviderRepository = Depends(get_provider_repository)) -> CreateProviderUseCase:
    return CreateProviderUseCase(provider_repository)


def get_providers_use_case(provider_repository: ProviderRepository = Depends(get_provider_repository)) -> GetProvidersUseCase:
    return GetProvidersUseCase(provider_repository)


def get_update_provider_use_case(provider_repository: ProviderRepository = Depends(get_provider_repository)) -> UpdateProviderUseCase:
    return UpdateProviderUseCase(provider_repository)


def get_delete_provider_use_case(provider_repository: ProviderRepository = Depends(get_provider_repository)) -> DeleteProviderUseCase:
    return DeleteProviderUseCase(provider_repository)
