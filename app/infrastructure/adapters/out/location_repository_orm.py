"""
Implementación de repositorio ORM para Ubicación
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.ports.out.location_repository import LocationRepository
from app.domain.entities.location_model import Location
from app.infrastructure.db.models.location_orm import LocationORM


class LocationRepositoryORM(LocationRepository):
    """Implementación del repositorio de Ubicación usando SQLAlchemy ORM"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _orm_to_entity(self, orm: LocationORM) -> Location:
        """Convierte modelo ORM a entidad"""
        if not orm:
            return None
        return Location(
            id_ubicacion=orm.id_ubicacion,
            ubicacion=orm.ubicacion,
            posicion=orm.posicion,
            nivel=orm.nivel,
            tipo_ubicacion=orm.tipo_ubicacion,
            localizador=orm.localizador,
            id_empresa=orm.id_empresa,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: Location) -> LocationORM:
        """Convierte entidad a modelo ORM"""
        return LocationORM(
            ubicacion=entity.ubicacion,
            posicion=entity.posicion,
            nivel=entity.nivel,
            tipo_ubicacion=entity.tipo_ubicacion,
            localizador=entity.localizador,
            id_empresa=entity.id_empresa,
            is_active=entity.is_active
        )
    
    def get_all_locations(self, company_id: str) -> List[Location]:
        """Obtiene todas las ubicaciones"""
        locations = self.session.query(LocationORM).filter(
            LocationORM.id_empresa == company_id
        ).all()
        return [self._orm_to_entity(l) for l in locations]
    
    def get_location_by_id(self, location_id: int, company_id: str) -> Optional[Location]:
        """Obtiene una ubicación por ID"""
        location = self.session.query(LocationORM).filter(
            LocationORM.id_ubicacion == location_id,
            LocationORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(location)
    
    def get_location_by_code(self, localizador: str, company_id: str) -> Optional[Location]:
        """Obtiene una ubicación por código"""
        location = self.session.query(LocationORM).filter(
            LocationORM.localizador == localizador,
            LocationORM.id_empresa == company_id
        ).first()
        return self._orm_to_entity(location)
    
    def create_location(self, location: Location) -> Location:
        """Crea una ubicación"""
        orm = self._entity_to_orm(location)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def update_location(self, location_id: int, location: Location) -> Optional[Location]:
        """Actualiza una ubicación"""
        orm = self.session.query(LocationORM).filter(
            LocationORM.id_ubicacion == location_id
        ).first()
        
        if not orm:
            return None
        
        orm.ubicacion = location.ubicacion
        orm.posicion = location.posicion
        orm.nivel = location.nivel
        orm.tipo_ubicacion = location.tipo_ubicacion
        orm.localizador = location.localizador
        orm.is_active = location.is_active
        
        self.session.commit()
        self.session.refresh(orm)
        return self._orm_to_entity(orm)
    
    def delete_location(self, location_id: int, company_id: str) -> bool:
        """Elimina una ubicación"""
        result = self.session.query(LocationORM).filter(
            LocationORM.id_ubicacion == location_id,
            LocationORM.id_empresa == company_id
        ).delete()
        self.session.commit()
        return result > 0
