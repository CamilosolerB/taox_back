from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.user_model import User
from typing import Optional

class GetAllUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, role_names: Optional[list[str]] = None, company_id: Optional[str] = None) -> list[User]:
        if role_names:
            users = self.user_repository.get_users_by_role_names(role_names)
        else:
            users = self.user_repository.get_all_users()
            
        if company_id:
            return [u for u in users if str(u.company_id) == company_id]
        return users
