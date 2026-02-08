from fastapi import APIRouter, Depends
from uuid import UUID
from app.application.dto.products_dto.product_dto import ProductDTO
from app.application.dto.products_dto.create_product_dto import CreateProductDTO
from app.application.dto.products_dto.update_product_dto import UpdateProductDTO
from app.application.use_cases.products_case.get_all_products import GetAllProductsUseCase
from app.application.use_cases.products_case.get_product_by_id import GetProductByIdUseCase
from app.application.use_cases.products_case.get_products_by_company_id import GetProductsByCompanyIdUseCase
from app.application.use_cases.products_case.create_product import CreateProductUseCase
from app.application.use_cases.products_case.update_product import UpdateProductUseCase
from app.application.use_cases.products_case.delete_product import DeleteProductUseCase
from app.infrastructure.config.products_dependencies import (
    get_all_products_use_case,
    get_product_by_id_use_case,
    get_products_by_company_id_use_case,
    get_create_product_use_case,
    get_update_product_use_case,
    get_delete_product_use_case
)
from app.domain.entities.product_model import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductDTO])
def get_all_products(
    get_all_products_use_case: GetAllProductsUseCase = Depends(get_all_products_use_case)
):
    products = get_all_products_use_case.execute()
    return [ProductDTO.from_entity(product) for product in products]

@router.get("/by-id/{product_id}", response_model=ProductDTO)
def get_product_by_id(
    product_id: str,
    get_product_by_id_use_case: GetProductByIdUseCase = Depends(get_product_by_id_use_case)
):
    product = get_product_by_id_use_case.execute(product_id)
    if product is None:
        return {"error": "Product not found"}
    return ProductDTO.from_entity(product)

@router.get("/by-company/{company_id}", response_model=list[ProductDTO])
def get_products_by_company_id(
    company_id: UUID,
    get_products_by_company_id_use_case: GetProductsByCompanyIdUseCase = Depends(get_products_by_company_id_use_case)
):
    products = get_products_by_company_id_use_case.execute(str(company_id))
    return [ProductDTO.from_entity(product) for product in products]

@router.post("/", response_model=ProductDTO)
def create_product(
    create_product_dto: CreateProductDTO,
    create_product_use_case: CreateProductUseCase = Depends(get_create_product_use_case)
):
    product = create_product_use_case.execute(Product(
        id_product=create_product_dto.id_product,
        name=create_product_dto.name,
        generic_name=create_product_dto.generic_name,
        price=create_product_dto.price,
        unit_measure=create_product_dto.unit_measure,
        unit_price=create_product_dto.unit_price,
        min_unit_price=create_product_dto.min_unit_price,
        lead_time_days=create_product_dto.lead_time_days,
        restorage=create_product_dto.restorage,
        company_id=create_product_dto.company_id
    ))
    return ProductDTO.from_entity(product)

@router.put("/{product_id}", response_model=ProductDTO)
def update_product(
    product_id: str,
    update_product_dto: UpdateProductDTO,
    update_product_use_case: UpdateProductUseCase = Depends(get_update_product_use_case)
):
    product_data = update_product_dto.model_dump(exclude_unset=True)
    product = update_product_use_case.execute(product_id, product_data)
    return ProductDTO.from_entity(product)

@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    delete_product_use_case: DeleteProductUseCase = Depends(get_delete_product_use_case)
):
    delete_product_use_case.execute(product_id)
    return {"message": "Product deleted successfully"}
