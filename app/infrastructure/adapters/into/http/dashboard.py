from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.config.dashboard_dependencies import get_dashboard_stats_use_case
from app.application.use_cases.dashboard_case.get_dashboard_stats import GetDashboardStatsUseCase
from app.application.dto.dashboard_dto import DashboardStatsDTO

router = APIRouter(prefix="/companies/{company_id}/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStatsDTO, summary="Obtener estadísticas principales del dashboard")
def get_dashboard_stats(
    company_id: str,
    use_case: GetDashboardStatsUseCase = Depends(get_dashboard_stats_use_case)
):
    try:
        stats = use_case.execute(company_id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )
