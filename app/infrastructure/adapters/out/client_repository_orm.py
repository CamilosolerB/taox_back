"""
Implementación de repositorio ORM para Cliente
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.ports.out.client_repository import ClientRepository
from app.domain.entities.client_model import Client
from app.infrastructure.db.models.client_orm import ClientORM


class ClientRepositoryORM(ClientRepository):
    """Implementación del repositorio de Cliente"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _orm_to_entity(self, orm: ClientORM) -> Client:
        """Convierte modelo ORM a entidad"""
        if not orm:
            return None
        return Client(
            codigo_cliente=orm.codigo_cliente,
            cliente=orm.cliente,
            telefono1=orm.telefono1,
            telefono2=orm.telefono2,
            contacto=orm.contacto,
            correo=orm.correo,
            ciudad=orm.ciudad,
            tipo_agua=orm.tipo_agua,
            cantidad_promedio_kg=orm.cantidad_promedio_kg,
            id_empresa=orm.id_empresa,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: Client) -> ClientORM:
        """Convierte entidad a modelo ORM"""
        return ClientORM(
            codigo_cliente=entity.codigo_cliente,
            cliente=entity.cliente,
            telefono1=entity.telefono1,
            telefono2=entity.telefono2,
            contacto=entity.contacto,
            correo=entity.correo,
            ciudad=entity.ciudad,
            tipo_agua=entity.tipo_agua,
            cantidad_promedio_kg=entity.cantidad_promedio_kg,
            id_empresa=entity.id_empresa,
            is_active=entity.is_active
        )
    
    def get_all_clients(self, company_id: str) -> List[Client]:
        """Obtiene todos los clientes"""
        clients = self.session.query(ClientORM).filter(
            ClientORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(c) for c in clients]
    
    def get_client_by_id(self, client_id: str, company_id: str) -> Optional[Client]:
        """Obtiene un cliente por ID"""
        client = self.session.query(ClientORM).filter(
            ClientORM.codigo_cliente == client_id,
            ClientORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(client)
    
    def get_client_by_email(self, email: str, company_id: str) -> Optional[Client]:
        """Obtiene un cliente por email"""
        client = self.session.query(ClientORM).filter(
            ClientORM.correo == email,
            ClientORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(client)
    
    def get_clients_by_city(self, city: str, company_id: str) -> List[Client]:
        """Obtiene clientes de una ciudad"""
        clients = self.session.query(ClientORM).filter(
            ClientORM.ciudad == city,
            ClientORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(c) for c in clients]
    
    def create_client(self, client: Client) -> Client:
        """Crea un cliente"""
        orm = self._entity_to_orm(client)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def update_client(self, client_id: str, client: Client) -> Optional[Client]:
        """Actualiza un cliente"""
        orm = self.session.query(ClientORM).filter(
            ClientORM.codigo_cliente == client_id
        ).first()
        
        if not orm:
            return None
        
        orm.cliente = client.cliente
        orm.telefono1 = client.telefono1
        orm.telefono2 = client.telefono2
        orm.contacto = client.contacto
        orm.correo = client.correo
        orm.ciudad = client.ciudad
        orm.tipo_agua = client.tipo_agua
        orm.cantidad_promedio_kg = client.cantidad_promedio_kg
        orm.is_active = client.is_active
        
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def delete_client(self, client_id: str, company_id: str) -> bool:
        """Elimina un cliente"""
        result = self.session.query(ClientORM).filter(
            ClientORM.codigo_cliente == client_id,
            ClientORM.id_empresa == company_id
        ).delete()
        self.session.commit()
        return result > 0
