"""
Configuración de dependencias para el Copiloto IA
"""
import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.settings import settings
from app.infrastructure.db.session import get_session
from app.infrastructure.adapters.out.copilot_repository_orm import CopilotORMRepository
from app.infrastructure.adapters.out.telegram_repository_orm import TelegramORMRepository
from app.infrastructure.adapters.out.replenishment_repository_orm import ReplenishmentORMRepository
from app.infrastructure.adapters.out.stock_alert_repository_orm import StockAlertORMRepository
from app.infrastructure.adapters.out.product_orm_repository import ProductORMRepository
from app.infrastructure.adapters.out.product_movement_repository_orm import ProductMovementORMRepository
from app.infrastructure.adapters.out.minimax_llm_provider import MiniMaxLlmProvider
from app.infrastructure.adapters.out.stub_llm_provider import StubLlmProvider
from app.infrastructure.adapters.out.telegram_channel import TelegramChannel

from app.domain.ports.out.copilot_repository import CopilotRepository
from app.domain.ports.out.telegram_repository import TelegramRepository
from app.domain.ports.out.replenishment_repository import ReplenishmentRepository
from app.domain.ports.out.stock_alert_repository import StockAlertRepository
from app.domain.ports.out.product_repository import ProductRepository
from app.domain.ports.out.product_movement_repository import ProductMovementRepository
from app.domain.ports.out.llm_provider import LlmProvider
from app.domain.ports.out.notification_channel import NotificationChannel

from app.application.use_cases.copilot_case import (
    SendChatMessageUseCase,
    GenerateReportUseCase,
    ProcessTelegramUpdateUseCase,
    NotifyStockAlertUseCase,
    CreateLinkCodeUseCase,
    GetLinkStatusUseCase,
    UnlinkTelegramUseCase,
    OpenConversationUseCase,
    GetConversationsUseCase,
    GetConversationMessagesUseCase,
    CreateReplenishmentDraftUseCase,
    GetReplenishmentDraftsUseCase,
    UpdateReplenishmentDraftUseCase,
)

logger = logging.getLogger(__name__)


def resolve_bot_link() -> str | None:
    """Resuelve el enlace público del bot a partir de la configuración."""
    if settings.TELEGRAM_BOT_LINK:
        return settings.TELEGRAM_BOT_LINK
    if settings.TELEGRAM_BOT_USERNAME:
        return f"https://t.me/{settings.TELEGRAM_BOT_USERNAME.lstrip('@')}"
    return None


# --- Repositorios ---
def get_copilot_repository(session: Session = Depends(get_session)) -> CopilotRepository:
    return CopilotORMRepository(session)


def get_telegram_repository(session: Session = Depends(get_session)) -> TelegramRepository:
    return TelegramORMRepository(session)


def get_replenishment_repository(session: Session = Depends(get_session)) -> ReplenishmentRepository:
    return ReplenishmentORMRepository(session)


def get_copilot_alert_repository(session: Session = Depends(get_session)) -> StockAlertRepository:
    return StockAlertORMRepository(session)


def get_copilot_product_repository(session: Session = Depends(get_session)) -> ProductRepository:
    return ProductORMRepository(session)


def get_copilot_movement_repository(
    session: Session = Depends(get_session),
) -> ProductMovementRepository:
    return ProductMovementORMRepository(session)


# --- Adaptadores externos ---
def get_llm_provider() -> LlmProvider:
    """Selecciona el proveedor LLM OpenAI-compatible según configuración.

    Prioriza Groq si hay GROQ_API_KEY; si no, MiniMax; si no hay ninguna key
    (o COPILOT_LLM_PROVIDER=stub), usa el proveedor de prueba sin costo.
    """
    provider = (settings.COPILOT_LLM_PROVIDER or "").lower()
    if provider == "stub":
        return StubLlmProvider(model=settings.MINIMAX_MODEL)

    if settings.GROQ_API_KEY:
        return MiniMaxLlmProvider(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            base_url=settings.GROQ_BASE_URL,
            max_tokens=settings.COPILOT_MAX_TOKENS,
            timeout=settings.COPILOT_TIMEOUT_SECONDS,
            provider_name="groq",
        )

    if settings.MINIMAX_API_KEY:
        return MiniMaxLlmProvider(
            api_key=settings.MINIMAX_API_KEY,
            model=settings.MINIMAX_MODEL,
            base_url=settings.MINIMAX_BASE_URL,
            max_tokens=settings.COPILOT_MAX_TOKENS,
            timeout=settings.COPILOT_TIMEOUT_SECONDS,
            provider_name="minimax",
        )

    logger.warning("Sin API key de LLM configurada; se usa el proveedor LLM de prueba")
    return StubLlmProvider(model=settings.MINIMAX_MODEL)


def get_notification_channel() -> NotificationChannel:
    return TelegramChannel(
        bot_token=settings.TELEGRAM_BOT_TOKEN,
        timeout=settings.COPILOT_TIMEOUT_SECONDS,
    )


# --- Use cases ---
def get_generate_report_use_case(
    product_repository: ProductRepository = Depends(get_copilot_product_repository),
    alert_repository: StockAlertRepository = Depends(get_copilot_alert_repository),
    movement_repository: ProductMovementRepository = Depends(get_copilot_movement_repository),
) -> GenerateReportUseCase:
    return GenerateReportUseCase(
        product_repository=product_repository,
        alert_repository=alert_repository,
        movement_repository=movement_repository,
        public_base_url=settings.PUBLIC_BASE_URL,
    )


def get_send_chat_message_use_case(
    copilot_repository: CopilotRepository = Depends(get_copilot_repository),
    alert_repository: StockAlertRepository = Depends(get_copilot_alert_repository),
    product_repository: ProductRepository = Depends(get_copilot_product_repository),
    replenishment_repository: ReplenishmentRepository = Depends(get_replenishment_repository),
    llm_provider: LlmProvider = Depends(get_llm_provider),
    report_use_case: GenerateReportUseCase = Depends(get_generate_report_use_case),
) -> SendChatMessageUseCase:
    return SendChatMessageUseCase(
        copilot_repository,
        alert_repository,
        product_repository,
        replenishment_repository,
        llm_provider,
        report_use_case=report_use_case,
    )


def get_notify_stock_alert_use_case(
    copilot_repository: CopilotRepository = Depends(get_copilot_repository),
    telegram_repository: TelegramRepository = Depends(get_telegram_repository),
    channel: NotificationChannel = Depends(get_notification_channel),
) -> NotifyStockAlertUseCase:
    return NotifyStockAlertUseCase(copilot_repository, telegram_repository, channel)


def get_process_telegram_update_use_case(
    telegram_repository: TelegramRepository = Depends(get_telegram_repository),
    copilot_repository: CopilotRepository = Depends(get_copilot_repository),
    chat_use_case: SendChatMessageUseCase = Depends(get_send_chat_message_use_case),
    channel: NotificationChannel = Depends(get_notification_channel),
) -> ProcessTelegramUpdateUseCase:
    return ProcessTelegramUpdateUseCase(
        telegram_repository, copilot_repository, chat_use_case, channel
    )


def get_create_link_code_use_case(
    telegram_repository: TelegramRepository = Depends(get_telegram_repository),
) -> CreateLinkCodeUseCase:
    return CreateLinkCodeUseCase(telegram_repository, bot_link=resolve_bot_link())


def get_get_link_status_use_case(
    telegram_repository: TelegramRepository = Depends(get_telegram_repository),
) -> GetLinkStatusUseCase:
    return GetLinkStatusUseCase(telegram_repository)


def get_unlink_telegram_use_case(
    telegram_repository: TelegramRepository = Depends(get_telegram_repository),
) -> UnlinkTelegramUseCase:
    return UnlinkTelegramUseCase(telegram_repository)


def get_open_conversation_use_case(
    copilot_repository: CopilotRepository = Depends(get_copilot_repository),
) -> OpenConversationUseCase:
    return OpenConversationUseCase(copilot_repository)


def get_get_conversations_use_case(
    copilot_repository: CopilotRepository = Depends(get_copilot_repository),
) -> GetConversationsUseCase:
    return GetConversationsUseCase(copilot_repository)


def get_get_conversation_messages_use_case(
    copilot_repository: CopilotRepository = Depends(get_copilot_repository),
) -> GetConversationMessagesUseCase:
    return GetConversationMessagesUseCase(copilot_repository)


def get_create_replenishment_draft_use_case(
    replenishment_repository: ReplenishmentRepository = Depends(get_replenishment_repository),
) -> CreateReplenishmentDraftUseCase:
    return CreateReplenishmentDraftUseCase(replenishment_repository)


def get_get_replenishment_drafts_use_case(
    replenishment_repository: ReplenishmentRepository = Depends(get_replenishment_repository),
) -> GetReplenishmentDraftsUseCase:
    return GetReplenishmentDraftsUseCase(replenishment_repository)


def get_update_replenishment_draft_use_case(
    replenishment_repository: ReplenishmentRepository = Depends(get_replenishment_repository),
) -> UpdateReplenishmentDraftUseCase:
    return UpdateReplenishmentDraftUseCase(replenishment_repository)
