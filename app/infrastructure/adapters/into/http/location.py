"""
Endpoints para Ubicación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.application.dto.location_dto import LocationCreateDTO, LocationUpdateDTO, LocationDTO
from app.application.use_cases.location_case.location_use_cases import (
    CreateLocationUseCase,
    GetLocationsUseCase,
    UpdateLocationUseCase,
    DeleteLocationUseCase
)
from app.infrastructure.config.location_dependencies import (
    get_create_location_use_case,
    get_locations_use_case,
    get_update_location_use_case,
    get_delete_location_use_case
)
from app.core.middleware.auth_middleware import get_current_user, require_admin
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=List[LocationDTO])
def get_locations(
    company_id: UUID,
    get_locations_use_case: GetLocationsUseCase = Depends(get_locations_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todas las ubicaciones"""
    try:
        return get_locations_use_case.get_all(str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{location_id}", response_model=LocationDTO)
def get_location(
    location_id: int,
    company_id: UUID,
    get_locations_use_case: GetLocationsUseCase = Depends(get_locations_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene una ubicación específica"""
    try:
        return get_locations_use_case.get_by_id(location_id, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=LocationDTO, status_code=status.HTTP_201_CREATED)
def create_location(
    location_dto: LocationCreateDTO,
    create_location_use_case: CreateLocationUseCase = Depends(get_create_location_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Crea una nueva ubicación"""
    logger.info(f"Creando ubicación: {location_dto.localizador}")
    try:
        return create_location_use_case.execute(
            ubicacion=location_dto.ubicacion,
            posicion=location_dto.posicion,
            nivel=location_dto.nivel,
            tipo_ubicacion=location_dto.tipo_ubicacion,
            localizador=location_dto.localizador,
            id_empresa=str(location_dto.company_id)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{location_id}", response_model=LocationDTO)
def update_location(
    location_id: int,
    location_dto: LocationUpdateDTO,
    update_location_use_case: UpdateLocationUseCase = Depends(get_update_location_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Actualiza una ubicación"""
    logger.info(f"Actualizando ubicación: {location_id}")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    location_id: int,
    company_id: UUID,
    delete_location_use_case: DeleteLocationUseCase = Depends(get_delete_location_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Elimina una ubicación"""
    logger.info(f"Eliminando ubicación: {location_id}")
    try:
        delete_location_use_case.execute(location_id, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
