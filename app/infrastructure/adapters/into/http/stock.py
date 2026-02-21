"""
Endpoints para Stock (Ubicación y Almacén)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.application.dto.stock_dto import (
    StockLocationDTO, StockLocationCreateDTO, StockLocationUpdateDTO,
    StockWarehouseDTO, StockWarehouseCreateDTO, StockWarehouseUpdateDTO
)
from app.application.use_cases.stock_case.stock_use_cases import (
    CreateStockLocationUseCase, GetStockLocationsUseCase, UpdateStockLocationUseCase, DeleteStockLocationUseCase,
    CreateStockWarehouseUseCase, GetStockWarehousesUseCase, UpdateStockWarehouseUseCase, DeleteStockWarehouseUseCase
)
from app.infrastructure.config.stock_dependencies import (
    get_create_stock_location_use_case, get_stock_locations_use_case, 
    get_update_stock_location_use_case, get_delete_stock_location_use_case,
    get_create_stock_warehouse_use_case, get_stock_warehouses_use_case,
    get_update_stock_warehouse_use_case, get_delete_stock_warehouse_use_case
)
from app.core.middleware.auth_middleware import get_current_user, require_admin
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["stock"])


# Stock Ubicación Endpoints
@router.get("/stock-locations", response_model=List[StockLocationDTO])
def get_stock_locations(
    company_id: UUID,
    get_stock_use_case: GetStockLocationsUseCase = Depends(get_stock_locations_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todos los stocks en ubicaciones"""
    try:
        return get_stock_use_case.get_all(str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/stock-locations/{location_id}/{product_code}", response_model=StockLocationDTO)
def get_stock_by_location_product(
    location_id: int,
    product_code: str,
    company_id: UUID,
    get_stock_use_case: GetStockLocationsUseCase = Depends(get_stock_locations_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene stock de un producto en una ubicación específica"""
    try:
        return get_stock_use_case.get_by_location_and_product(location_id, product_code, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/stock-locations", response_model=StockLocationDTO, status_code=status.HTTP_201_CREATED)
def create_stock_location(
    stock_dto: StockLocationCreateDTO,
    create_stock_use_case: CreateStockLocationUseCase = Depends(get_create_stock_location_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Crea un nuevo stock en una ubicación"""
    logger.info(f"Creando stock ubicación - Producto: {stock_dto.codigo_producto}, Ubicación: {stock_dto.id_ubicacion}")
    try:
        return create_stock_use_case.execute(
            id_ubicacion=stock_dto.id_ubicacion,
            codigo_producto=stock_dto.codigo_producto,
            cantidad=stock_dto.cantidad,
            id_empresa=str(stock_dto.company_id)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/stock-locations/{location_id}/{product_code}", response_model=StockLocationDTO)
def update_stock_location(
    location_id: int,
    product_code: str,
    stock_dto: StockLocationUpdateDTO,
    update_stock_use_case: UpdateStockLocationUseCase = Depends(get_update_stock_location_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Actualiza la cantidad de stock en una ubicación"""
    logger.info(f"Actualizando stock ubicación - Producto: {product_code}, Ubicación: {location_id}")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/stock-locations/{location_id}/{product_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_location(
    location_id: int,
    product_code: str,
    company_id: UUID,
    delete_stock_use_case: DeleteStockLocationUseCase = Depends(get_delete_stock_location_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Elimina el stock de una ubicación"""
    logger.info(f"Eliminando stock ubicación - Producto: {product_code}, Ubicación: {location_id}")
    try:
        delete_stock_use_case.execute(location_id, product_code, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Stock Almacén Endpoints
@router.get("/stock-warehouse", response_model=List[StockWarehouseDTO])
def get_stock_warehouse(
    company_id: UUID,
    get_stock_use_case: GetStockWarehousesUseCase = Depends(get_stock_warehouses_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todos los stocks del almacén"""
    try:
        return get_stock_use_case.get_all(str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/stock-warehouse/{product_code}", response_model=StockWarehouseDTO)
def get_stock_warehouse_product(
    product_code: str,
    company_id: UUID,
    get_stock_use_case: GetStockWarehousesUseCase = Depends(get_stock_warehouses_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene el stock total de un producto"""
    try:
        return get_stock_use_case.get_by_product(product_code, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/stock-warehouse", response_model=StockWarehouseDTO, status_code=status.HTTP_201_CREATED)
def create_stock_warehouse(
    stock_dto: StockWarehouseCreateDTO,
    create_stock_use_case: CreateStockWarehouseUseCase = Depends(get_create_stock_warehouse_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Crea un nuevo stock en el almacén"""
    logger.info(f"Creando stock almacén - Producto: {stock_dto.codigo_producto}")
    try:
        return create_stock_use_case.execute(
            codigo_producto=stock_dto.codigo_producto,
            cantidad=stock_dto.cantidad,
            id_empresa=str(stock_dto.company_id)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/stock-warehouse/{product_code}/increment")
def increment_stock_warehouse(
    product_code: str,
    quantity: int,
    company_id: UUID,
    update_stock_use_case: UpdateStockWarehouseUseCase = Depends(get_update_stock_warehouse_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Incrementa el stock de un producto"""
    logger.info(f"Incrementando stock - Producto: {product_code}, Cantidad: {quantity}")
    try:
        update_stock_use_case.increment(product_code, quantity, str(company_id))
        return {"message": "Stock incrementado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/stock-warehouse/{product_code}/decrement")
def decrement_stock_warehouse(
    product_code: str,
    quantity: int,
    company_id: UUID,
    update_stock_use_case: UpdateStockWarehouseUseCase = Depends(get_update_stock_warehouse_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Decrementa el stock de un producto"""
    logger.info(f"Decrementando stock - Producto: {product_code}, Cantidad: {quantity}")
    try:
        update_stock_use_case.decrement(product_code, quantity, str(company_id))
        return {"message": "Stock decrementado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/stock-warehouse/{product_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_warehouse(
    product_code: str,
    company_id: UUID,
    delete_stock_use_case: DeleteStockWarehouseUseCase = Depends(get_delete_stock_warehouse_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Elimina el stock de un producto del almacén"""
    logger.info(f"Eliminando stock almacén - Producto: {product_code}")
    try:
        delete_stock_use_case.execute(product_code, str(company_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
