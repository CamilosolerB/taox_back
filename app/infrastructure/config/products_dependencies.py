from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.product_orm_repository import (
    ProductORMRepository
)
from app.application.use_cases.products_case.get_all_products import GetAllProductsUseCase
from app.application.use_cases.products_case.get_product_by_id import GetProductByIdUseCase
from app.application.use_cases.products_case.get_products_by_company_id import GetProductsByCompanyIdUseCase
from app.application.use_cases.products_case.create_product import CreateProductUseCase
from app.application.use_cases.products_case.update_product import UpdateProductUseCase
from app.application.use_cases.products_case.delete_product import DeleteProductUseCase
from app.domain.ports.out.product_repository import ProductRepository


def get_product_repository(session: Session = Depends(get_session)) -> ProductRepository:
    return ProductORMRepository(session)

def get_all_products_use_case(product_repository: ProductRepository = Depends(get_product_repository)) -> GetAllProductsUseCase:
    return GetAllProductsUseCase(product_repository)

def get_product_by_id_use_case(product_repository: ProductRepository = Depends(get_product_repository)) -> GetProductByIdUseCase:
    return GetProductByIdUseCase(product_repository)

def get_products_by_company_id_use_case(product_repository: ProductRepository = Depends(get_product_repository)) -> GetProductsByCompanyIdUseCase:
    return GetProductsByCompanyIdUseCase(product_repository)

def get_create_product_use_case(product_repository: ProductRepository = Depends(get_product_repository)) -> CreateProductUseCase:
    return CreateProductUseCase(product_repository)

def get_update_product_use_case(product_repository: ProductRepository = Depends(get_product_repository)) -> UpdateProductUseCase:
    return UpdateProductUseCase(product_repository)

def get_delete_product_use_case(product_repository: ProductRepository = Depends(get_product_repository)) -> DeleteProductUseCase:
    return DeleteProductUseCase(product_repository)
