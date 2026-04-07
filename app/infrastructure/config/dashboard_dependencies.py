from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.dashboard_repository_orm import DashboardORMRepository
from app.domain.ports.out.dashboard_repository import DashboardRepository
from app.application.use_cases.dashboard_case.get_dashboard_stats import GetDashboardStatsUseCase

def get_dashboard_repository(session: Session = Depends(get_session)) -> DashboardRepository:
    return DashboardORMRepository(session)

def get_dashboard_stats_use_case(repository: DashboardRepository = Depends(get_dashboard_repository)) -> GetDashboardStatsUseCase:
    return GetDashboardStatsUseCase(repository)
