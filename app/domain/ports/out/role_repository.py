from abc import ABC, abstractmethod
from app.domain.entities.role_model import Role


class RoleRepository(ABC):
    @abstractmethod
    def get_all_roles(self) -> list[Role]:
        pass

    @abstractmethod
    def get_role_by_id(self, id_role: str) -> Role:
        pass

    @abstractmethod
    def create_role(self, role: Role) -> Role:
        pass

    @abstractmethod
    def update_role(self, id_role: str, role_data: dict) -> Role:
        pass

    @abstractmethod
    def delete_role(self, id_role: str) -> None:
        pass