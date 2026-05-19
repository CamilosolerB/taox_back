from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User
from app.core.security import hash_password

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user: User) -> User:
        if self.user_repository.get_user_by_email(user.email) is not None:
            raise Exception("User already exists")
        
        # Hash user password
        user.password = hash_password(user.password)
        
        return self.user_repository.create_user(user)