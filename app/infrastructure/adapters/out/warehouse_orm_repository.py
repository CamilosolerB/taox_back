from sqlalchemy.orm import Session
from app.domain.entities.warehouse_model import Warehouse
from app.domain.ports.out.warehouse_repository import WarehouseRepository
from app.infrastructure.db.models.warehouse_orm import WarehouseORM


class WarehouseORMRepository(WarehouseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all_warehouses(self, company_id: str) -> list[Warehouse]:
        warehouses = self.session.query(WarehouseORM).filter(
            WarehouseORM.company_id == company_id,
            WarehouseORM.is_active == True
        ).all()
        return [
            Warehouse(
                id_warehouse=warehouse.id_warehouse,
                name=warehouse.name,
                description=warehouse.description,
                location=warehouse.location,
                is_active=warehouse.is_active,
                company_id=warehouse.company_id,
                created_at=warehouse.created_at.isoformat() if warehouse.created_at else None,
                updated_at=warehouse.updated_at.isoformat() if warehouse.updated_at else None
            )
            for warehouse in warehouses
        ]

    def get_warehouse_by_id(self, id_warehouse: str) -> Warehouse | None:
        warehouse = self.session.query(WarehouseORM).filter(
            WarehouseORM.id_warehouse == id_warehouse
        ).first()
        if warehouse is None:
            return None
        return Warehouse(
            id_warehouse=warehouse.id_warehouse,
            name=warehouse.name,
            description=warehouse.description,
            location=warehouse.location,
            is_active=warehouse.is_active,
            company_id=warehouse.company_id,
            created_at=warehouse.created_at.isoformat() if warehouse.created_at else None,
            updated_at=warehouse.updated_at.isoformat() if warehouse.updated_at else None
        )

    def get_warehouse_by_id_and_company(self, id_warehouse: str, company_id: str) -> Warehouse | None:
        warehouse = self.session.query(WarehouseORM).filter(
            WarehouseORM.id_warehouse == id_warehouse,
            WarehouseORM.company_id == company_id
        ).first()
        if warehouse is None:
            return None
        return Warehouse(
            id_warehouse=warehouse.id_warehouse,
            name=warehouse.name,
            description=warehouse.description,
            location=warehouse.location,
            is_active=warehouse.is_active,
            company_id=warehouse.company_id,
            created_at=warehouse.created_at.isoformat() if warehouse.created_at else None,
            updated_at=warehouse.updated_at.isoformat() if warehouse.updated_at else None
        )

    def create_warehouse(self, warehouse: Warehouse) -> Warehouse:
        warehouse_orm = WarehouseORM(
            name=warehouse.name,
            description=warehouse.description,
            location=warehouse.location,
            is_active=warehouse.is_active,
            company_id=warehouse.company_id
        )
        self.session.add(warehouse_orm)
        self.session.commit()
        self.session.refresh(warehouse_orm)
        return Warehouse(
            id_warehouse=warehouse_orm.id_warehouse,
            name=warehouse_orm.name,
            description=warehouse_orm.description,
            location=warehouse_orm.location,
            is_active=warehouse_orm.is_active,
            company_id=warehouse_orm.company_id,
            created_at=warehouse_orm.created_at.isoformat() if warehouse_orm.created_at else None,
            updated_at=warehouse_orm.updated_at.isoformat() if warehouse_orm.updated_at else None
        )

    def update_warehouse(self, id_warehouse: str, warehouse_data: dict) -> Warehouse | None:
        warehouse_orm = self.session.query(WarehouseORM).filter(
            WarehouseORM.id_warehouse == id_warehouse
        ).first()
        if warehouse_orm is None:
            return None
        for key, value in warehouse_data.items():
            if value is not None and hasattr(warehouse_orm, key):
                setattr(warehouse_orm, key, value)
        self.session.commit()
        self.session.refresh(warehouse_orm)
        return Warehouse(
            id_warehouse=warehouse_orm.id_warehouse,
            name=warehouse_orm.name,
            description=warehouse_orm.description,
            location=warehouse_orm.location,
            is_active=warehouse_orm.is_active,
            company_id=warehouse_orm.company_id,
            created_at=warehouse_orm.created_at.isoformat() if warehouse_orm.created_at else None,
            updated_at=warehouse_orm.updated_at.isoformat() if warehouse_orm.updated_at else None
        )

    def delete_warehouse(self, id_warehouse: str) -> None:
        warehouse_orm = self.session.query(WarehouseORM).filter(
            WarehouseORM.id_warehouse == id_warehouse
        ).first()
        if warehouse_orm:
            warehouse_orm.is_active = False
            self.session.commit()