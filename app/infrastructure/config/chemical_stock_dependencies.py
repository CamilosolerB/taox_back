"""
Configuración de dependencias para Chemical Stock
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.chemical_stock_repository_orm import ChemicalStockORMRepository
from app.application.use_cases.chemical_stock_case import (
    GetAllStocksUseCase,
    GetStockByIdUseCase,
    GetCriticalStocksUseCase,
    CreateStockUseCase,
    UpdateStockUseCase,
    DeleteStockUseCase
)
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository


def get_stock_repository(session: Session = Depends(get_session)) -> ChemicalStockRepository:
    """Inyecta el repositorio de stock químico"""
    return ChemicalStockORMRepository(session)


def get_get_all_stocks_use_case(
    repository: ChemicalStockRepository = Depends(get_stock_repository)
) -> GetAllStocksUseCase:
    """Inyecta el caso de uso para obtener todos los stocks"""
    return GetAllStocksUseCase(repository)


def get_get_stock_by_id_use_case(
    repository: ChemicalStockRepository = Depends(get_stock_repository)
) -> GetStockByIdUseCase:
    """Inyecta el caso de uso para obtener un stock por ID"""
    return GetStockByIdUseCase(repository)


def get_get_critical_stocks_use_case(
    repository: ChemicalStockRepository = Depends(get_stock_repository)
) -> GetCriticalStocksUseCase:
    """Inyecta el caso de uso para obtener stocks críticos"""
    return GetCriticalStocksUseCase(repository)


def get_create_stock_use_case(
    repository: ChemicalStockRepository = Depends(get_stock_repository)
) -> CreateStockUseCase:
    """Inyecta el caso de uso para crear un stock"""
    return CreateStockUseCase(repository)


def get_update_stock_use_case(
    repository: ChemicalStockRepository = Depends(get_stock_repository)
) -> UpdateStockUseCase:
    """Inyecta el caso de uso para actualizar un stock"""
    return UpdateStockUseCase(repository)


def get_delete_stock_use_case(
    repository: ChemicalStockRepository = Depends(get_stock_repository)
) -> DeleteStockUseCase:
    """Inyecta el caso de uso para eliminar un stock"""
    return DeleteStockUseCase(repository)
