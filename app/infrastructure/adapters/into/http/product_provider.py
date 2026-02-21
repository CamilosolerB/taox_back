"""
Endpoints para Producto-Proveedor
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.application.dto.product_provider_dto import ProductProviderCreateDTO, ProductProviderUpdateDTO, ProductProviderDTO
from app.application.use_cases.product_provider_case.product_provider_use_cases import (
    CreateProductProviderUseCase,
    GetProductProvidersUseCase,
    UpdateProductProviderUseCase,
    DeleteProductProviderUseCase
)
from app.infrastructure.config.product_provider_dependencies import (
    get_create_product_provider_use_case,
    get_product_providers_use_case,
    get_update_product_provider_use_case,
    get_delete_product_provider_use_case
)
from app.core.middleware.auth_middleware import get_current_user, require_admin
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/product-providers", tags=["product-providers"])


@router.get("", response_model=List[ProductProviderDTO])
def get_product_providers(
    get_pp_use_case: GetProductProvidersUseCase = Depends(get_product_providers_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todas las relaciones producto-proveedor"""
    try:
        return get_pp_use_case.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/by-product/{product_code}", response_model=List[ProductProviderDTO])
def get_providers_by_product(
    product_code: str,
    get_pp_use_case: GetProductProvidersUseCase = Depends(get_product_providers_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todos los proveedores de un producto"""
    try:
        return get_pp_use_case.get_by_product(product_code)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/by-provider/{provider_id}", response_model=List[ProductProviderDTO])
def get_products_by_provider(
    provider_id: str,
    get_pp_use_case: GetProductProvidersUseCase = Depends(get_product_providers_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene todos los productos de un proveedor"""
    try:
        return get_pp_use_case.get_by_provider(provider_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/main/{product_code}", response_model=ProductProviderDTO)
def get_main_provider(
    product_code: str,
    get_pp_use_case: GetProductProvidersUseCase = Depends(get_product_providers_use_case),
    current_user: Annotated[dict, Depends(get_current_user)] = None
):
    """Obtiene el proveedor principal de un producto"""
    try:
        return get_pp_use_case.get_main_provider(product_code)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=ProductProviderDTO, status_code=status.HTTP_201_CREATED)
def create_product_provider(
    pp_dto: ProductProviderCreateDTO,
    create_pp_use_case: CreateProductProviderUseCase = Depends(get_create_product_provider_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Crea una nueva relación producto-proveedor"""
    logger.info(f"Creando relación - Producto: {pp_dto.codigo_producto}, Proveedor: {pp_dto.cad_proveedor}")
    try:
        return create_pp_use_case.execute(
            codigo_producto=pp_dto.codigo_producto,
            cad_proveedor=pp_dto.cad_proveedor,
            es_principal=pp_dto.es_principal
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{product_code}/{provider_id}", response_model=ProductProviderDTO)
def update_product_provider(
    product_code: str,
    provider_id: str,
    pp_dto: ProductProviderUpdateDTO,
    update_pp_use_case: UpdateProductProviderUseCase = Depends(get_update_product_provider_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Actualiza una relación producto-proveedor"""
    logger.info(f"Actualizando relación - Producto: {product_code}, Proveedor: {provider_id}")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.post("/{product_code}/{provider_id}/set-main")
def set_main_provider(
    product_code: str,
    provider_id: str,
    update_pp_use_case: UpdateProductProviderUseCase = Depends(get_update_product_provider_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Establece un proveedor como principal para un producto"""
    logger.info(f"Estableciendo proveedor principal - Producto: {product_code}, Proveedor: {provider_id}")
    try:
        result = update_pp_use_case.set_main_provider(product_code, provider_id)
        return {"message": "Proveedor principal establecido", "data": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_code}/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_provider(
    product_code: str,
    provider_id: str,
    delete_pp_use_case: DeleteProductProviderUseCase = Depends(get_delete_product_provider_use_case),
    current_user: Annotated[dict, Depends(require_admin)] = None
):
    """Elimina una relación producto-proveedor"""
    logger.info(f"Eliminando relación - Producto: {product_code}, Proveedor: {provider_id}")
    try:
        delete_pp_use_case.execute(product_code, provider_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
