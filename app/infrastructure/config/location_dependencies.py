"""
Location dependencies configuration
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.location_repository_orm import LocationRepositoryORM
from app.application.use_cases.location_case.location_use_cases import (
    CreateLocationUseCase,
    GetLocationsUseCase,
    UpdateLocationUseCase,
    DeleteLocationUseCase
)
from app.domain.ports.out.location_repository import LocationRepository


def get_location_repository(session: Session = Depends(get_session)) -> LocationRepository:
    return LocationRepositoryORM(session)


def get_create_location_use_case(location_repository: LocationRepository = Depends(get_location_repository)) -> CreateLocationUseCase:
    return CreateLocationUseCase(location_repository)


def get_locations_use_case(location_repository: LocationRepository = Depends(get_location_repository)) -> GetLocationsUseCase:
    return GetLocationsUseCase(location_repository)


def get_update_location_use_case(location_repository: LocationRepository = Depends(get_location_repository)) -> UpdateLocationUseCase:
    return UpdateLocationUseCase(location_repository)


def get_delete_location_use_case(location_repository: LocationRepository = Depends(get_location_repository)) -> DeleteLocationUseCase:
    return DeleteLocationUseCase(location_repository)
