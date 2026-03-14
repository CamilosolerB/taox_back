"""
Repository ORM implementation para Process
"""
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.process_model import Process
from app.domain.ports.out.process_repository import ProcessRepository
from app.infrastructure.db.models.process_orm import ProcessORM
from typing import List


class ProcessORMRepository(ProcessRepository):
    """Implementación ORM del repositorio de procesos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_processes(self, company_id: str) -> List[Process]:
        """Obtiene todos los procesos de una empresa"""
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        processes_orm = self.db.query(ProcessORM).filter(ProcessORM.id_empresa == company_uuid).all()
        return [self._orm_to_entity(p) for p in processes_orm]
    
    def get_process_by_id(self, id_proceso: UUID, company_id: str) -> Process:
        """Obtiene un proceso por ID"""
        # Convert id_proceso to UUID if it's a string
        proceso_uuid = UUID(id_proceso) if isinstance(id_proceso, str) else id_proceso
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        process_orm = self.db.query(ProcessORM).filter(
            ProcessORM.id_proceso == proceso_uuid,
            ProcessORM.id_empresa == company_uuid
        ).first()
        return self._orm_to_entity(process_orm) if process_orm else None
    
    def get_processes_by_type(self, tipo_proceso: str, company_id: str) -> List[Process]:
        """Obtiene procesos por tipo"""
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        processes_orm = self.db.query(ProcessORM).filter(
            ProcessORM.tipo_proceso == tipo_proceso,
            ProcessORM.id_empresa == company_uuid
        ).all()
        return [self._orm_to_entity(p) for p in processes_orm]
    
    def create_process(self, process: Process) -> Process:
        """Crea un nuevo proceso"""
        process_orm = self._entity_to_orm(process)
        self.db.add(process_orm)
        self.db.commit()
        self.db.refresh(process_orm)
        return self._orm_to_entity(process_orm)
    
    def update_process(self, id_proceso: UUID, process_data: dict) -> Process:
        """Actualiza un proceso"""
        # Convert id_proceso to UUID if it's a string
        proceso_uuid = UUID(id_proceso) if isinstance(id_proceso, str) else id_proceso
        process_orm = self.db.query(ProcessORM).filter(ProcessORM.id_proceso == proceso_uuid).first()
        if not process_orm:
            return None
        for key, value in process_data.items():
            if value is not None:
                setattr(process_orm, key, value)
        self.db.commit()
        self.db.refresh(process_orm)
        return self._orm_to_entity(process_orm)
    
    def delete_process(self, id_proceso: UUID, company_id: str) -> bool:
        """Elimina un proceso"""
        # Convert to UUID if they're strings
        proceso_uuid = UUID(id_proceso) if isinstance(id_proceso, str) else id_proceso
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        process_orm = self.db.query(ProcessORM).filter(
            ProcessORM.id_proceso == proceso_uuid,
            ProcessORM.id_empresa == company_uuid
        ).first()
        if not process_orm:
            return False
        self.db.delete(process_orm)
        self.db.commit()
        return True
    
    def _orm_to_entity(self, process_orm: ProcessORM) -> Process:
        """Convierte ORM a entidad de dominio"""
        if not process_orm:
            return None
        return Process(
            id_proceso=process_orm.id_proceso,
            nombre=process_orm.nombre,
            descripcion=process_orm.descripcion,
            tipo_proceso=process_orm.tipo_proceso,
            id_empresa=process_orm.id_empresa,
            is_active=process_orm.is_active,
            created_at=process_orm.created_at,
            updated_at=process_orm.updated_at
        )
    
    def _entity_to_orm(self, process: Process) -> ProcessORM:
        """Convierte entidad de dominio a ORM"""
        return ProcessORM(
            id_proceso=process.id_proceso,
            nombre=process.nombre,
            descripcion=process.descripcion,
            tipo_proceso=process.tipo_proceso,
            id_empresa=process.id_empresa,
            is_active=process.is_active,
            created_at=process.created_at,
            updated_at=process.updated_at
        )
