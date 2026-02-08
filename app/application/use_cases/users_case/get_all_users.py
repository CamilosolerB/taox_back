from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User

class GetAllUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> list[User]:
        return self.user_repository.get_all_users()
