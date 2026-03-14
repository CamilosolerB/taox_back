"""
Configuración de dependencias para Stock Alert
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.stock_alert_repository_orm import StockAlertORMRepository
from app.application.use_cases.stock_alert_case import (
    GetAllAlertsUseCase,
    GetAlertByIdUseCase,
    GetActiveAlertsUseCase,
    CreateAlertUseCase,
    UpdateAlertUseCase,
    ResolveAlertUseCase,
    DeleteAlertUseCase
)
from app.domain.ports.out.stock_alert_repository import StockAlertRepository


def get_alert_repository(session: Session = Depends(get_session)) -> StockAlertRepository:
    """Inyecta el repositorio de alertas de stock"""
    return StockAlertORMRepository(session)


def get_get_all_alerts_use_case(
    repository: StockAlertRepository = Depends(get_alert_repository)
) -> GetAllAlertsUseCase:
    """Inyecta el caso de uso para obtener todas las alertas"""
    return GetAllAlertsUseCase(repository)


def get_get_alert_by_id_use_case(
    repository: StockAlertRepository = Depends(get_alert_repository)
) -> GetAlertByIdUseCase:
    """Inyecta el caso de uso para obtener una alerta por ID"""
    return GetAlertByIdUseCase(repository)


def get_get_active_alerts_use_case(
    repository: StockAlertRepository = Depends(get_alert_repository)
) -> GetActiveAlertsUseCase:
    """Inyecta el caso de uso para obtener alertas activas"""
    return GetActiveAlertsUseCase(repository)


def get_create_alert_use_case(
    repository: StockAlertRepository = Depends(get_alert_repository)
) -> CreateAlertUseCase:
    """Inyecta el caso de uso para crear una alerta"""
    return CreateAlertUseCase(repository)


def get_update_alert_use_case(
    repository: StockAlertRepository = Depends(get_alert_repository)
) -> UpdateAlertUseCase:
    """Inyecta el caso de uso para actualizar una alerta"""
    return UpdateAlertUseCase(repository)


def get_resolve_alert_use_case(
    repository: StockAlertRepository = Depends(get_alert_repository)
) -> ResolveAlertUseCase:
    """Inyecta el caso de uso para resolver una alerta"""
    return ResolveAlertUseCase(repository)


def get_delete_alert_use_case(
    repository: StockAlertRepository = Depends(get_alert_repository)
) -> DeleteAlertUseCase:
    """Inyecta el caso de uso para eliminar una alerta"""
    return DeleteAlertUseCase(repository)
