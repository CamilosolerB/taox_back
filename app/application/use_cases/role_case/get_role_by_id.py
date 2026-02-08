from app.domain.ports.out.role_repository import RoleRepository
from app.domain.entities.role_model import Role

class GetRoleByIdUseCase:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def execute(self, role_id: str) -> Role:
        return self.role_repository.get_role_by_id(role_id)
