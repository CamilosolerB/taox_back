from pydantic import BaseModel, ConfigDict
from uuid import UUID
from app.application.dto.role_dto.role_dto import RoleDTO
from app.application.dto.companies_dto.companies_dto import CompanyDTO


class UserWithRelationsDTO(BaseModel):
    id_user: UUID
    username: str
    email: str
    password: str
    is_active: bool
    role: RoleDTO | None = None
    company: CompanyDTO | None = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_relations(cls, user_orm):
        """
        Crea un UserWithRelationsDTO desde un ORM de usuario que tiene las relaciones cargadas
        """
        role_dto = None
        company_dto = None
        
        if hasattr(user_orm, 'role') and user_orm.role:
            role_dto = RoleDTO.from_entity(user_orm.role)
        
        if hasattr(user_orm, 'company') and user_orm.company:
            company_dto = CompanyDTO.from_entity(user_orm.company)
        
        return cls(
            id_user=user_orm.id_user,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            is_active=user_orm.is_active,
            role=role_dto,
            company=company_dto
        )
