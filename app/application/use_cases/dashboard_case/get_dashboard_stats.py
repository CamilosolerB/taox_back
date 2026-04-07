from app.domain.ports.out.dashboard_repository import DashboardRepository
from app.application.dto.dashboard_dto import DashboardStatsDTO

class GetDashboardStatsUseCase:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.dashboard_repository = dashboard_repository

    def execute(self, company_id: str) -> DashboardStatsDTO:
        return self.dashboard_repository.get_dashboard_stats(company_id)
