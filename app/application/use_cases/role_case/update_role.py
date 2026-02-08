from app.domain.ports.out.role_repository import RoleRepository
from app.domain.entities.role_model import Role

class UpdateRoleUseCase:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def execute(self, role_id: str, role_data: dict) -> Role:
        return self.role_repository.update_role(role_id, role_data)
