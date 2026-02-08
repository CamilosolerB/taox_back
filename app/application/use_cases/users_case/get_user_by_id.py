from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User

class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> User:
        return self.user_repository.get_user_by_id(user_id)
