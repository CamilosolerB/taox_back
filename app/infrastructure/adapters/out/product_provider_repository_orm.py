"""
Implementación de repositorio ORM para Producto-Proveedor
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.ports.out.product_provider_repository import ProductProviderRepository
from app.domain.entities.product_provider_model import ProductProvider
from app.infrastructure.db.models.product_provider_orm import ProductProviderORM


class ProductProviderRepositoryORM(ProductProviderRepository):
    """Implementación del repositorio de Producto-Proveedor"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _orm_to_entity(self, orm: ProductProviderORM) -> ProductProvider:
        """Convierte modelo ORM a entidad"""
        if not orm:
            return None
        return ProductProvider(
            codigo_producto=orm.codigo_producto,
            cad_proveedor=orm.cad_proveedor,
            es_principal=orm.es_principal,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: ProductProvider) -> ProductProviderORM:
        """Convierte entidad a modelo ORM"""
        return ProductProviderORM(
            codigo_producto=entity.codigo_producto,
            cad_proveedor=entity.cad_proveedor,
            es_principal=entity.es_principal
        )
    
    def get_all_product_providers(self) -> List[ProductProvider]:
        """Obtiene todas las relaciones"""
        relationships = self.session.query(ProductProviderORM).all()
        return [self._orm_to_entity(r) for r in relationships]
    
    def get_providers_by_product(self, product_code: str) -> List[ProductProvider]:
        """Obtiene proveedores de un producto"""
        relationships = self.session.query(ProductProviderORM).filter(
            ProductProviderORM.codigo_producto == product_code
        ).all()
        return [self._orm_to_entity(r) for r in relationships]
    
    def get_products_by_provider(self, provider_id: str) -> List[ProductProvider]:
        """Obtiene productos de un proveedor"""
        relationships = self.session.query(ProductProviderORM).filter(
            ProductProviderORM.cad_proveedor == provider_id
        ).all()
        return [self._orm_to_entity(r) for r in relationships]
    
    def get_main_provider(self, product_code: str) -> Optional[ProductProvider]:
        """Obtiene el proveedor principal de un producto"""
        relationship = self.session.query(ProductProviderORM).filter(
            ProductProviderORM.codigo_producto == product_code,
            ProductProviderORM.es_principal == True
        ).first()
        return self._orm_to_entity(relationship)
    
    def create_product_provider(self, product_provider: ProductProvider) -> ProductProvider:
        """Crea una relación"""
        orm = self._entity_to_orm(product_provider)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def update_product_provider(
        self,
        product_code: str,
        provider_id: str,
        product_provider: ProductProvider
    ) -> Optional[ProductProvider]:
        """Actualiza una relación"""
        orm = self.session.query(ProductProviderORM).filter(
            ProductProviderORM.codigo_producto == product_code,
            ProductProviderORM.cad_proveedor == provider_id
        ).first()
        
        if not orm:
            return None
        
        orm.es_principal = product_provider.es_principal
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def delete_product_provider(self, product_code: str, provider_id: str) -> bool:
        """Elimina una relación"""
        result = self.session.query(ProductProviderORM).filter(
            ProductProviderORM.codigo_producto == product_code,
            ProductProviderORM.cad_proveedor == provider_id
        ).delete()
        self.session.commit()
        return result > 0
    
    def set_main_provider(self, product_code: str, provider_id: str) -> Optional[ProductProvider]:
        """Establece un proveedor como principal"""
        # Primero, desactivar main de otros proveedores
        self.session.query(ProductProviderORM).filter(
            ProductProviderORM.codigo_producto == product_code,
            ProductProviderORM.es_principal == True
        ).update({ProductProviderORM.es_principal: False})
        
        # Actualizar el nuevo main
        orm = self.session.query(ProductProviderORM).filter(
            ProductProviderORM.codigo_producto == product_code,
            ProductProviderORM.cad_proveedor == provider_id
        ).first()
        
        if not orm:
            return None
        
        orm.es_principal = True
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
