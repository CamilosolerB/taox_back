from app.domain.ports.out.product_repository import ProductRepository
from app.domain.entities.product_model import Product


class GetAllProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self) -> list[Product]:
        return self.product_repository.get_all_products()
