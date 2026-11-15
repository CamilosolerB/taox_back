"""
Use case: enviar un mensaje al copiloto y obtener su respuesta.

Ensambla el contexto de la empresa (alertas activas y producto asociado),
invoca el proveedor LLM y persiste la conversación. Si el modelo propone un
borrador de reabastecimiento, se crea y se vincula a la conversación.
"""
import json
import logging
import re
from typing import List, Optional
from uuid import UUID

from app.domain.entities.copilot_models import (
    CopilotConversation,
    CopilotMessage,
    CopilotReply,
    ReplenishmentDraft,
)
from app.domain.exceptions.copilot_exceptions import LlmProviderError
from app.domain.ports.out.copilot_repository import CopilotRepository
from app.domain.ports.out.llm_provider import LlmProvider
from app.domain.ports.out.product_repository import ProductRepository
from app.domain.ports.out.replenishment_repository import ReplenishmentRepository
from app.domain.ports.out.stock_alert_repository import StockAlertRepository

logger = logging.getLogger(__name__)

ACTION_BLOCK_PATTERN = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)

SYSTEM_PROMPT_TEMPLATE = """\
Eres el copiloto de TAOX, un asistente experto en gestión de inventario y \
abastecimiento para plantas de tratamiento de agua. Ayudas a los administradores \
a interpretar alertas de stock, priorizar reposiciones y preparar borradores de \
reabastecimiento para revisión humana.

Reglas:
- Responde en español, de forma clara y breve.
- Basa tus respuestas en el contexto proporcionado. No inventes datos.
- Nunca ejecutes compras ni movimientos de inventario: solo propones borradores \
que un humano debe revisar.
- Si el usuario pide preparar una reposición, responde con tu recomendación y, \
además, incluye EXACTAMENTE un bloque JSON con este formato:

```json
{{"action": "replenishment_draft", "codigo_producto": "<codigo>", "cantidad_sugerida": <numero>, "unidad_medida": "<unidad>", "proveedor_sugerido": "<proveedor o null>", "notas": "<justificacion breve>"}}
```

Contexto de la empresa:
{context}
"""


class SendChatMessageUseCase:
    """Orquesta un turno de conversación con el copiloto."""

    def __init__(
        self,
        copilot_repository: CopilotRepository,
        alert_repository: StockAlertRepository,
        product_repository: ProductRepository,
        replenishment_repository: ReplenishmentRepository,
        llm_provider: LlmProvider,
    ):
        self.copilot_repository = copilot_repository
        self.alert_repository = alert_repository
        self.product_repository = product_repository
        self.replenishment_repository = replenishment_repository
        self.llm_provider = llm_provider

    def execute(
        self,
        company_id: str,
        user_id: Optional[str],
        message: str,
        conversation_id: Optional[UUID] = None,
        alerta_id: Optional[int] = None,
        codigo_producto: Optional[str] = None,
        canal: str = "web",
    ) -> CopilotReply:
        conversation = self._resolve_conversation(
            company_id=company_id,
            user_id=user_id,
            conversation_id=conversation_id,
            alerta_id=alerta_id,
            codigo_producto=codigo_producto,
            canal=canal,
        )

        self.copilot_repository.add_message(
            CopilotMessage(
                id_conversation=conversation.id_conversation,
                rol="user",
                contenido=message,
                canal=canal,
            )
        )

        context = self._build_context(company_id, conversation)
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
        history = self._build_history(conversation.id_conversation)

        try:
            llm_result = self.llm_provider.generate(system_prompt, history)
            reply_text = llm_result.content
            provider = llm_result.provider
            model = llm_result.model
        except LlmProviderError as exc:
            logger.error(f"Fallo del proveedor LLM: {exc}")
            reply_text = (
                "No pude contactar al proveedor de IA en este momento. "
                "Vuelve a intentarlo en unos minutos."
            )
            provider = "error"
            model = "-"

        visible_reply, action = self._split_action(reply_text)
        draft = self._maybe_create_draft(action, conversation, user_id)

        self.copilot_repository.add_message(
            CopilotMessage(
                id_conversation=conversation.id_conversation,
                rol="assistant",
                contenido=visible_reply,
                canal=canal,
                proveedor=provider,
                modelo=model,
            )
        )
        self.copilot_repository.update_conversation(
            conversation.id_conversation, {"updated_at": self._now()}
        )

        return CopilotReply(
            reply=visible_reply,
            provider=provider,
            model=model,
            conversation_id=conversation.id_conversation,
            replenishment_draft=draft,
        )

    # --- helpers ---
    def _resolve_conversation(
        self,
        company_id: str,
        user_id: Optional[str],
        conversation_id: Optional[UUID],
        alerta_id: Optional[int],
        codigo_producto: Optional[str],
        canal: str,
    ) -> CopilotConversation:
        if conversation_id is not None:
            existing = self.copilot_repository.get_conversation(conversation_id, company_id)
            if existing is None:
                raise ValueError("Conversación no encontrada para esta empresa")
            return existing

        return self.copilot_repository.create_conversation(
            CopilotConversation(
                id_empresa=company_id,
                id_usuario=user_id,
                canal=canal,
                alerta_id=alerta_id,
                codigo_producto=codigo_producto,
                titulo=codigo_producto or "Conversación con el copiloto",
            )
        )

    def _build_context(self, company_id: str, conversation: CopilotConversation) -> str:
        lines: List[str] = []

        try:
            alerts = self.alert_repository.get_active_alerts(company_id) or []
        except Exception as exc:  # pragma: no cover - defensivo
            logger.error(f"Error cargando alertas para contexto: {exc}")
            alerts = []

        if alerts:
            lines.append("Alertas activas:")
            for alert in alerts[:20]:
                lines.append(
                    f"- Alerta #{alert.id_alerta} | producto {alert.codigo_producto} | "
                    f"tipo {alert.tipo_alerta} | actual {alert.cantidad_actual} | "
                    f"referencia {alert.cantidad_referencia} | {alert.descripcion or ''}"
                )
        else:
            lines.append("Alertas activas: ninguna.")

        codigo = conversation.codigo_producto
        if codigo:
            try:
                product = self.product_repository.get_product_by_id(codigo)
            except Exception as exc:  # pragma: no cover - defensivo
                logger.error(f"Error cargando producto para contexto: {exc}")
                product = None
            if product:
                lines.append("")
                lines.append(f"Producto en foco ({codigo}):")
                lines.append(f"- Nombre: {getattr(product, 'name', codigo)}")
                lines.append(f"- Unidad: {getattr(product, 'unit_measure', 'n/d')}")
                lines.append(f"- Precio unitario: {getattr(product, 'unit_price', 'n/d')}")
                lines.append(f"- Límite crítico: {getattr(product, 'limite_critico', 'n/d')}")
                lines.append(f"- Lead time (días): {getattr(product, 'lead_time_days', 'n/d')}")
                lines.append(f"- Reabastecimiento: {getattr(product, 'restorage', 'n/d')}")

        if conversation.alerta_id:
            lines.append("")
            lines.append(f"Conversación vinculada a la alerta #{conversation.alerta_id}.")

        return "\n".join(lines)

    def _build_history(self, conversation_id: UUID) -> List[dict]:
        messages = self.copilot_repository.get_recent_messages(conversation_id, limit=20)
        history = []
        for msg in messages:
            if msg.rol in ("user", "assistant"):
                history.append({"role": msg.rol, "content": msg.contenido})
        return history

    def _split_action(self, text: str):
        match = ACTION_BLOCK_PATTERN.search(text)
        if not match:
            return text.strip(), None
        visible = (text[: match.start()] + text[match.end() :]).strip()
        try:
            action = json.loads(match.group(1))
        except json.JSONDecodeError:
            return text.strip(), None
        if not isinstance(action, dict) or action.get("action") != "replenishment_draft":
            return text.strip(), None
        return visible or text.strip(), action

    def _maybe_create_draft(
        self, action: Optional[dict], conversation: CopilotConversation, user_id: Optional[str]
    ) -> Optional[ReplenishmentDraft]:
        if not action:
            return None

        codigo = action.get("codigo_producto") or conversation.codigo_producto
        if not codigo:
            logger.warning("Acción de reposición sin codigo_producto; se ignora")
            return None

        try:
            cantidad = action.get("cantidad_sugerida")
            draft = ReplenishmentDraft(
                id_empresa=conversation.id_empresa,
                codigo_producto=str(codigo),
                alerta_id=conversation.alerta_id,
                id_conversation=conversation.id_conversation,
                cantidad_sugerida=float(cantidad) if cantidad is not None else None,
                unidad_medida=action.get("unidad_medida"),
                proveedor_sugerido=action.get("proveedor_sugerido"),
                notas=action.get("notas"),
                created_by=user_id,
            )
        except (TypeError, ValueError) as exc:
            logger.warning(f"Acción de reposición inválida: {exc}")
            return None

        return self.replenishment_repository.create_draft(draft)

    @staticmethod
    def _now():
        from datetime import datetime

        return datetime.utcnow()
