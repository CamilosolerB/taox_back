from app.domain.ports.out.product_repository import ProductRepository
from app.domain.entities.product_model import Product


class UpdateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: str, product_data: dict) -> Product:
        return self.product_repository.update_product(product_id, product_data)
