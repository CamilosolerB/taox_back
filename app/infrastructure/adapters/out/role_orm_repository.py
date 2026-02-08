from sqlalchemy.orm import Session
from app.domain.entities.role_model import Role
from app.domain.ports.out.role_repository import RoleRepository
from app.infrastructure.db.models.role_orm import Role as RoleORM


class RoleORMRepository(RoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_roles(self) -> list[Role]:
        roles_orm = self.db.query(RoleORM).all()
        return [
            Role(
                id_role=role.id_role,
                name=role.name
            )
            for role in roles_orm
        ]
    
    def get_role_by_id(self, id_role: str) -> Role:
        role_orm = self.db.query(RoleORM).filter(RoleORM.id_role == id_role).first()
        return Role(
            id_role=role_orm.id_role,
            name=role_orm.name
        )
    
    def create_role(self, role: Role) -> Role:
        role_orm = RoleORM(**role.dict())
        self.db.add(role_orm)
        self.db.commit()
        self.db.refresh(role_orm)
        return Role(
            id_role=role_orm.id_role,
            name=role_orm.name
        )
    
    def update_role(self, id_role: str, role_data: dict) -> Role:
        role_orm = self.db.query(RoleORM).filter(RoleORM.id_role == id_role).first()
        if role_orm is None:
            return None
        for key, value in role_data.items():
            if value is not None:
                setattr(role_orm, key, value)
        self.db.commit()
        self.db.refresh(role_orm)
        return Role(
            id_role=role_orm.id_role,
            name=role_orm.name
        )
    
    def delete_role(self, id_role: str) -> None:
        role_orm = self.db.query(RoleORM).filter(RoleORM.id_role == id_role).first()
        self.db.delete(role_orm)
        self.db.commit()
