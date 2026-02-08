from app.domain.ports.out.role_repository import RoleRepository
from app.domain.entities.role_model import Role

class GetRolesUseCase:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def execute(self) -> list[Role]:
        return self.role_repository.get_all_roles()