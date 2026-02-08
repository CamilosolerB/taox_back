from app.domain.ports.out.product_repository import ProductRepository
from app.domain.entities.product_model import Product


class GetProductByIdUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: str) -> Product:
        return self.product_repository.get_product_by_id(product_id)
