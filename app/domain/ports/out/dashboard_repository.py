from abc import ABC, abstractmethod
from app.application.dto.dashboard_dto import DashboardStatsDTO

class DashboardRepository(ABC):
    @abstractmethod
    def get_dashboard_stats(self, company_id: str) -> DashboardStatsDTO:
        pass
