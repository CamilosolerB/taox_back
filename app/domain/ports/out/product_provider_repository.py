"""
Puerto de salida para repositorio de Producto-Proveedor
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.product_provider_model import ProductProvider


class ProductProviderRepository(ABC):
    """
    Interfaz para el repositorio de Producto-Proveedor
    """
    
    @abstractmethod
    def get_all_product_providers(self) -> List[ProductProvider]:
        """Obtiene todas las relaciones producto-proveedor"""
        pass
    
    @abstractmethod
    def get_providers_by_product(self, product_code: str) -> List[ProductProvider]:
        """Obtiene todos los proveedores de un producto"""
        pass
    
    @abstractmethod
    def get_products_by_provider(self, provider_id: str) -> List[ProductProvider]:
        """Obtiene todos los productos de un proveedor"""
        pass
    
    @abstractmethod
    def get_main_provider(self, product_code: str) -> Optional[ProductProvider]:
        """Obtiene el proveedor principal de un producto"""
        pass
    
    @abstractmethod
    def create_product_provider(self, product_provider: ProductProvider) -> ProductProvider:
        """Crea una nueva relación producto-proveedor"""
        pass
    
    @abstractmethod
    def update_product_provider(
        self,
        product_code: str,
        provider_id: str,
        product_provider: ProductProvider
    ) -> Optional[ProductProvider]:
        """Actualiza una relación producto-proveedor"""
        pass
    
    @abstractmethod
    def delete_product_provider(self, product_code: str, provider_id: str) -> bool:
        """Elimina una relación producto-proveedor"""
        pass
    
    @abstractmethod
    def set_main_provider(self, product_code: str, provider_id: str) -> Optional[ProductProvider]:
        """Establece un proveedor como principal"""
        pass
