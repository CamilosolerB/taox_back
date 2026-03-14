"""
HTTP endpoints para Chemical Stock
"""
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.application.dto.chemical_stock_dto import ChemicalStockCreateDTO, ChemicalStockUpdateDTO, ChemicalStockResponseDTO
from app.application.use_cases.chemical_stock_case import (
    GetAllStocksUseCase,
    GetStockByIdUseCase,
    GetCriticalStocksUseCase,
    CreateStockUseCase,
    UpdateStockUseCase,
    DeleteStockUseCase
)
from app.infrastructure.config.chemical_stock_dependencies import (
    get_get_all_stocks_use_case,
    get_get_stock_by_id_use_case,
    get_get_critical_stocks_use_case,
    get_create_stock_use_case,
    get_update_stock_use_case,
    get_delete_stock_use_case
)

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/", response_model=List[ChemicalStockResponseDTO], status_code=status.HTTP_200_OK)
def get_all_stocks(
    company_id: str,
    use_case: GetAllStocksUseCase = Depends(get_get_all_stocks_use_case)
):
    """Obtiene todos los stocks químicos de una empresa"""
    stocks = use_case.execute(company_id)
    return [ChemicalStockResponseDTO.model_validate(s) for s in stocks]


@router.get("/critical", response_model=List[ChemicalStockResponseDTO], status_code=status.HTTP_200_OK)
def get_critical_stocks(
    company_id: str,
    use_case: GetCriticalStocksUseCase = Depends(get_get_critical_stocks_use_case)
):
    """Obtiene todos los stocks en nivel crítico.
    
    Dashboard para mostrar productos con stock crítico (cantidad_actual < cantidad_minima)
    """
    stocks = use_case.execute(company_id)
    return [ChemicalStockResponseDTO.model_validate(s) for s in stocks]


@router.get("/{id_stock_quimico}", response_model=ChemicalStockResponseDTO, status_code=status.HTTP_200_OK)
def get_stock_by_id(
    id_stock_quimico: int,
    company_id: str,
    use_case: GetStockByIdUseCase = Depends(get_get_stock_by_id_use_case)
):
    """Obtiene un stock por ID con información de estado crítico y bajo"""
    try:
        stock = use_case.execute(id_stock_quimico, company_id)
        return ChemicalStockResponseDTO.model_validate(stock)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ChemicalStockResponseDTO, status_code=status.HTTP_201_CREATED)
def create_stock(
    stock_dto: ChemicalStockCreateDTO,
    use_case: CreateStockUseCase = Depends(get_create_stock_use_case)
):
    """Crea un nuevo stock químico con umbrales de alertas automáticas"""
    try:
        stock = use_case.execute(stock_dto)
        return ChemicalStockResponseDTO.model_validate(stock)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_stock_quimico}", response_model=ChemicalStockResponseDTO, status_code=status.HTTP_200_OK)
def update_stock(
    id_stock_quimico: int,
    stock_dto: ChemicalStockUpdateDTO,
    use_case: UpdateStockUseCase = Depends(get_update_stock_use_case)
):
    """Actualiza un stock químico"""
    try:
        stock = use_case.execute(id_stock_quimico, stock_dto)
        return ChemicalStockResponseDTO.model_validate(stock)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_stock_quimico}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock(
    id_stock_quimico: int,
    company_id: str,
    use_case: DeleteStockUseCase = Depends(get_delete_stock_use_case)
):
    """Elimina un stock químico"""
    try:
        use_case.execute(id_stock_quimico, company_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
