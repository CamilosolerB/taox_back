from fastapi import APIRouter, Depends
from uuid import UUID
from app.application.dto.role_dto.role_dto import RoleDTO
from app.application.dto.role_dto.create_role_dto import CreateRoleDTO
from app.application.dto.role_dto.update_role_dto import UpdateRoleDTO
from app.application.use_cases.role_case.get_roles import GetRolesUseCase
from app.application.use_cases.role_case.get_role_by_id import GetRoleByIdUseCase
from app.application.use_cases.role_case.create_role import CreateRoleUseCase
from app.application.use_cases.role_case.update_role import UpdateRoleUseCase
from app.application.use_cases.role_case.delete_role import DeleteRoleUseCase
from app.infrastructure.config.role_dependencies import (
    get_get_roles_use_case,
    get_role_by_id_use_case,
    get_create_role_use_case,
    get_update_role_use_case,
    get_delete_role_use_case
)
from app.domain.entities.role_model import Role

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=list[RoleDTO])
def get_roles(get_roles_use_case: GetRolesUseCase = Depends(get_get_roles_use_case)):
    roles = get_roles_use_case.execute()
    return [RoleDTO.from_entity(role) for role in roles]

@router.get("/{role_id}", response_model=RoleDTO)
def get_role_by_id(
    role_id: UUID,
    get_role_by_id_use_case: GetRoleByIdUseCase = Depends(get_role_by_id_use_case)
):
    role = get_role_by_id_use_case.execute(str(role_id))
    return RoleDTO.from_entity(role)

@router.post("/", response_model=RoleDTO)
def create_role(
    create_role_dto: CreateRoleDTO,
    create_role_use_case: CreateRoleUseCase = Depends(get_create_role_use_case)
):
    role = create_role_use_case.execute(Role(
        id_role=None,
        name=create_role_dto.name
    ))
    return RoleDTO.from_entity(role)

@router.put("/{role_id}", response_model=RoleDTO)
def update_role(
    role_id: UUID,
    update_role_dto: UpdateRoleDTO,
    update_role_use_case: UpdateRoleUseCase = Depends(get_update_role_use_case)
):
    role_data = update_role_dto.model_dump(exclude_unset=True)
    role = update_role_use_case.execute(str(role_id), role_data)
    return RoleDTO.from_entity(role)

@router.delete("/{role_id}")
def delete_role(
    role_id: UUID,
    delete_role_use_case: DeleteRoleUseCase = Depends(get_delete_role_use_case)
):
    delete_role_use_case.execute(str(role_id))
    return {"message": "Role deleted successfully"}