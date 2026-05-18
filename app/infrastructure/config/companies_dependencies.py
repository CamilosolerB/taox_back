from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.companies_orm_repository import(
    CompanyORMRepository
)
from app.infrastructure.adapters.out.user_orm_repository import UserORMRepository
from app.application.use_cases.companies_case.get_companies import GetCompaniesUseCase
from app.application.use_cases.companies_case.get_company_by_id import GetCompanyByIdUseCase
from app.application.use_cases.companies_case.create_company import CreateCompanyUseCase
from app.application.use_cases.companies_case.update_company import UpdateCompanyUseCase
from app.application.use_cases.companies_case.delete_company import DeleteCompanyUseCase
from app.domain.ports.out.company_repository import CompanyRepository
from app.domain.ports.out.user_repository import UserRepository


def get_companies_repository(session: Session = Depends(get_session)) -> CompanyRepository:
    return CompanyORMRepository(session)

def get_user_repository_for_company(session: Session = Depends(get_session)) -> UserRepository:
    return UserORMRepository(session)

def get_companies_use_case(companies_repository: CompanyRepository = Depends(get_companies_repository)) -> GetCompaniesUseCase:
    return GetCompaniesUseCase(companies_repository)

def get_company_by_id_use_case(companies_repository: CompanyRepository = Depends(get_companies_repository)) -> GetCompanyByIdUseCase:
    return GetCompanyByIdUseCase(companies_repository)

def get_create_company_use_case(
    companies_repository: CompanyRepository = Depends(get_companies_repository),
    user_repository: UserRepository = Depends(get_user_repository_for_company),
    session: Session = Depends(get_session)
) -> CreateCompanyUseCase:
    return CreateCompanyUseCase(companies_repository, user_repository, session)

def get_update_company_use_case(
    companies_repository: CompanyRepository = Depends(get_companies_repository),
    user_repository: UserRepository = Depends(get_user_repository_for_company),
    session: Session = Depends(get_session)
) -> UpdateCompanyUseCase:
    return UpdateCompanyUseCase(companies_repository, user_repository, session)

def get_delete_company_use_case(companies_repository: CompanyRepository = Depends(get_companies_repository)) -> DeleteCompanyUseCase:
    return DeleteCompanyUseCase(companies_repository)