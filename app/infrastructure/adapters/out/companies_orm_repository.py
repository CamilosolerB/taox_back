from sqlalchemy.orm import Session
from app.domain.entities.company_model import Company
from app.domain.ports.out.company_repository import CompanyRepository
from app.infrastructure.db.models.company_orm import Company as CompanyORM

class CompanyORMRepository(CompanyRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all_companies(self) -> list[Company]:
        companies = self.session.query(CompanyORM).all()
        return [
            Company(
                id_company=company.id_company,
                name=company.name,
                nit=company.nit,
                address=company.address,
                phone=company.phone,
                email=company.email,
                is_active=company.is_active
            )
            for company in companies
        ]

    def create_company(self, company: Company) -> Company:
        company_orm = CompanyORM(**company.dict())
        self.session.add(company_orm)
        self.session.commit()
        self.session.refresh(company_orm)
        return Company(
            id_company=company_orm.id_company,
            name=company_orm.name,
            nit=company_orm.nit,
            address=company_orm.address,
            phone=company_orm.phone,
            email=company_orm.email,
            is_active=company_orm.is_active
        )

    def update_company(self, id_company: str, company_data: dict) -> Company:
        company_orm = self.session.query(CompanyORM).filter(CompanyORM.id_company == id_company).first()
        if company_orm is None:
            return None
        for key, value in company_data.items():
            if value is not None:
                setattr(company_orm, key, value)
        self.session.commit()
        self.session.refresh(company_orm)
        return Company(
            id_company=company_orm.id_company,
            name=company_orm.name,
            nit=company_orm.nit,
            address=company_orm.address,
            phone=company_orm.phone,
            email=company_orm.email,
            is_active=company_orm.is_active
        )

    def delete_company(self, id_company: str) -> None:
        company_orm = self.session.query(CompanyORM).filter(CompanyORM.id_company == id_company).first()
        self.session.delete(company_orm)
        self.session.commit()

    def get_company_by_id(self, id_company: str) -> Company:
        company_orm = self.session.query(CompanyORM).filter(CompanyORM.id_company == id_company).first()
        return Company(
            id_company=company_orm.id_company,
            name=company_orm.name,
            nit=company_orm.nit,
            address=company_orm.address,
            phone=company_orm.phone,
            email=company_orm.email,
            is_active=company_orm.is_active
        )

    def get_company_by_nit(self, nit: str) -> Company:
        company_orm = self.session.query(CompanyORM).filter(CompanyORM.nit == nit).first()
        return Company(
            id_company=company_orm.id_company,
            name=company_orm.name,
            nit=company_orm.nit,
            address=company_orm.address,
            phone=company_orm.phone,
            email=company_orm.email,
            is_active=company_orm.is_active
        )