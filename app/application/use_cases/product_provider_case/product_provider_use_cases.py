"""
Use cases para Producto-Proveedor
"""
from typing import List
from app.domain.ports.out.product_provider_repository import ProductProviderRepository
from app.domain.entities.product_provider_model import ProductProvider
import logging

logger = logging.getLogger(__name__)


class CreateProductProviderUseCase:
    """Use case para crear relación producto-proveedor"""
    
    def __init__(self, product_provider_repository: ProductProviderRepository):
        self.product_provider_repository = product_provider_repository
    
    def execute(
        self,
        codigo_producto: str,
        cad_proveedor: str,
        es_principal: bool = False
    ) -> ProductProvider:
        """Crea una relación producto-proveedor"""
        logger.info(f"Creando relación: producto={codigo_producto}, proveedor={cad_proveedor}")
        
        product_provider = ProductProvider(
            codigo_producto=codigo_producto,
            cad_proveedor=cad_proveedor,
            es_principal=es_principal
        )
        
        created = self.product_provider_repository.create_product_provider(product_provider)
        logger.info(f"Relación creada exitosamente")
        return created


class GetProductProvidersUseCase:
    """Use case para obtener relaciones producto-proveedor"""
    
    def __init__(self, product_provider_repository: ProductProviderRepository):
        self.product_provider_repository = product_provider_repository
    
    def get_all(self) -> List[ProductProvider]:
        """Obtiene todas las relaciones"""
        return self.product_provider_repository.get_all_product_providers()
    
    def get_by_product(self, product_code: str) -> List[ProductProvider]:
        """Obtiene proveedores de un producto"""
        return self.product_provider_repository.get_providers_by_product(product_code)
    
    def get_by_provider(self, provider_id: str) -> List[ProductProvider]:
        """Obtiene productos de un proveedor"""
        return self.product_provider_repository.get_products_by_provider(provider_id)
    
    def get_main_provider(self, product_code: str) -> ProductProvider:
        """Obtiene el proveedor principal de un producto"""
        provider = self.product_provider_repository.get_main_provider(product_code)
        if not provider:
            raise Exception(f"No main provider found for product {product_code}")
        return provider


class UpdateProductProviderUseCase:
    """Use case para actualizar relación producto-proveedor"""
    
    def __init__(self, product_provider_repository: ProductProviderRepository):
        self.product_provider_repository = product_provider_repository
    
    def execute(
        self,
        codigo_producto: str,
        cad_proveedor: str,
        product_provider: ProductProvider
    ) -> ProductProvider:
        """Actualiza una relación"""
        logger.info(f"Actualizando relación: producto={codigo_producto}, proveedor={cad_proveedor}")
        updated = self.product_provider_repository.update_product_provider(
            codigo_producto,
            cad_proveedor,
            product_provider
        )
        if not updated:
            raise Exception(f"Could not update product provider")
        return updated
    
    def set_main_provider(self, product_code: str, provider_id: str) -> ProductProvider:
        """Establece un proveedor como principal"""
        logger.info(f"Estableciendo proveedor principal: {provider_id}")
        main = self.product_provider_repository.set_main_provider(product_code, provider_id)
        if not main:
            raise Exception(f"Could not set main provider")
        return main


class DeleteProductProviderUseCase:
    """Use case para eliminar relación producto-proveedor"""
    
    def __init__(self, product_provider_repository: ProductProviderRepository):
        self.product_provider_repository = product_provider_repository
    
    def execute(self, product_code: str, provider_id: str) -> bool:
        """Elimina una relación"""
        logger.info(f"Eliminando relación: producto={product_code}, proveedor={provider_id}")
        deleted = self.product_provider_repository.delete_product_provider(product_code, provider_id)
        if not deleted:
            raise Exception(f"Could not delete product provider")
        return True
