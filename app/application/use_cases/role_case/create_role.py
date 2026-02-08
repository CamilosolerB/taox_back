from app.domain.ports.out.role_repository import RoleRepository
from app.domain.entities.role_model import Role

class CreateRoleUseCase:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def execute(self, role: Role) -> Role:
        return self.role_repository.create_role(role)
