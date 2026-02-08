from app.domain.ports.out.role_repository import RoleRepository

class DeleteRoleUseCase:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def execute(self, role_id: str) -> None:
        return self.role_repository.delete_role(role_id)
