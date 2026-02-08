from app.domain.ports.out.product_repository import ProductRepository
from app.domain.entities.product_model import Product


class GetProductsByCompanyIdUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, company_id: str) -> list[Product]:
        return self.product_repository.get_products_by_company_id(company_id)
