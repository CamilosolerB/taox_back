from abc import ABC, abstractmethod
from app.domain.entities.user_model import User

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, id_user: str) -> User:
        pass

    @abstractmethod
    def update_user(self, id_user: str, user_data: dict) -> User:
        pass

    @abstractmethod
    def delete_user(self, id_user: str) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass
