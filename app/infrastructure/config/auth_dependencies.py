from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.user_orm_repository import UserORMRepository
from app.application.use_cases.auth_case.register_user import RegisterUserUseCase
from app.application.use_cases.auth_case.login_user import LoginUserUseCase
from app.domain.ports.out.user_repository import UserRepository


def get_auth_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserORMRepository(session)


def get_register_user_use_case(user_repository: UserRepository = Depends(get_auth_user_repository)) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository)


def get_login_user_use_case(user_repository: UserRepository = Depends(get_auth_user_repository)) -> LoginUserUseCase:
    return LoginUserUseCase(user_repository)
