import logging
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.domain.ports.out.dashboard_repository import DashboardRepository
from app.application.dto.dashboard_dto import DashboardStatsDTO, ProcessStockStat

from app.infrastructure.db.models.products_orm import Product as ProductORM
from app.infrastructure.db.models.stock_alert_orm import StockAlertORM
from app.infrastructure.db.models.product_movement_orm import ProductMovementORM
from app.infrastructure.db.models.process_orm import ProcessORM
from app.infrastructure.db.models.chemical_stock_orm import ChemicalStockORM

logger = logging.getLogger(__name__)

class DashboardORMRepository(DashboardRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_stats(self, company_id: str) -> DashboardStatsDTO:
        # 1. Total Products
        total_products = self.db.query(ProductORM).filter(ProductORM.id_empresa == company_id).count()

        # 2. Low Stock Alerts
        company_uuid = UUID(company_id) if isinstance(company_id, str) else company_id
        low_stock_alerts = self.db.query(StockAlertORM).filter(
            StockAlertORM.id_empresa == company_uuid,
            StockAlertORM.estado == "activa"
        ).count()

        # 3. Movements Today
        # today in UTC
        today = datetime.now(timezone.utc).date()
        movements_today = self.db.query(ProductMovementORM).filter(
            ProductMovementORM.id_empresa == company_uuid,
            func.date(ProductMovementORM.created_at) == today
        ).count()

        # 4. Active processes
        active_processes = self.db.query(ProcessORM).filter(
            ProcessORM.id_empresa == company_id,
            ProcessORM.is_active == True
        ).count()

        # 5. Stock by Process
        # We join ChemicalStockORM with ProcessORM to get the name and sum the quantities
        results = self.db.query(
            ProcessORM.id_proceso,
            ProcessORM.nombre,
            func.sum(ChemicalStockORM.cantidad_actual).label("total")
        ).join(
            ChemicalStockORM, ProcessORM.id_proceso == ChemicalStockORM.id_proceso
        ).filter(
            ProcessORM.id_empresa == company_id
        ).group_by(
            ProcessORM.id_proceso, ProcessORM.nombre
        ).all()

        total_global_stock = sum([r.total for r in results if r.total]) or 1  # Evitar división por cero
        
        # Sort by total descending and take top 4
        sorted_results = sorted(results, key=lambda x: x.total or 0, reverse=True)[:4]
        
        stock_by_process = []
        for r in sorted_results:
            qty = float(r.total) if r.total else 0
            stock_by_process.append(
                ProcessStockStat(
                    process_id=str(r.id_proceso),
                    process_name=r.nombre,
                    total_stock=qty,
                    percentage=(qty / float(total_global_stock)) * 100
                )
            )

        return DashboardStatsDTO(
            total_products=total_products,
            low_stock_alerts=low_stock_alerts,
            movements_today=movements_today,
            active_processes=active_processes,
            stock_by_process=stock_by_process
        )
