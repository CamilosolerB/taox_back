from app.domain.ports.out.company_repository import CompanyRepository

class DeleteCompanyUseCase:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def execute(self, company_id: str) -> None:
        return self.company_repository.delete_company(company_id)
