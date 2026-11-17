"""
Use case: generar un reporte descargable (Excel o PDF) con datos de la empresa.

Lo invoca el copiloto cuando el usuario pide un reporte/informe/exportable.
Construye las filas a partir de los repositorios, genera el archivo con
ReportService, lo guarda en el almacenamiento estático y devuelve su URL de
descarga.
"""
import logging
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple

from app.application.services.report_service import ReportService
from app.domain.ports.out.product_movement_repository import ProductMovementRepository
from app.domain.ports.out.product_repository import ProductRepository
from app.domain.ports.out.stock_alert_repository import StockAlertRepository

logger = logging.getLogger(__name__)

REPORTES_VALIDOS = {"inventario", "alertas", "movimientos"}
FORMATOS_VALIDOS = {"excel", "pdf"}

TIPO_ALERTA_LABEL = {
    "stock_critico": "Stock crítico",
    "stock_bajo": "Stock bajo",
    "exceso": "Exceso de stock",
}

TITULOS_POR_DEFECTO = {
    "inventario": "Inventario de productos",
    "alertas": "Alertas de stock activas",
    "movimientos": "Movimientos de productos",
}


class GenerateReportUseCase:
    """Genera un archivo de reporte y devuelve su URL pública de descarga."""

    def __init__(
        self,
        product_repository: ProductRepository,
        alert_repository: StockAlertRepository,
        movement_repository: ProductMovementRepository,
        public_base_url: Optional[str] = None,
    ):
        self.product_repository = product_repository
        self.alert_repository = alert_repository
        self.movement_repository = movement_repository
        self.public_base_url = (public_base_url or "").rstrip("/")

    def execute(
        self,
        company_id: str,
        tipo: str,
        formato: str,
        titulo: Optional[str] = None,
    ) -> Dict[str, Any]:
        tipo = (tipo or "").strip().lower()
        formato = (formato or "").strip().lower()

        if tipo not in REPORTES_VALIDOS:
            raise ValueError(f"Tipo de reporte no soportado: {tipo!r}")
        if formato not in FORMATOS_VALIDOS:
            raise ValueError(f"Formato de reporte no soportado: {formato!r}")

        data, default_title = self._build_data(company_id, tipo)
        title = (titulo or default_title).strip()

        if formato == "excel":
            buffer = ReportService.generate_excel(data)
            ext = "xlsx"
        else:
            buffer = ReportService.generate_pdf(data, title=title)
            ext = "pdf"

        filename = f"{tipo}-{uuid.uuid4().hex[:8]}.{ext}"
        url = self._save(buffer, filename)

        return {
            "tipo": tipo,
            "formato": formato,
            "titulo": title,
            "filename": filename,
            "url": url,
            "rows": len(data),
        }

    # --- datos ---
    def _build_data(self, company_id: str, tipo: str) -> Tuple[List[Dict[str, Any]], str]:
        if tipo == "inventario":
            return self._inventory_rows(company_id), TITULOS_POR_DEFECTO["inventario"]
        if tipo == "alertas":
            return self._alert_rows(company_id), TITULOS_POR_DEFECTO["alertas"]
        return self._movement_rows(company_id), TITULOS_POR_DEFECTO["movimientos"]

    def _inventory_rows(self, company_id: str) -> List[Dict[str, Any]]:
        try:
            products = self.product_repository.get_products_by_company_id(company_id) or []
        except Exception as exc:  # pragma: no cover - defensivo
            logger.error(f"Error cargando productos para reporte: {exc}")
            products = []

        rows: List[Dict[str, Any]] = []
        for p in products:
            rows.append(
                {
                    "Código": getattr(p, "id_product", "") or "",
                    "Producto": getattr(p, "name", "") or "",
                    "Nombre genérico": getattr(p, "generic_name", "") or "",
                    "Unidad": getattr(p, "unit_measure", "") or "",
                    "Precio unitario": getattr(p, "unit_price", "") or "",
                    "Límite crítico": getattr(p, "limite_critico", "") or "",
                    "Reposición (días)": getattr(p, "lead_time_days", "") or "",
                    "Reabastecimiento": getattr(p, "restorage", "") or "",
                }
            )
        return rows

    def _alert_rows(self, company_id: str) -> List[Dict[str, Any]]:
        try:
            alerts = self.alert_repository.get_active_alerts(company_id) or []
        except Exception as exc:  # pragma: no cover - defensivo
            logger.error(f"Error cargando alertas para reporte: {exc}")
            alerts = []

        rows: List[Dict[str, Any]] = []
        for a in alerts:
            tipo_alerta = getattr(a, "tipo_alerta", "") or ""
            rows.append(
                {
                    "Alerta": getattr(a, "id_alerta", "") or "",
                    "Producto": getattr(a, "codigo_producto", "") or "",
                    "Tipo": TIPO_ALERTA_LABEL.get(tipo_alerta, tipo_alerta),
                    "Cantidad actual": getattr(a, "cantidad_actual", "") or "",
                    "Cantidad referencia": getattr(a, "cantidad_referencia", "") or "",
                    "Estado": getattr(a, "estado", "") or "",
                    "Descripción": getattr(a, "descripcion", "") or "",
                }
            )
        return rows

    def _movement_rows(self, company_id: str) -> List[Dict[str, Any]]:
        try:
            movements = self.movement_repository.get_all_movements(company_id) or []
        except Exception as exc:  # pragma: no cover - defensivo
            logger.error(f"Error cargando movimientos para reporte: {exc}")
            movements = []

        rows: List[Dict[str, Any]] = []
        for m in movements:
            created = getattr(m, "created_at", None)
            fecha = created.strftime("%Y-%m-%d %H:%M") if hasattr(created, "strftime") else ""
            rows.append(
                {
                    "Movimiento": getattr(m, "id_movimiento", "") or "",
                    "Producto": getattr(m, "codigo_producto", "") or "",
                    "Tipo": getattr(m, "tipo_movimiento", "") or "",
                    "Cantidad": getattr(m, "cantidad", "") or "",
                    "Estado": getattr(m, "estado", "") or "",
                    "Fecha": fecha,
                    "Notas": getattr(m, "notas", "") or "",
                }
            )
        return rows

    # --- almacenamiento ---
    def _reports_dir(self) -> str:
        if os.path.exists("/static/uploads"):
            return "/static/uploads/reports"
        return "static/uploads/reports"

    def _save(self, buffer, filename: str) -> str:
        directory = self._reports_dir()
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, filename), "wb") as fh:
            fh.write(buffer.getvalue())

        rel_path = f"/copilot/reports/{filename}"
        if self.public_base_url:
            return f"{self.public_base_url}{rel_path}"
        return rel_path
