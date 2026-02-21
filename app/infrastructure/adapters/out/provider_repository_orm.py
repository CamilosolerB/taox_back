"""
Implementación de repositorio ORM para Proveedor
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.ports.out.provider_repository import ProviderRepository
from app.domain.entities.provider_model import Provider
from app.infrastructure.db.models.provider_orm import ProviderORM


class ProviderRepositoryORM(ProviderRepository):
    """Implementación del repositorio de Proveedor usando SQLAlchemy ORM"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _orm_to_entity(self, orm: ProviderORM) -> Provider:
        """Convierte modelo ORM a entidad de dominio"""
        if not orm:
            return None
        return Provider(
            cad_proveedor=orm.cad_proveedor,
            nombre=orm.nombre,
            contacto=orm.contacto,
            direccion=orm.direccion,
            telefono=orm.telefono,
            celular=orm.celular,
            web=orm.web,
            correo=orm.correo,
            id_empresa=orm.id_empresa,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: Provider) -> ProviderORM:
        """Convierte entidad de dominio a modelo ORM"""
        return ProviderORM(
            cad_proveedor=entity.cad_proveedor,
            nombre=entity.nombre,
            contacto=entity.contacto,
            direccion=entity.direccion,
            telefono=entity.telefono,
            celular=entity.celular,
            web=entity.web,
            correo=entity.correo,
            id_empresa=entity.id_empresa,
            is_active=entity.is_active
        )
    
    def get_all_providers(self, company_id: str) -> List[Provider]:
        """Obtiene todos los proveedores de una empresa"""
        providers = self.session.query(ProviderORM).filter(
            ProviderORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(p) for p in providers]
    
    def get_provider_by_id(self, provider_id: str, company_id: str) -> Optional[Provider]:
        """Obtiene un proveedor por ID"""
        provider = self.session.query(ProviderORM).filter(
            ProviderORM.cad_proveedor == provider_id,
            ProviderORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(provider)
    
    def get_provider_by_email(self, email: str, company_id: str) -> Optional[Provider]:
        """Obtiene un proveedor por email"""
        provider = self.session.query(ProviderORM).filter(
            ProviderORM.correo == email,
            ProviderORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(provider)
    
    def create_provider(self, provider: Provider) -> Provider:
        """Crea un nuevo proveedor"""
        orm = self._entity_to_orm(provider)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def update_provider(self, provider_id: str, provider: Provider) -> Optional[Provider]:
        """Actualiza un proveedor existente"""
        orm = self.session.query(ProviderORM).filter(
            ProviderORM.cad_proveedor == provider_id
        ).first()
        
        if not orm:
            return None
        
        orm.nombre = provider.nombre
        orm.contacto = provider.contacto
        orm.direccion = provider.direccion
        orm.telefono = provider.telefono
        orm.celular = provider.celular
        orm.web = provider.web
        orm.correo = provider.correo
        orm.is_active = provider.is_active
        
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def delete_provider(self, provider_id: str, company_id: str) -> bool:
        """Elimina un proveedor"""
        result = self.session.query(ProviderORM).filter(
            ProviderORM.cad_proveedor == provider_id,
            ProviderORM.id_empresa == company_id
        ).delete()
        self.session.commit()
        return result > 0
