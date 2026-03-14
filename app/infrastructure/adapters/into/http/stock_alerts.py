"""
HTTP endpoints para Stock Alert
"""
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.application.dto.stock_alert_dto import StockAlertCreateDTO, StockAlertUpdateDTO, StockAlertResponseDTO
from app.application.use_cases.stock_alert_case import (
    GetAllAlertsUseCase,
    GetAlertByIdUseCase,
    GetActiveAlertsUseCase,
    CreateAlertUseCase,
    UpdateAlertUseCase,
    ResolveAlertUseCase,
    DeleteAlertUseCase
)
from app.infrastructure.config.stock_alert_dependencies import (
    get_get_all_alerts_use_case,
    get_get_alert_by_id_use_case,
    get_get_active_alerts_use_case,
    get_create_alert_use_case,
    get_update_alert_use_case,
    get_resolve_alert_use_case,
    get_delete_alert_use_case
)

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[StockAlertResponseDTO], status_code=status.HTTP_200_OK)
def get_all_alerts(
    company_id: str,
    use_case: GetAllAlertsUseCase = Depends(get_get_all_alerts_use_case)
):
    """Obtiene todas las alertas de una empresa"""
    alerts = use_case.execute(company_id)
    return [StockAlertResponseDTO.model_validate(a) for a in alerts]


@router.get("/active", response_model=List[StockAlertResponseDTO], status_code=status.HTTP_200_OK)
def get_active_alerts(
    company_id: str,
    use_case: GetActiveAlertsUseCase = Depends(get_get_active_alerts_use_case)
):
    """Obtiene todas las alertas activas de una empresa.
    
    Útil para tablero de control de alertas en tiempo real
    """
    alerts = use_case.execute(company_id)
    return [StockAlertResponseDTO.model_validate(a) for a in alerts]


@router.get("/{id_alerta}", response_model=StockAlertResponseDTO, status_code=status.HTTP_200_OK)
def get_alert_by_id(
    id_alerta: int,
    company_id: str,
    use_case: GetAlertByIdUseCase = Depends(get_get_alert_by_id_use_case)
):
    """Obtiene una alerta por ID"""
    try:
        alert = use_case.execute(id_alerta, company_id)
        return StockAlertResponseDTO.model_validate(alert)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=StockAlertResponseDTO, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert_dto: StockAlertCreateDTO,
    use_case: CreateAlertUseCase = Depends(get_create_alert_use_case)
):
    """Crea una nueva alerta de stock"""
    alert = use_case.execute(alert_dto)
    return StockAlertResponseDTO.model_validate(alert)


@router.put("/{id_alerta}", response_model=StockAlertResponseDTO, status_code=status.HTTP_200_OK)
def update_alert(
    id_alerta: int,
    alert_dto: StockAlertUpdateDTO,
    use_case: UpdateAlertUseCase = Depends(get_update_alert_use_case)
):
    """Actualiza una alerta"""
    try:
        alert = use_case.execute(id_alerta, alert_dto)
        return StockAlertResponseDTO.model_validate(alert)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{id_alerta}/resolve", response_model=StockAlertResponseDTO, status_code=status.HTTP_200_OK)
def resolve_alert(
    id_alerta: int,
    use_case: ResolveAlertUseCase = Depends(get_resolve_alert_use_case)
):
    """Marca una alerta como resuelta. Registra el timestamp de resolución"""
    try:
        alert = use_case.execute(id_alerta)
        return StockAlertResponseDTO.model_validate(alert)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id_alerta}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    id_alerta: int,
    company_id: str,
    use_case: DeleteAlertUseCase = Depends(get_delete_alert_use_case)
):
    """Elimina una alerta"""
    try:
        use_case.execute(id_alerta, company_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
