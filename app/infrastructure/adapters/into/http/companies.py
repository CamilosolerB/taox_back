from fastapi import APIRouter, Depends
from uuid import UUID
from app.application.dto.companies_dto.companies_dto import CompanyDTO
from app.application.dto.companies_dto.create_company_dto import CreateCompanyDTO
from app.application.dto.companies_dto.update_company_dto import UpdateCompanyDTO
from app.application.use_cases.companies_case.get_companies import GetCompaniesUseCase
from app.application.use_cases.companies_case.get_company_by_id import GetCompanyByIdUseCase
from app.application.use_cases.companies_case.create_company import CreateCompanyUseCase
from app.application.use_cases.companies_case.update_company import UpdateCompanyUseCase
from app.application.use_cases.companies_case.delete_company import DeleteCompanyUseCase
from app.infrastructure.config.companies_dependencies import (
    get_companies_use_case,
    get_company_by_id_use_case,
    get_create_company_use_case,
    get_update_company_use_case,
    get_delete_company_use_case
)
from app.domain.entities.company_model import Company

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("/", response_model=list[CompanyDTO])
def get_companies(get_companies_use_case: GetCompaniesUseCase = Depends(get_companies_use_case)):
    companies = get_companies_use_case.execute()
    return [CompanyDTO.from_entity(company) for company in companies]

@router.get("/{company_id}", response_model=CompanyDTO)
def get_company_by_id(
    company_id: UUID,
    get_company_by_id_use_case: GetCompanyByIdUseCase = Depends(get_company_by_id_use_case)
):
    company = get_company_by_id_use_case.execute(str(company_id))
    return CompanyDTO.from_entity(company)

@router.post("/", response_model=CompanyDTO)
def create_company(
    create_company_dto: CreateCompanyDTO,
    create_company_use_case: CreateCompanyUseCase = Depends(get_create_company_use_case)
):
    company = create_company_use_case.execute(Company(
        id_company=None,
        name=create_company_dto.name,
        nit=create_company_dto.nit,
        address=create_company_dto.address,
        phone=create_company_dto.phone,
        email=create_company_dto.email,
        is_active=create_company_dto.is_active
    ))
    return CompanyDTO.from_entity(company)

@router.put("/{company_id}", response_model=CompanyDTO)
def update_company(
    company_id: UUID,
    update_company_dto: UpdateCompanyDTO,
    update_company_use_case: UpdateCompanyUseCase = Depends(get_update_company_use_case)
):
    company_data = update_company_dto.model_dump(exclude_unset=True)
    company = update_company_use_case.execute(str(company_id), company_data)
    return CompanyDTO.from_entity(company)

@router.delete("/{company_id}")
def delete_company(
    company_id: UUID,
    delete_company_use_case: DeleteCompanyUseCase = Depends(get_delete_company_use_case)
):
    delete_company_use_case.execute(str(company_id))
    return {"message": "Company deleted successfully"}