"""
HTTP endpoints para Product Movement
"""
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.application.dto.product_movement_dto import ProductMovementCreateDTO, ProductMovementUpdateDTO, ProductMovementResponseDTO
from app.application.use_cases.product_movement_case import (
    GetAllMovementsUseCase,
    GetMovementByIdUseCase,
    CreateMovementUseCase,
    UpdateMovementUseCase,
    UpdateMovementStatusUseCase,
    DeleteMovementUseCase
)
from app.infrastructure.config.product_movement_dependencies import (
    get_get_all_movements_use_case,
    get_get_movement_by_id_use_case,
    get_create_movement_use_case,
    get_update_movement_use_case,
    get_update_movement_status_use_case,
    get_delete_movement_use_case
)

router = APIRouter(prefix="/movements", tags=["movements"])


def _movement_to_response_dto(movement):
    """Convierte ProductMovement entity a ProductMovementResponseDTO"""
    return ProductMovementResponseDTO(
        id_movimiento=movement.id_movimiento,
        codigo_producto=movement.codigo_producto,
        id_proceso_origen=str(movement.id_proceso_origen),
        id_proceso_destino=str(movement.id_proceso_destino),
        cantidad=movement.cantidad,
        notas=movement.notas,
        id_empresa=str(movement.id_empresa),
        estado=movement.estado,
        created_at=movement.created_at,
        updated_at=movement.updated_at
    )


@router.get("/", response_model=List[ProductMovementResponseDTO], status_code=status.HTTP_200_OK)
def get_all_movements(
    company_id: str,
    use_case: GetAllMovementsUseCase = Depends(get_get_all_movements_use_case)
):
    """Obtiene todos los movimientos de una empresa"""
    movements = use_case.execute(company_id)
    return [_movement_to_response_dto(m) for m in movements]


@router.get("/{id_movimiento}", response_model=ProductMovementResponseDTO, status_code=status.HTTP_200_OK)
def get_movement_by_id(
    id_movimiento: int,
    company_id: str,
    use_case: GetMovementByIdUseCase = Depends(get_get_movement_by_id_use_case)
):
    """Obtiene un movimiento por ID"""
    try:
        movement = use_case.execute(id_movimiento, company_id)
        return _movement_to_response_dto(movement)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ProductMovementResponseDTO, status_code=status.HTTP_201_CREATED)
def create_movement(
    movement_dto: ProductMovementCreateDTO,
    use_case: CreateMovementUseCase = Depends(get_create_movement_use_case)
):
    """Crea un nuevo movimiento. Automáticamente genera alertas si hay cambios de stock crítico"""
    movement = use_case.execute(movement_dto)
    return _movement_to_response_dto(movement)


@router.put("/{id_movimiento}", response_model=ProductMovementResponseDTO, status_code=status.HTTP_200_OK)
def update_movement(
    id_movimiento: int,
    movement_dto: ProductMovementUpdateDTO,
    use_case: UpdateMovementUseCase = Depends(get_update_movement_use_case)
):
    """Actualiza un movimiento"""
    try:
        movement = use_case.execute(id_movimiento, movement_dto)
        return _movement_to_response_dto(movement)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{id_movimiento}/status", response_model=ProductMovementResponseDTO, status_code=status.HTTP_200_OK)
def update_movement_status(
    id_movimiento: int,
    nuevo_estado: str,
    use_case: UpdateMovementStatusUseCase = Depends(get_update_movement_status_use_case)
):
    """Actualiza el estado de un movimiento"""
    try:
        movement = use_case.execute(id_movimiento, nuevo_estado)
        return _movement_to_response_dto(movement)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_movimiento}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movement(
    id_movimiento: int,
    company_id: str,
    use_case: DeleteMovementUseCase = Depends(get_delete_movement_use_case)
):
    """Elimina un movimiento"""
    try:
        use_case.execute(id_movimiento, company_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
