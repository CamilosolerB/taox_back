from fastapi import APIRouter, Depends
from uuid import UUID
from app.application.dto.users_dto.create_user_dto import CreateUserDTO
from app.application.dto.users_dto.update_user_dto import UpdateUserDTO
from app.application.dto.users_dto.user_dto import UserDTO
from app.application.dto.users_dto.user_detail_dto import UserDetailDTO
from app.application.dto.users_dto.user_with_relations_dto import UserWithRelationsDTO
from app.application.use_cases.users_case.create_user import CreateUserUseCase
from app.application.use_cases.users_case.get_all_users import GetAllUsersUseCase
from app.application.use_cases.users_case.get_user_by_id import GetUserByIdUseCase
from app.application.use_cases.users_case.update_user import UpdateUserUseCase
from app.application.use_cases.users_case.delete_user import DeleteUserUseCase
from app.infrastructure.config.dependencies import (
    get_create_user_use_case,
    get_all_users_use_case,
    get_user_by_id_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
    get_user_repository
)
from app.core.middleware.auth_middleware import (
    get_current_user,
    require_admin
)
from app.domain.entities.user_model import User
from app.domain.ports.out.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserDTO, dependencies=[Depends(require_admin)])
def create_user(
    create_user_dto: CreateUserDTO, 
    create_user_use_case: CreateUserUseCase = Depends(get_create_user_use_case),
    payload: dict = Depends(require_admin)
):
    """
    Crea un nuevo usuario (requiere rol de administrador)
    """
    user = create_user_use_case.execute(User(
        id_user=None,
        username=create_user_dto.username,
        email=create_user_dto.email,
        password=create_user_dto.password,
        is_active=create_user_dto.is_active,
        role_id=create_user_dto.role_id,
        company_id=create_user_dto.company_id
    ))
    return UserDTO.from_entity(user)

@router.get("/", response_model=list[UserDetailDTO], dependencies=[Depends(get_current_user)])
def get_all_users(
    get_all_users_use_case: GetAllUsersUseCase = Depends(get_all_users_use_case),
    payload: dict = Depends(get_current_user)
):
    """
    Lista todos los usuarios (requiere autenticación)
    """
    users = get_all_users_use_case.execute()
    return [UserDetailDTO.from_entity(user) for user in users]

@router.get("/{user_id}", response_model=UserWithRelationsDTO, dependencies=[Depends(get_current_user)])
def get_user_by_id(
    user_id: UUID, 
    user_repository: UserRepository = Depends(get_user_repository),
    payload: dict = Depends(get_current_user)
):
    """
    Obtiene un usuario específico con sus relaciones de rol y company
    (requiere autenticación)
    """
    user_orm = user_repository.get_user_by_id_orm(str(user_id))
    if user_orm is None:
        return {"error": "User not found"}
    return UserWithRelationsDTO.from_orm_with_relations(user_orm)

@router.put("/{user_id}", response_model=UserDTO, dependencies=[Depends(require_admin)])
def update_user(
    user_id: UUID, 
    update_user_dto: UpdateUserDTO,
    update_user_use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
    payload: dict = Depends(require_admin)
):
    """
    Actualiza un usuario (requiere rol de administrador)
    """
    user_data = update_user_dto.model_dump(exclude_unset=True)
    user = update_user_use_case.execute(str(user_id), user_data)
    return UserDTO.from_entity(user)

@router.delete("/{user_id}", dependencies=[Depends(require_admin)])
def delete_user(
    user_id: UUID,
    delete_user_use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
    payload: dict = Depends(require_admin)
):
    """
    Elimina un usuario (requiere rol de administrador)
    """
    delete_user_use_case.execute(str(user_id))
    return {"message": "User deleted successfully"}