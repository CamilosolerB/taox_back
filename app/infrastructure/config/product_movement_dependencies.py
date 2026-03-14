"""
Configuración de dependencias para Product Movement
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.product_movement_repository_orm import ProductMovementORMRepository
from app.infrastructure.adapters.out.chemical_stock_repository_orm import ChemicalStockORMRepository
from app.infrastructure.adapters.out.stock_alert_repository_orm import StockAlertORMRepository
from app.application.use_cases.product_movement_case import (
    GetAllMovementsUseCase,
    GetMovementByIdUseCase,
    CreateMovementUseCase,
    UpdateMovementUseCase,
    UpdateMovementStatusUseCase,
    DeleteMovementUseCase
)
from app.domain.ports.out.product_movement_repository import ProductMovementRepository
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository
from app.domain.ports.out.stock_alert_repository import StockAlertRepository


def get_movement_repository(session: Session = Depends(get_session)) -> ProductMovementRepository:
    """Inyecta el repositorio de movimientos"""
    return ProductMovementORMRepository(session)


def get_chemical_stock_repository(session: Session = Depends(get_session)) -> ChemicalStockRepository:
    """Inyecta el repositorio de stock químico"""
    return ChemicalStockORMRepository(session)


def get_stock_alert_repository(session: Session = Depends(get_session)) -> StockAlertRepository:
    """Inyecta el repositorio de alertas de stock"""
    return StockAlertORMRepository(session)


def get_get_all_movements_use_case(
    repository: ProductMovementRepository = Depends(get_movement_repository)
) -> GetAllMovementsUseCase:
    """Inyecta el caso de uso para obtener todos los movimientos"""
    return GetAllMovementsUseCase(repository)


def get_get_movement_by_id_use_case(
    repository: ProductMovementRepository = Depends(get_movement_repository)
) -> GetMovementByIdUseCase:
    """Inyecta el caso de uso para obtener un movimiento por ID"""
    return GetMovementByIdUseCase(repository)


def get_create_movement_use_case(
    movement_repository: ProductMovementRepository = Depends(get_movement_repository),
    stock_repository: ChemicalStockRepository = Depends(get_chemical_stock_repository),
    alert_repository: StockAlertRepository = Depends(get_stock_alert_repository)
) -> CreateMovementUseCase:
    """Inyecta el caso de uso para crear un movimiento con lógica de alertas"""
    return CreateMovementUseCase(movement_repository, stock_repository, alert_repository)


def get_update_movement_use_case(
    repository: ProductMovementRepository = Depends(get_movement_repository)
) -> UpdateMovementUseCase:
    """Inyecta el caso de uso para actualizar un movimiento"""
    return UpdateMovementUseCase(repository)


def get_update_movement_status_use_case(
    repository: ProductMovementRepository = Depends(get_movement_repository)
) -> UpdateMovementStatusUseCase:
    """Inyecta el caso de uso para actualizar el estado de un movimiento"""
    return UpdateMovementStatusUseCase(repository)


def get_delete_movement_use_case(
    repository: ProductMovementRepository = Depends(get_movement_repository)
) -> DeleteMovementUseCase:
    """Inyecta el caso de uso para eliminar un movimiento"""
    return DeleteMovementUseCase(repository)
