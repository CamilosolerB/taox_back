from app.domain.ports.out.company_repository import CompanyRepository
from app.domain.entities.company_model import Company

class CreateCompanyUseCase:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def execute(self, company: Company) -> Company:
        if self.company_repository.get_company_by_nit(company.nit) is not None:
            raise Exception("Company with this NIT already exists")
        return self.company_repository.create_company(company)
