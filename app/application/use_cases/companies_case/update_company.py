from app.domain.ports.out.company_repository import CompanyRepository
from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.company_model import Company
from app.core.security import hash_password
from app.infrastructure.db.models.role_orm import Role as RoleORM
from app.infrastructure.db.models.user_orm import User as UserORM
from sqlalchemy.orm import Session

class UpdateCompanyUseCase:
    def __init__(
        self, 
        company_repository: CompanyRepository,
        user_repository: UserRepository,
        db: Session
    ):
        self.company_repository = company_repository
        self.user_repository = user_repository
        self.db = db

    def execute(self, company_id: str, company_data: dict) -> Company:
        # Extraer datos de admin si existen
        admin_username = company_data.pop("admin_username", None)
        admin_email = company_data.pop("admin_email", None)
        admin_password = company_data.pop("admin_password", None)

        # 1. Actualizar la empresa
        updated_company = self.company_repository.update_company(company_id, company_data)

        # 2. Actualizar el admin si se proporcionaron datos
        if admin_username or admin_email or admin_password:
            # Buscar el rol company_Admin
            role_orm = self.db.query(RoleORM).filter(RoleORM.name == "company_Admin").first()
            if role_orm:
                # Buscar el usuario admin de esta empresa
                user_orm = self.db.query(UserORM).filter(
                    UserORM.company_id == company_id,
                    UserORM.role_id == role_orm.id_role
                ).first()

                if user_orm:
                    update_fields = {}
                    if admin_username:
                        update_fields["username"] = admin_username
                    if admin_email:
                        update_fields["email"] = admin_email
                    if admin_password:
                        update_fields["password"] = hash_password(admin_password)
                    
                    if update_fields:
                        self.user_repository.update_user(str(user_orm.id_user), update_fields)

        return updated_company
