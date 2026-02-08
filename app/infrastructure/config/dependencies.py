from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.user_orm_repository import (
    UserORMRepository
)
from app.application.use_cases.users_case.create_user import CreateUserUseCase
from app.application.use_cases.users_case.get_all_users import GetAllUsersUseCase
from app.application.use_cases.users_case.get_user_by_id import GetUserByIdUseCase
from app.application.use_cases.users_case.update_user import UpdateUserUseCase
from app.application.use_cases.users_case.delete_user import DeleteUserUseCase
from app.domain.ports.out.user_repository import UserRepository

def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserORMRepository(session)

def get_create_user_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository)

def get_all_users_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> GetAllUsersUseCase:
    return GetAllUsersUseCase(user_repository)

def get_user_by_id_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_repository)

def get_update_user_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repository)

def get_delete_user_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_repository)