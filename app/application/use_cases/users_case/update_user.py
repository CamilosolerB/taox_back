from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str, user_data: dict) -> User:
        return self.user_repository.update_user(user_id, user_data)
