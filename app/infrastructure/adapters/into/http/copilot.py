"""
HTTP endpoints del Copiloto IA (chat interno + integración Telegram)
"""
import logging
from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from app.settings import settings
from app.core.middleware.auth_middleware import get_current_user
from app.application.dto.copilot_dto import (
    ChatMessageRequest,
    OpenConversationRequest,
    CopilotMessageResponse,
    CopilotConversationResponse,
    CopilotReplyResponse,
    ReplenishmentDraftCreateRequest,
    ReplenishmentDraftUpdateRequest,
    ReplenishmentDraftResponse,
    LinkStartResponse,
    LinkStatusResponse,
)
from app.application.use_cases.copilot_case import (
    SendChatMessageUseCase,
    ProcessTelegramUpdateUseCase,
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
from app.infrastructure.config.copilot_dependencies import (
    get_send_chat_message_use_case,
    get_process_telegram_update_use_case,
    get_create_link_code_use_case,
    get_get_link_status_use_case,
    get_unlink_telegram_use_case,
    get_open_conversation_use_case,
    get_get_conversations_use_case,
    get_get_conversation_messages_use_case,
    get_create_replenishment_draft_use_case,
    get_get_replenishment_drafts_use_case,
    get_update_replenishment_draft_use_case,
    resolve_bot_link,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/copilot", tags=["copilot"])


def _company_and_user(payload: Dict) -> (str, str):
    company_id = payload.get("company_id")
    user_id = payload.get("sub")
    if not company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no está asociado a una empresa",
        )
    return str(company_id), str(user_id)


# --- Conversaciones (chat interno) ---
@router.get("/conversations", response_model=List[CopilotConversationResponse])
def list_conversations(
    payload: Dict = Depends(get_current_user),
    use_case: GetConversationsUseCase = Depends(get_get_conversations_use_case),
):
    """Lista las conversaciones del copiloto de la empresa del usuario."""
    company_id, _ = _company_and_user(payload)
    return [CopilotConversationResponse.model_validate(c) for c in use_case.execute(company_id)]


@router.post("/conversations", response_model=CopilotConversationResponse, status_code=status.HTTP_201_CREATED)
def open_conversation(
    body: OpenConversationRequest,
    payload: Dict = Depends(get_current_user),
    use_case: OpenConversationUseCase = Depends(get_open_conversation_use_case),
):
    """Abre una conversación nueva (opcionalmente vinculada a una alerta)."""
    company_id, user_id = _company_and_user(payload)
    conversation = use_case.execute(
        company_id=company_id,
        user_id=user_id,
        alerta_id=body.alerta_id,
        codigo_producto=body.codigo_producto,
        titulo=body.titulo,
    )
    return CopilotConversationResponse.model_validate(conversation)


@router.get("/conversations/{id_conversation}/messages", response_model=List[CopilotMessageResponse])
def get_conversation_messages(
    id_conversation: UUID,
    payload: Dict = Depends(get_current_user),
    use_case: GetConversationMessagesUseCase = Depends(get_get_conversation_messages_use_case),
):
    """Lista los mensajes de una conversación."""
    company_id, _ = _company_and_user(payload)
    try:
        messages = use_case.execute(id_conversation, company_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return [CopilotMessageResponse.model_validate(m) for m in messages]


@router.post("/conversations/{id_conversation}/messages", response_model=CopilotReplyResponse)
def send_message(
    id_conversation: UUID,
    body: ChatMessageRequest,
    payload: Dict = Depends(get_current_user),
    use_case: SendChatMessageUseCase = Depends(get_send_chat_message_use_case),
):
    """Envía un mensaje al copiloto dentro de una conversación existente."""
    company_id, user_id = _company_and_user(payload)
    try:
        result = use_case.execute(
            company_id=company_id,
            user_id=user_id,
            message=body.contenido,
            conversation_id=id_conversation,
            alerta_id=body.alerta_id,
            codigo_producto=body.codigo_producto,
            canal="web",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return _reply_response(result)


@router.post("/chat", response_model=CopilotReplyResponse)
def chat(
    body: ChatMessageRequest,
    payload: Dict = Depends(get_current_user),
    use_case: SendChatMessageUseCase = Depends(get_send_chat_message_use_case),
):
    """Envía un mensaje al copiloto, creando la conversación si no se indica una."""
    company_id, user_id = _company_and_user(payload)
    try:
        result = use_case.execute(
            company_id=company_id,
            user_id=user_id,
            message=body.contenido,
            conversation_id=body.conversation_id,
            alerta_id=body.alerta_id,
            codigo_producto=body.codigo_producto,
            canal="web",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return _reply_response(result)


# --- Vinculación Telegram ---
@router.get("/telegram/link", response_model=LinkStatusResponse)
def telegram_link_status(
    payload: Dict = Depends(get_current_user),
    use_case: GetLinkStatusUseCase = Depends(get_get_link_status_use_case),
):
    """Consulta si el usuario tiene Telegram vinculado."""
    _, user_id = _company_and_user(payload)
    account = use_case.execute(user_id)
    if account is None:
        return LinkStatusResponse(linked=False)
    return LinkStatusResponse(
        linked=True,
        chat_id=account.chat_id,
        telegram_username=account.telegram_username,
    )


@router.post("/telegram/link", response_model=LinkStartResponse)
def telegram_link_start(
    payload: Dict = Depends(get_current_user),
    use_case: CreateLinkCodeUseCase = Depends(get_create_link_code_use_case),
):
    """Genera un código para vincular Telegram con el usuario."""
    company_id, user_id = _company_and_user(payload)
    link_code = use_case.execute(user_id=user_id, company_id=company_id)
    bot_link = resolve_bot_link()
    instructions = (
        "Abre el bot en Telegram y envía: /start " + link_code.code
        if bot_link
        else "Envía al bot de Telegram: /start " + link_code.code
    )
    return LinkStartResponse(
        code=link_code.code,
        expires_at=link_code.expires_at,
        bot_link=bot_link,
        instructions=instructions,
    )


@router.delete("/telegram/link", status_code=status.HTTP_204_NO_CONTENT)
def telegram_unlink(
    payload: Dict = Depends(get_current_user),
    use_case: UnlinkTelegramUseCase = Depends(get_unlink_telegram_use_case),
):
    """Desvincula la cuenta de Telegram del usuario."""
    _, user_id = _company_and_user(payload)
    use_case.execute(user_id)


# --- Webhook Telegram (público, autenticado por secret token) ---
@router.post("/telegram/webhook")
def telegram_webhook(
    update: dict,
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default=""),
    use_case: ProcessTelegramUpdateUseCase = Depends(get_process_telegram_update_use_case),
):
    """Recibe las actualizaciones del bot de Telegram."""
    expected = settings.TELEGRAM_WEBHOOK_SECRET
    if expected and x_telegram_bot_api_secret_token != expected:
        logger.warning("Webhook de Telegram con secret token inválido")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        return use_case.execute(update)
    except Exception as exc:  # noqa: BLE001 - el webhook nunca debe devolver 500 a Telegram
        logger.error(f"Error procesando update de Telegram: {exc}")
        return {"ok": True, "error": "processed_with_error"}


# --- Borradores de reabastecimiento ---
@router.get("/replenishment-drafts", response_model=List[ReplenishmentDraftResponse])
def list_replenishment_drafts(
    payload: Dict = Depends(get_current_user),
    use_case: GetReplenishmentDraftsUseCase = Depends(get_get_replenishment_drafts_use_case),
):
    """Lista los borradores de reabastecimiento de la empresa."""
    company_id, _ = _company_and_user(payload)
    return [ReplenishmentDraftResponse.model_validate(d) for d in use_case.execute(company_id)]


@router.post(
    "/replenishment-drafts",
    response_model=ReplenishmentDraftResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_replenishment_draft(
    body: ReplenishmentDraftCreateRequest,
    payload: Dict = Depends(get_current_user),
    use_case: CreateReplenishmentDraftUseCase = Depends(get_create_replenishment_draft_use_case),
):
    """Crea un borrador de reabastecimiento (pendiente de revisión)."""
    company_id, user_id = _company_and_user(payload)
    draft = use_case.execute(
        company_id=company_id,
        user_id=user_id,
        codigo_producto=body.codigo_producto,
        alerta_id=body.alerta_id,
        id_conversation=body.conversation_id,
        cantidad_sugerida=body.cantidad_sugerida,
        unidad_medida=body.unidad_medida,
        proveedor_sugerido=body.proveedor_sugerido,
        notas=body.notas,
    )
    return ReplenishmentDraftResponse.model_validate(draft)


@router.patch("/replenishment-drafts/{id_borrador}", response_model=ReplenishmentDraftResponse)
def update_replenishment_draft(
    id_borrador: int,
    body: ReplenishmentDraftUpdateRequest,
    payload: Dict = Depends(get_current_user),
    use_case: UpdateReplenishmentDraftUseCase = Depends(get_update_replenishment_draft_use_case),
):
    """Actualiza un borrador de reabastecimiento durante su revisión."""
    company_id, _ = _company_and_user(payload)
    try:
        draft = use_case.execute(id_borrador, company_id, body.model_dump(exclude_none=True))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return ReplenishmentDraftResponse.model_validate(draft)


def _reply_response(result) -> CopilotReplyResponse:
    draft_response = None
    if result.replenishment_draft is not None:
        draft_response = ReplenishmentDraftResponse.model_validate(result.replenishment_draft)
    return CopilotReplyResponse(
        reply=result.reply,
        provider=result.provider,
        model=result.model,
        conversation_id=result.conversation_id,
        replenishment_draft=draft_response,
    )
