"""
HTTP endpoints para Almacenes
"""
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from uuid import UUID
from app.core.middleware.auth_middleware import get_current_user, require_company_admin
from app.application.dto.process_dto import ProcessCreateDTO, ProcessUpdateDTO, ProcessResponseDTO
from app.application.use_cases.process_case import (
    GetAllProcessesUseCase,
    GetProcessByIdUseCase,
    CreateProcessUseCase,
    UpdateProcessUseCase,
    DeleteProcessUseCase
)
from pydantic import BaseModel
from app.infrastructure.config.process_dependencies import (
    get_get_all_processes_use_case,
    get_get_process_by_id_use_case,
    get_create_process_use_case,
    get_update_process_use_case,
    get_delete_process_use_case
)

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


class WarehouseCreateRequest(BaseModel):
    nombre: str
    descripcion: str | None = None


class WarehouseUpdateRequest(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None

def _process_to_warehouse_dto(process):
    """Convierte Process entity a ProcessResponseDTO (como almacen)"""
    return ProcessResponseDTO(
        id_proceso=str(process.id_proceso),
        nombre=process.nombre,
        descripcion=process.descripcion,
        tipo_proceso=process.tipo_proceso,
        id_empresa=str(process.id_empresa),
        is_active=process.is_active,
        created_at=process.created_at,
        updated_at=process.updated_at
    )


def _is_warehouse(process):
    return process.tipo_proceso == 'almacenamiento'


@router.get("/", response_model=List[ProcessResponseDTO], status_code=status.HTTP_200_OK)
def get_warehouses(
    payload: dict = Depends(get_current_user),
    use_case: GetAllProcessesUseCase = Depends(get_get_all_processes_use_case)
):
    """Obtiene todos los almacenes de la empresa del usuario"""
    company_id = payload.get("company_id")
    processes = use_case.execute(company_id)
    warehouses = [p for p in processes if _is_warehouse(p)]
    return [_process_to_warehouse_dto(p) for p in warehouses]


@router.get("/{warehouse_id}", response_model=ProcessResponseDTO, status_code=status.HTTP_200_OK)
def get_warehouse(
    warehouse_id: str,
    payload: dict = Depends(get_current_user),
    use_case: GetProcessByIdUseCase = Depends(get_get_process_by_id_use_case)
):
    """Obtiene un almacen por ID"""
    company_id = payload.get("company_id")
    try:
        process = use_case.execute(warehouse_id, company_id)
        if not _is_warehouse(process):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Almacen no encontrado")
        return _process_to_warehouse_dto(process)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ProcessResponseDTO, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    warehouse_req: WarehouseCreateRequest,
    payload: dict = Depends(require_company_admin()),
    use_case: CreateProcessUseCase = Depends(get_create_process_use_case)
):
    """Crea un nuevo almacen (tipo='almacenamiento')"""
    company_id = payload.get("company_id")
    
    warehouse_data = ProcessCreateDTO(
        nombre=warehouse_req.nombre,
        descripcion=warehouse_req.descripcion,
        tipo_proceso="almacenamiento",
        id_empresa=company_id
    )
    
    warehouse = use_case.execute(warehouse_data)
    return _process_to_warehouse_dto(warehouse)


@router.put("/{warehouse_id}", response_model=ProcessResponseDTO, status_code=status.HTTP_200_OK)
def update_warehouse(
    warehouse_id: str,
    warehouse_req: WarehouseUpdateRequest,
    payload: dict = Depends(require_company_admin()),
    use_case: UpdateProcessUseCase = Depends(get_update_process_use_case)
):
    """Actualiza un almacen"""
    company_id = payload.get("company_id")
    
    try:
        existing = use_case.execute(warehouse_id, company_id)
        if not _is_warehouse(existing):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Almacen no encontrado")
        
        warehouse_dto = ProcessUpdateDTO(
            nombre=warehouse_req.nombre,
            descripcion=warehouse_req.descripcion
        )
        updated = use_case.execute(warehouse_id, warehouse_dto)
        return _process_to_warehouse_dto(updated)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(
    warehouse_id: str,
    payload: dict = Depends(require_company_admin()),
    use_case: DeleteProcessUseCase = Depends(get_delete_process_use_case)
):
    """Elimina (desactiva) un almacen"""
    company_id = payload.get("company_id")
    
    try:
        existing_use_case = GetProcessByIdUseCase(None)
        existing = existing_use_case.execute(warehouse_id, company_id)
        if not _is_warehouse(existing):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Almacen no encontrado")
        
        use_case.execute(warehouse_id, company_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))