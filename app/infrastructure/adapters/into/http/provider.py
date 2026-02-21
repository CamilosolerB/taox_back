"""
Endpoints para Proveedor
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.application.dto.provider_dto import ProviderCreateDTO, ProviderUpdateDTO, ProviderDTO
from app.application.use_cases.provider_case.create_provider import CreateProviderUseCase
from app.application.use_cases.provider_case.provider_use_cases import (
    GetProvidersUseCase,
    UpdateProviderUseCase,
    DeleteProviderUseCase
)
from app.infrastructure.config.provider_dependencies import (
    get_create_provider_use_case,
    get_providers_use_case,
    get_update_provider_use_case,
    get_delete_provider_use_case
)
from app.core.middleware.auth_middleware import get_current_user, require_admin
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=List[ProviderDTO])
def get_providers(
    company_id: UUID,
    get_providers_use_case: GetProvidersUseCase = Depends(get_providers_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todos los proveedores de una empresa"""
    logger.info(f"Obteniendo proveedores de empresa: {company_id}")
    return get_providers_use_case.get_all(str(company_id))


@router.get("/{provider_id}", response_model=ProviderDTO)
def get_provider(
    provider_id: str,
    company_id: UUID,
    get_providers_use_case: GetProvidersUseCase = Depends(get_providers_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene un proveedor específico"""
    logger.info(f"Obteniendo proveedor: {provider_id}")
    try:
        return get_providers_use_case.get_by_id(provider_id, str(company_id))
    except Exception as e:
        logger.error(f"Error obteniendo proveedor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("", response_model=ProviderDTO, status_code=status.HTTP_201_CREATED)
def create_provider(
    provider_dto: ProviderCreateDTO,
    create_provider_use_case: CreateProviderUseCase = Depends(get_create_provider_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Crea un nuevo proveedor"""
    logger.info(f"Creando proveedor: {provider_dto.cad_proveedor}")
    try:
        return create_provider_use_case.execute(
            cad_proveedor=provider_dto.cad_proveedor,
            nombre=provider_dto.nombre,
            contacto=provider_dto.contacto,
            direccion=provider_dto.direccion,
            telefono=provider_dto.telefono,
            celular=provider_dto.celular,
            web=provider_dto.web or "",
            correo=provider_dto.correo,
            id_empresa=str(provider_dto.company_id)
        )
    except Exception as e:
        logger.error(f"Error creando proveedor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{provider_id}", response_model=ProviderDTO)
def update_provider(
    provider_id: str,
    provider_dto: ProviderUpdateDTO,
    company_id: UUID,
    update_provider_use_case: UpdateProviderUseCase = Depends(get_update_provider_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Actualiza un proveedor"""
    logger.info(f"Actualizando proveedor: {provider_id}")
    try:
        return update_provider_use_case.execute(
            provider_id=provider_id,
            id_empresa=str(company_id),
            nombre=provider_dto.nombre,
            contacto=provider_dto.contacto,
            direccion=provider_dto.direccion,
            telefono=provider_dto.telefono,
            celular=provider_dto.celular,
            web=provider_dto.web,
            correo=provider_dto.correo,
            is_active=provider_dto.is_active
        )
    except Exception as e:
        logger.error(f"Error actualizando proveedor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider(
    provider_id: str,
    company_id: UUID,
    delete_provider_use_case: DeleteProviderUseCase = Depends(get_delete_provider_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Elimina un proveedor"""
    logger.info(f"Eliminando proveedor: {provider_id}")
    try:
        delete_provider_use_case.execute(provider_id, str(company_id))
    except Exception as e:
        logger.error(f"Error eliminando proveedor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
