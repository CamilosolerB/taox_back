from app.domain.ports.out.product_repository import ProductRepository
from app.domain.entities.product_model import Product


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product: Product) -> Product:
        return self.product_repository.create_product(product)
