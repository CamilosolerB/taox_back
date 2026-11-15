"""
Use case: notificar una alerta de stock por los canales externos configurados.

Se invoca tras crear una alerta. Crea una conversación por cada cuenta vinculada
de la empresa y envía el aviso por el canal correspondiente. Es tolerante a fallos:
un error de entrega nunca debe interrumpir la creación del movimiento.
"""
import logging

from app.domain.entities.copilot_models import CopilotConversation, CopilotMessage
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.copilot_repository import CopilotRepository
from app.domain.ports.out.notification_channel import NotificationChannel
from app.domain.ports.out.telegram_repository import TelegramRepository

logger = logging.getLogger(__name__)

TIPO_LABEL = {
    "stock_critico": "🔴 Stock crítico",
    "stock_bajo": "🟡 Stock bajo",
    "exceso": "🟢 Exceso de stock",
}


class NotifyStockAlertUseCase:
    """Envía avisos de alertas de stock a las cuentas vinculadas de la empresa."""

    def __init__(
        self,
        copilot_repository: CopilotRepository,
        telegram_repository: TelegramRepository,
        channel: NotificationChannel,
    ):
        self.copilot_repository = copilot_repository
        self.telegram_repository = telegram_repository
        self.channel = channel

    def execute(self, alert: StockAlert) -> int:
        if alert is None or alert.id_empresa is None:
            return 0
        if not self.channel.is_enabled:
            logger.info("Canal %s deshabilitado; no se notifica la alerta", self.channel.channel_name)
            return 0

        try:
            accounts = self.telegram_repository.get_accounts_by_company(str(alert.id_empresa)) or []
        except Exception as exc:  # pragma: no cover - defensivo
            logger.error(f"Error obteniendo cuentas para notificar alerta: {exc}")
            return 0

        if not accounts:
            return 0

        text = self._format_message(alert)
        sent = 0
        for account in accounts:
            try:
                conversation = self.copilot_repository.create_conversation(
                    CopilotConversation(
                        id_empresa=alert.id_empresa,
                        id_usuario=account.user_id,
                        canal=self.channel.channel_name,
                        canal_chat_id=str(account.chat_id),
                        alerta_id=alert.id_alerta,
                        codigo_producto=alert.codigo_producto,
                        titulo=f"Alerta #{alert.id_alerta} - {alert.codigo_producto}",
                    )
                )
                self.copilot_repository.add_message(
                    CopilotMessage(
                        id_conversation=conversation.id_conversation,
                        rol="assistant",
                        contenido=text,
                        canal=self.channel.channel_name,
                    )
                )
                if self.channel.send_message(str(account.chat_id), text):
                    sent += 1
            except Exception as exc:  # pragma: no cover - defensivo
                logger.error(f"Error notificando alerta a chat {account.chat_id}: {exc}")

        logger.info(f"Alerta #{alert.id_alerta} notificada a {sent} cuenta(s)")
        return sent

    def _format_message(self, alert: StockAlert) -> str:
        label = TIPO_LABEL.get(alert.tipo_alerta, alert.tipo_alerta)
        lines = [
            f"<b>{label}</b>",
            f"Producto: <b>{alert.codigo_producto}</b>",
            f"Cantidad actual: {alert.cantidad_actual} (referencia: {alert.cantidad_referencia})",
        ]
        if alert.descripcion:
            lines.append(f"Detalle: {alert.descripcion}")
        lines.append("")
        lines.append(
            "Responde a este mensaje y el copiloto te ayudará a preparar la reposición."
        )
        return "\n".join(lines)
