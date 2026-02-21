"""
Product Provider dependencies configuration
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.product_provider_repository_orm import ProductProviderRepositoryORM
from app.application.use_cases.product_provider_case.product_provider_use_cases import (
    CreateProductProviderUseCase,
    GetProductProvidersUseCase,
    UpdateProductProviderUseCase,
    DeleteProductProviderUseCase
)
from app.domain.ports.out.product_provider_repository import ProductProviderRepository


def get_product_provider_repository(session: Session = Depends(get_session)) -> ProductProviderRepository:
    return ProductProviderRepositoryORM(session)


def get_create_product_provider_use_case(pp_repository: ProductProviderRepository = Depends(get_product_provider_repository)) -> CreateProductProviderUseCase:
    return CreateProductProviderUseCase(pp_repository)


def get_product_providers_use_case(pp_repository: ProductProviderRepository = Depends(get_product_provider_repository)) -> GetProductProvidersUseCase:
    return GetProductProvidersUseCase(pp_repository)


def get_update_product_provider_use_case(pp_repository: ProductProviderRepository = Depends(get_product_provider_repository)) -> UpdateProductProviderUseCase:
    return UpdateProductProviderUseCase(pp_repository)


def get_delete_product_provider_use_case(pp_repository: ProductProviderRepository = Depends(get_product_provider_repository)) -> DeleteProductProviderUseCase:
    return DeleteProductProviderUseCase(pp_repository)
