"""
HTTP endpoints para Process
"""
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.application.dto.process_dto import ProcessCreateDTO, ProcessUpdateDTO, ProcessResponseDTO
from app.application.use_cases.process_case import (
    GetAllProcessesUseCase,
    GetProcessByIdUseCase,
    CreateProcessUseCase,
    UpdateProcessUseCase,
    DeleteProcessUseCase
)
from app.infrastructure.config.process_dependencies import (
    get_get_all_processes_use_case,
    get_get_process_by_id_use_case,
    get_create_process_use_case,
    get_update_process_use_case,
    get_delete_process_use_case
)

router = APIRouter(prefix="/processes", tags=["processes"])


def _process_to_response_dto(process):
    """Convierte Process entity a ProcessResponseDTO"""
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


@router.get("/", response_model=List[ProcessResponseDTO], status_code=status.HTTP_200_OK)
def get_all_processes(
    company_id: str,
    use_case: GetAllProcessesUseCase = Depends(get_get_all_processes_use_case)
):
    """Obtiene todos los procesos de una empresa"""
    processes = use_case.execute(company_id)
    return [_process_to_response_dto(p) for p in processes]


@router.get("/{id_proceso}", response_model=ProcessResponseDTO, status_code=status.HTTP_200_OK)
def get_process_by_id(
    id_proceso: str,
    company_id: str,
    use_case: GetProcessByIdUseCase = Depends(get_get_process_by_id_use_case)
):
    """Obtiene un proceso por ID"""
    try:
        process = use_case.execute(id_proceso, company_id)
        return _process_to_response_dto(process)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ProcessResponseDTO, status_code=status.HTTP_201_CREATED)
def create_process(
    process_dto: ProcessCreateDTO,
    use_case: CreateProcessUseCase = Depends(get_create_process_use_case)
):
    """Crea un nuevo proceso"""
    process = use_case.execute(process_dto)
    return _process_to_response_dto(process)


@router.put("/{id_proceso}", response_model=ProcessResponseDTO, status_code=status.HTTP_200_OK)
def update_process(
    id_proceso: str,
    process_dto: ProcessUpdateDTO,
    use_case: UpdateProcessUseCase = Depends(get_update_process_use_case)
):
    """Actualiza un proceso"""
    try:
        process = use_case.execute(id_proceso, process_dto)
        return _process_to_response_dto(process)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_proceso}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process(
    id_proceso: str,
    company_id: str,
    use_case: DeleteProcessUseCase = Depends(get_delete_process_use_case)
):
    """Elimina un proceso"""
    try:
        use_case.execute(id_proceso, company_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
