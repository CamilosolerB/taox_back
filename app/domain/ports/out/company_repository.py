from abc import ABC, abstractmethod
from app.domain.entities.company_model import Company

class CompanyRepository(ABC):
    @abstractmethod
    def get_all_companies(self) -> list[Company]:
        pass

    @abstractmethod
    def create_company(self, company: Company) -> Company:
        pass

    @abstractmethod
    def update_company(self, id_company: str, company_data: dict) -> Company:
        pass

    @abstractmethod
    def delete_company(self, id_company: str) -> None:
        pass

    @abstractmethod
    def get_company_by_id(self, id_company: str) -> Company:
        pass

    @abstractmethod
    def get_company_by_nit(self, nit: str) -> Company:
        pass

    