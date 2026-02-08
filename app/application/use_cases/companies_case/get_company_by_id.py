from app.domain.ports.out.company_repository import CompanyRepository
from app.domain.entities.company_model import Company

class GetCompanyByIdUseCase:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def execute(self, company_id: str) -> Company:
        return self.company_repository.get_company_by_id(company_id)
