from app.domain.ports.out.product_repository import ProductRepository


class DeleteProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: str) -> None:
        return self.product_repository.delete_product(product_id)
