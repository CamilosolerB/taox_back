"""
Endpoints para Cliente
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.application.dto.client_dto import ClientCreateDTO, ClientUpdateDTO, ClientDTO
from app.application.use_cases.client_case.client_use_cases import (
    CreateClientUseCase,
    GetClientsUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase
)
from app.infrastructure.config.client_dependencies import (
    get_create_client_use_case,
    get_clients_use_case,
    get_update_client_use_case,
    get_delete_client_use_case
)
from app.core.middleware.auth_middleware import get_current_user, require_admin
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=List[ClientDTO])
def get_clients(
    company_id: UUID,
    get_clients_use_case: GetClientsUseCase = Depends(get_clients_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todos los clientes"""
    try:
        return get_clients_use_case.get_all(str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{client_id}", response_model=ClientDTO)
def get_client(
    client_id: str,
    company_id: UUID,
    get_clients_use_case: GetClientsUseCase = Depends(get_clients_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene un cliente específico"""
    try:
        return get_clients_use_case.get_by_id(client_id, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/city/{city}", response_model=List[ClientDTO])
def get_clients_by_city(
    city: str,
    company_id: UUID,
    get_clients_use_case: GetClientsUseCase = Depends(get_clients_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todos los clientes de una ciudad"""
    try:
        return get_clients_use_case.get_by_city(city, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("", response_model=ClientDTO, status_code=status.HTTP_201_CREATED)
def create_client(
    client_dto: ClientCreateDTO,
    create_client_use_case: CreateClientUseCase = Depends(get_create_client_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Crea un nuevo cliente"""
    logger.info(f"Creando cliente: {client_dto.cliente}")
    try:
        return create_client_use_case.execute(
            codigo_cliente=client_dto.codigo_cliente,
            cliente=client_dto.cliente,
            telefono1=client_dto.telefono1,
            telefono2=client_dto.telefono2,
            contacto=client_dto.contacto,
            correo=client_dto.correo,
            ciudad=client_dto.ciudad,
            tipo_agua=client_dto.tipo_agua,
            cantidad_promedio_kg=client_dto.cantidad_promedio_kg,
            id_empresa=str(client_dto.company_id)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{client_id}", response_model=ClientDTO)
def update_client(
    client_id: str,
    client_dto: ClientUpdateDTO,
    update_client_use_case: UpdateClientUseCase = Depends(get_update_client_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Actualiza un cliente"""
    logger.info(f"Actualizando cliente: {client_id}")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: str,
    company_id: UUID,
    delete_client_use_case: DeleteClientUseCase = Depends(get_delete_client_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Elimina un cliente"""
    logger.info(f"Eliminando cliente: {client_id}")
    try:
        delete_client_use_case.execute(client_id, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
