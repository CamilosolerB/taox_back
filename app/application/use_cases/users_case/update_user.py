from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User
from app.core.security import hash_password

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str, user_data: dict) -> User:
        # If password is being updated, hash it
        if "password" in user_data and user_data["password"]:
            user_data["password"] = hash_password(user_data["password"])
        return self.user_repository.update_user(user_id, user_data)
