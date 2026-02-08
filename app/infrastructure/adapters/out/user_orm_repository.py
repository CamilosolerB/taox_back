from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.domain.entities.user_model import User
from app.domain.ports.out.user_repository import UserRepository
from app.infrastructure.db.models.user_orm import User as UserORM

class UserORMRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        user_orm = UserORM(
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            role_id=user.role_id,
            company_id=user.company_id
        )
        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return User(
            id_user=user_orm.id_user,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            is_active=user_orm.is_active,
            role_id=user_orm.role_id,
            company_id=user_orm.company_id
        )
    
    def get_all_users(self):
        users = self.db.query(UserORM).options(
            joinedload(UserORM.role),
            joinedload(UserORM.company)
        ).all()
        return [User(
            id_user=user.id_user,
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            role_id=user.role_id,
            company_id=user.company_id
        ) for user in users]
    
    def get_user_by_email(self, email: str) -> User:
        user_orm = self.db.query(UserORM).filter(UserORM.email == email).first()
        if user_orm is None:
            return None
        return User(
            id_user=user_orm.id_user,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            is_active=user_orm.is_active,
            role_id=user_orm.role_id,
            company_id=user_orm.company_id
        )
    
    def get_user_by_id(self, id_user: str) -> User:
        user_orm = self.db.query(UserORM).options(
            joinedload(UserORM.role),
            joinedload(UserORM.company)
        ).filter(UserORM.id_user == id_user).first()
        if user_orm is None:
            return None
        return User(
            id_user=user_orm.id_user,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            is_active=user_orm.is_active,
            role_id=user_orm.role_id,
            company_id=user_orm.company_id
        )
    
    def update_user(self, id_user: str, user_data: dict) -> User:
        user_orm = self.db.query(UserORM).filter(UserORM.id_user == id_user).first()
        if user_orm is None:
            return None
        for key, value in user_data.items():
            if value is not None:
                setattr(user_orm, key, value)
        self.db.commit()
        self.db.refresh(user_orm)
        return User(
            id_user=user_orm.id_user,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            is_active=user_orm.is_active,
            role_id=user_orm.role_id,
            company_id=user_orm.company_id
        )
    
    def delete_user(self, id_user: str) -> None:
        user_orm = self.db.query(UserORM).filter(UserORM.id_user == id_user).first()
        self.db.delete(user_orm)
        self.db.commit()
    
    # Helper methods to get ORM objects with relations loaded
    def get_all_users_orm(self):
        """Retorna todos los usuarios ORM con relaciones cargadas"""
        return self.db.query(UserORM).options(
            joinedload(UserORM.role),
            joinedload(UserORM.company)
        ).all()
    
    def get_user_by_id_orm(self, id_user: str):
        """Retorna un usuario ORM con relaciones cargadas"""
        return self.db.query(UserORM).options(
            joinedload(UserORM.role),
            joinedload(UserORM.company)
        ).filter(UserORM.id_user == id_user).first()
    
