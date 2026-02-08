from app.domain.ports.out.user_repository import UserRepository

class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> None:
        return self.user_repository.delete_user(user_id)
