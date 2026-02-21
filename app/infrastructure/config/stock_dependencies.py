"""
Stock dependencies configuration
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.stock_repository_orm import StockLocationRepositoryORM, StockWarehouseRepositoryORM
from app.application.use_cases.stock_case.stock_use_cases import (
    CreateStockLocationUseCase,
    GetStockLocationsUseCase,
    UpdateStockLocationUseCase,
    DeleteStockLocationUseCase,
    CreateStockWarehouseUseCase,
    GetStockWarehousesUseCase,
    UpdateStockWarehouseUseCase,
    DeleteStockWarehouseUseCase
)
from app.domain.ports.out.stock_location_repository import StockLocationRepository
from app.domain.ports.out.stock_warehouse_repository import StockWarehouseRepository


def get_stock_location_repository(session: Session = Depends(get_session)) -> StockLocationRepository:
    return StockLocationRepositoryORM(session)


def get_stock_warehouse_repository(session: Session = Depends(get_session)) -> StockWarehouseRepository:
    return StockWarehouseRepositoryORM(session)


def get_create_stock_location_use_case(stock_repository: StockLocationRepository = Depends(get_stock_location_repository)) -> CreateStockLocationUseCase:
    return CreateStockLocationUseCase(stock_repository)


def get_stock_locations_use_case(stock_repository: StockLocationRepository = Depends(get_stock_location_repository)) -> GetStockLocationsUseCase:
    return GetStockLocationsUseCase(stock_repository)


def get_update_stock_location_use_case(stock_repository: StockLocationRepository = Depends(get_stock_location_repository)) -> UpdateStockLocationUseCase:
    return UpdateStockLocationUseCase(stock_repository)


def get_delete_stock_location_use_case(stock_repository: StockLocationRepository = Depends(get_stock_location_repository)) -> DeleteStockLocationUseCase:
    return DeleteStockLocationUseCase(stock_repository)


def get_create_stock_warehouse_use_case(stock_repository: StockWarehouseRepository = Depends(get_stock_warehouse_repository)) -> CreateStockWarehouseUseCase:
    return CreateStockWarehouseUseCase(stock_repository)


def get_stock_warehouses_use_case(stock_repository: StockWarehouseRepository = Depends(get_stock_warehouse_repository)) -> GetStockWarehousesUseCase:
    return GetStockWarehousesUseCase(stock_repository)


def get_update_stock_warehouse_use_case(stock_repository: StockWarehouseRepository = Depends(get_stock_warehouse_repository)) -> UpdateStockWarehouseUseCase:
    return UpdateStockWarehouseUseCase(stock_repository)


def get_delete_stock_warehouse_use_case(stock_repository: StockWarehouseRepository = Depends(get_stock_warehouse_repository)) -> DeleteStockWarehouseUseCase:
    return DeleteStockWarehouseUseCase(stock_repository)
