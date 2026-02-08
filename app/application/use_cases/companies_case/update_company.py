from app.domain.ports.out.company_repository import CompanyRepository
from app.domain.entities.company_model import Company

class UpdateCompanyUseCase:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def execute(self, company_id: str, company_data: dict) -> Company:
        return self.company_repository.update_company(company_id, company_data)
