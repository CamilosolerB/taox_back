from abc import ABC, abstractmethod
from app.domain.entities.product_model import Product


class ProductRepository(ABC):
    @abstractmethod
    def get_all_products(self) -> list[Product]:
        pass

    @abstractmethod
    def get_product_by_id(self, id_product: str) -> Product:
        pass

    @abstractmethod
    def get_products_by_company_id(self, company_id: str) -> list[Product]:
        pass

    @abstractmethod
    def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update_product(self, id_product: str, product_data: dict) -> Product:
        pass

    @abstractmethod
    def delete_product(self, id_product: str) -> None:
        pass
