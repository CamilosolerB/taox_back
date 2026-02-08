from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.role_orm_repository import(
    RoleORMRepository
)
from app.application.use_cases.role_case.get_roles import GetRolesUseCase
from app.application.use_cases.role_case.get_role_by_id import GetRoleByIdUseCase
from app.application.use_cases.role_case.create_role import CreateRoleUseCase
from app.application.use_cases.role_case.update_role import UpdateRoleUseCase
from app.application.use_cases.role_case.delete_role import DeleteRoleUseCase
from app.domain.ports.out.role_repository import RoleRepository

def get_role_repository(session: Session = Depends(get_session)) -> RoleRepository:
    return RoleORMRepository(session)

def get_get_roles_use_case(role_repository: RoleRepository = Depends(get_role_repository)) -> GetRolesUseCase:
    return GetRolesUseCase(role_repository)

def get_role_by_id_use_case(role_repository: RoleRepository = Depends(get_role_repository)) -> GetRoleByIdUseCase:
    return GetRoleByIdUseCase(role_repository)

def get_create_role_use_case(role_repository: RoleRepository = Depends(get_role_repository)) -> CreateRoleUseCase:
    return CreateRoleUseCase(role_repository)

def get_update_role_use_case(role_repository: RoleRepository = Depends(get_role_repository)) -> UpdateRoleUseCase:
    return UpdateRoleUseCase(role_repository)

def get_delete_role_use_case(role_repository: RoleRepository = Depends(get_role_repository)) -> DeleteRoleUseCase:
    return DeleteRoleUseCase(role_repository)