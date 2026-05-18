from app.domain.ports.out.company_repository import CompanyRepository
from app.domain.ports.out.user_repository import UserRepository
from app.domain.entities.company_model import Company
from app.core.security import hash_password
from app.infrastructure.db.models.role_orm import Role as RoleORM
from app.infrastructure.db.models.user_orm import User as UserORM
from sqlalchemy.orm import Session


class CreateCompanyUseCase:
    def __init__(
        self,
        company_repository: CompanyRepository,
        user_repository: UserRepository,
        db: Session
    ):
        self.company_repository = company_repository
        self.user_repository = user_repository
        self.db = db

    def execute(
        self,
        company: Company,
        admin_username: str,
        admin_email: str,
        admin_password: str
    ) -> Company:
        if self.company_repository.get_company_by_nit(company.nit) is not None:
            raise Exception("Company with this NIT already exists")

        # 1. Crear la empresa
        created_company = self.company_repository.create_company(company)

        # 2. Buscar el rol company_Admin
        role_orm = self.db.query(RoleORM).filter(RoleORM.name == "company_Admin").first()
        if role_orm is None:
            raise Exception("Role 'company_Admin' not found. Please create it first.")

        # 3. Verificar que el email del admin no exista
        if self.user_repository.get_user_by_email(admin_email) is not None:
            raise Exception(f"A user with email '{admin_email}' already exists.")

        # 4. Crear el usuario admin vinculado a la empresa
        hashed_password = hash_password(admin_password)
        from app.domain.entities.user_model import User
        admin_user = User(
            id_user=None,
            username=admin_username,
            email=admin_email,
            password=hashed_password,
            is_active=True,
            role_id=role_orm.id_role,
            company_id=created_company.id_company
        )
        self.user_repository.create_user(admin_user)

        return created_company
