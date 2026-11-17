"""
Tests del Copiloto IA: vinculación, separación multi-empresa, errores del LLM,
deduplicación de updates de Telegram y tolerancia a fallos del canal.

Usan dobles de prueba (fakes) en memoria para no depender de base de datos.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

import pytest

from app.domain.entities.copilot_models import (
    CopilotConversation,
    CopilotMessage,
    LlmResult,
    ReplenishmentDraft,
    TelegramAccount,
    TelegramLinkCode,
)
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.entities.product_model import Product
from app.domain.exceptions.copilot_exceptions import LlmProviderError
from app.application.use_cases.copilot_case import (
    SendChatMessageUseCase,
    GenerateReportUseCase,
    ProcessTelegramUpdateUseCase,
    NotifyStockAlertUseCase,
    CreateLinkCodeUseCase,
    GetLinkStatusUseCase,
    UnlinkTelegramUseCase,
)


# --------------------------------------------------------------------------- #
# Fakes
# --------------------------------------------------------------------------- #
class FakeCopilotRepository:
    def __init__(self):
        self.conversations: Dict[UUID, CopilotConversation] = {}
        self.messages: Dict[UUID, List[CopilotMessage]] = {}

    def create_conversation(self, conversation: CopilotConversation) -> CopilotConversation:
        conversation.id_conversation = conversation.id_conversation or uuid.uuid4()
        conversation.created_at = conversation.created_at or datetime.utcnow()
        conversation.updated_at = conversation.updated_at or datetime.utcnow()
        self.conversations[conversation.id_conversation] = conversation
        self.messages[conversation.id_conversation] = []
        return conversation

    def get_conversation(self, id_conversation: UUID, company_id: Optional[str] = None):
        conv = self.conversations.get(id_conversation)
        if conv is None:
            return None
        if company_id is not None and str(conv.id_empresa) != str(company_id):
            return None
        return conv

    def get_conversations_by_company(self, company_id: str):
        return [c for c in self.conversations.values() if str(c.id_empresa) == str(company_id)]

    def get_latest_conversation_by_channel(self, canal: str, canal_chat_id: str):
        matches = [
            c
            for c in self.conversations.values()
            if c.canal == canal and str(c.canal_chat_id) == str(canal_chat_id)
        ]
        return matches[-1] if matches else None

    def update_conversation(self, id_conversation: UUID, data: dict):
        conv = self.conversations.get(id_conversation)
        if conv is None:
            return None
        for key, value in data.items():
            setattr(conv, key, value)
        return conv

    def add_message(self, message: CopilotMessage) -> CopilotMessage:
        message.id_mensaje = len(self.messages.setdefault(message.id_conversation, [])) + 1
        message.created_at = message.created_at or datetime.utcnow()
        self.messages[message.id_conversation].append(message)
        return message

    def get_messages(self, id_conversation: UUID, company_id: Optional[str] = None):
        if company_id is not None and self.get_conversation(id_conversation, company_id) is None:
            return []
        return list(self.messages.get(id_conversation, []))

    def get_recent_messages(self, id_conversation: UUID, limit: int = 20):
        return list(self.messages.get(id_conversation, []))[-limit:]


class FakeTelegramRepository:
    def __init__(self):
        self.link_codes: Dict[str, TelegramLinkCode] = {}
        self.accounts_by_user: Dict[str, TelegramAccount] = {}
        self.processed_updates = set()

    def create_link_code(self, link_code: TelegramLinkCode) -> TelegramLinkCode:
        link_code.created_at = datetime.utcnow()
        self.link_codes[link_code.code] = link_code
        return link_code

    def get_link_code(self, code: str):
        return self.link_codes.get(code)

    def mark_link_code_used(self, code: str):
        if code in self.link_codes:
            self.link_codes[code].used_at = datetime.utcnow()

    def upsert_account(self, account: TelegramAccount) -> TelegramAccount:
        self.accounts_by_user[str(account.user_id)] = account
        return account

    def get_account_by_user(self, user_id: UUID):
        return self.accounts_by_user.get(str(user_id))

    def get_account_by_chat(self, chat_id: int):
        for acc in self.accounts_by_user.values():
            if acc.chat_id == chat_id:
                return acc
        return None

    def get_accounts_by_company(self, company_id: str):
        return [a for a in self.accounts_by_user.values() if str(a.id_empresa) == str(company_id)]

    def delete_account_by_user(self, user_id: UUID) -> bool:
        return self.accounts_by_user.pop(str(user_id), None) is not None

    def register_update(self, update_id: int) -> bool:
        if update_id in self.processed_updates:
            return False
        self.processed_updates.add(update_id)
        return True


class FakeReplenishmentRepository:
    def __init__(self):
        self.drafts: List[ReplenishmentDraft] = []

    def create_draft(self, draft: ReplenishmentDraft) -> ReplenishmentDraft:
        draft.id_borrador = len(self.drafts) + 1
        draft.created_at = datetime.utcnow()
        draft.updated_at = datetime.utcnow()
        self.drafts.append(draft)
        return draft

    def get_drafts_by_company(self, company_id: str):
        return [d for d in self.drafts if str(d.id_empresa) == str(company_id)]

    def get_draft_by_id(self, id_borrador: int, company_id: str):
        for d in self.drafts:
            if d.id_borrador == id_borrador and str(d.id_empresa) == str(company_id):
                return d
        return None

    def update_draft(self, id_borrador: int, company_id: str, data: dict):
        d = self.get_draft_by_id(id_borrador, company_id)
        if d is None:
            return None
        for key, value in data.items():
            setattr(d, key, value)
        return d


class FakeAlertRepository:
    def __init__(self, alerts: Optional[List[StockAlert]] = None):
        self.alerts = alerts or []

    def get_active_alerts(self, company_id: str):
        return [a for a in self.alerts if str(a.id_empresa) == str(company_id)]


class FakeProductRepository:
    def __init__(self, products: Optional[List[Product]] = None):
        self.products = products or []

    def get_product_by_id(self, id_product: str):
        for p in self.products:
            if p.id_product == id_product:
                return p
        return None

    def get_products_by_company_id(self, company_id: str):
        return [p for p in self.products if str(p.company_id) == str(company_id)]


class FakeMovementRepository:
    def __init__(self, movements: Optional[list] = None):
        self.movements = movements or []

    def get_all_movements(self, company_id: str):
        return list(self.movements)


class FakeLlmProvider:
    def __init__(self, content: str = "respuesta del copiloto", raise_error: bool = False):
        self.content = content
        self.raise_error = raise_error
        self.calls = 0

    @property
    def name(self):
        return "fake"

    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> LlmResult:
        self.calls += 1
        if self.raise_error:
            raise LlmProviderError("fallo simulado")
        return LlmResult(content=self.content, provider="fake", model="fake-model")


class FakeChannel:
    def __init__(self, enabled: bool = True, deliver: bool = True):
        self.enabled = enabled
        self.deliver = deliver
        self.sent: List[tuple] = []

    @property
    def channel_name(self):
        return "telegram"

    @property
    def is_enabled(self):
        return self.enabled

    def send_message(self, chat_id: str, text: str) -> bool:
        self.sent.append((str(chat_id), text))
        return self.deliver


def make_chat_use_case(llm=None, alerts=None, replenishment=None, report_use_case=None):
    return SendChatMessageUseCase(
        copilot_repository=FakeCopilotRepository(),
        alert_repository=FakeAlertRepository(alerts),
        product_repository=FakeProductRepository(),
        replenishment_repository=replenishment or FakeReplenishmentRepository(),
        llm_provider=llm or FakeLlmProvider(),
        report_use_case=report_use_case,
    )


COMPANY_A = str(uuid.uuid4())
COMPANY_B = str(uuid.uuid4())
USER_A = str(uuid.uuid4())


# --------------------------------------------------------------------------- #
# Chat
# --------------------------------------------------------------------------- #
def test_chat_creates_conversation_and_persists_messages():
    llm = FakeLlmProvider(content="Hola, aquí tienes el estado del stock.")
    use_case = make_chat_use_case(llm=llm)

    result = use_case.execute(company_id=COMPANY_A, user_id=USER_A, message="¿Cómo va el stock?")

    assert result.reply == "Hola, aquí tienes el estado del stock."
    assert result.conversation_id is not None
    assert llm.calls == 1

    stored = use_case.copilot_repository.get_messages(result.conversation_id)
    assert [m.rol for m in stored] == ["user", "assistant"]
    assert stored[0].contenido == "¿Cómo va el stock?"


def test_chat_llm_error_returns_friendly_message():
    llm = FakeLlmProvider(raise_error=True)
    use_case = make_chat_use_case(llm=llm)

    result = use_case.execute(company_id=COMPANY_A, user_id=USER_A, message="hola")

    assert "No pude contactar" in result.reply
    assert result.provider == "error"
    # el mensaje del usuario igualmente se persiste
    stored = use_case.copilot_repository.get_messages(result.conversation_id)
    assert stored[0].rol == "user"


def test_chat_parses_replenishment_action_and_creates_draft():
    action = (
        "Recomiendo reponer 50 unidades.\n"
        '```json\n{"action": "replenishment_draft", "codigo_producto": "CHEM001", '
        '"cantidad_sugerida": 50, "unidad_medida": "kg", "proveedor_sugerido": "ACME", '
        '"notas": "stock critico"}\n```'
    )
    replenishment = FakeReplenishmentRepository()
    use_case = make_chat_use_case(llm=FakeLlmProvider(content=action), replenishment=replenishment)

    result = use_case.execute(
        company_id=COMPANY_A, user_id=USER_A, message="prepara la reposición", codigo_producto="CHEM001"
    )

    assert result.replenishment_draft is not None
    assert result.replenishment_draft.codigo_producto == "CHEM001"
    assert result.replenishment_draft.cantidad_sugerida == 50
    assert len(replenishment.drafts) == 1
    # el bloque JSON no debe quedar en el texto visible
    assert "```json" not in result.reply


def test_chat_rejects_conversation_from_other_company():
    use_case = make_chat_use_case()
    conv = use_case.copilot_repository.create_conversation(
        CopilotConversation(id_empresa=COMPANY_B, canal="web")
    )

    with pytest.raises(ValueError):
        use_case.execute(
            company_id=COMPANY_A,
            user_id=USER_A,
            message="hola",
            conversation_id=conv.id_conversation,
        )


# --------------------------------------------------------------------------- #
# Telegram: vinculación
# --------------------------------------------------------------------------- #
def _build_telegram_stack(channel=None, llm=None):
    telegram_repo = FakeTelegramRepository()
    copilot_repo = FakeCopilotRepository()
    chat_use_case = SendChatMessageUseCase(
        copilot_repository=copilot_repo,
        alert_repository=FakeAlertRepository(),
        product_repository=FakeProductRepository(),
        replenishment_repository=FakeReplenishmentRepository(),
        llm_provider=llm or FakeLlmProvider(content="respuesta telegram"),
    )
    channel = channel or FakeChannel()
    process = ProcessTelegramUpdateUseCase(
        telegram_repository=telegram_repo,
        copilot_repository=copilot_repo,
        chat_use_case=chat_use_case,
        channel=channel,
    )
    return telegram_repo, copilot_repo, channel, process


def test_telegram_link_flow_and_message_reply():
    telegram_repo, _, channel, process = _build_telegram_stack()
    create_code = CreateLinkCodeUseCase(telegram_repo, bot_link="https://t.me/testbot")

    link_code = create_code.execute(user_id=USER_A, company_id=COMPANY_A)

    # /start con código vincula la cuenta
    process.execute(
        {
            "update_id": 1,
            "message": {
                "chat": {"id": 555},
                "from": {"username": "admin"},
                "text": f"/start {link_code.code}",
            },
        }
    )
    account = telegram_repo.get_account_by_chat(555)
    assert account is not None
    assert str(account.id_empresa) == COMPANY_A

    # mensaje normal -> se enruta al chat y responde por el canal
    process.execute(
        {"update_id": 2, "message": {"chat": {"id": 555}, "from": {"username": "admin"}, "text": "¿qué alertas hay?"}}
    )
    assert any("respuesta telegram" in text for _, text in channel.sent)


def test_telegram_invalid_link_code_does_not_link():
    telegram_repo, _, channel, process = _build_telegram_stack()

    process.execute(
        {"update_id": 10, "message": {"chat": {"id": 777}, "text": "/start NOEXISTE"}}
    )

    assert telegram_repo.get_account_by_chat(777) is None
    assert any("no es válido" in text for _, text in channel.sent)


def test_telegram_unlinked_message_prompts_link():
    _, _, channel, process = _build_telegram_stack()

    process.execute({"update_id": 20, "message": {"chat": {"id": 888}, "text": "hola"}})

    assert any("no está vinculada" in text for _, text in channel.sent)


def test_telegram_link_status_and_unlink():
    telegram_repo = FakeTelegramRepository()
    create_code = CreateLinkCodeUseCase(telegram_repo)
    create_code.execute(user_id=USER_A, company_id=COMPANY_A)
    telegram_repo.upsert_account(
        TelegramAccount(user_id=USER_A, chat_id=999, id_empresa=COMPANY_A)
    )

    status = GetLinkStatusUseCase(telegram_repo).execute(USER_A)
    assert status is not None and status.chat_id == 999

    assert UnlinkTelegramUseCase(telegram_repo).execute(USER_A) is True
    assert GetLinkStatusUseCase(telegram_repo).execute(USER_A) is None


# --------------------------------------------------------------------------- #
# Telegram: idempotencia y fallos de canal
# --------------------------------------------------------------------------- #
def test_telegram_duplicate_update_is_ignored():
    telegram_repo, _, channel, process = _build_telegram_stack()
    update = {"update_id": 42, "message": {"chat": {"id": 111}, "text": "hola"}}

    first = process.execute(update)
    second = process.execute(update)

    assert first.get("duplicate") is None
    assert second.get("duplicate") is True
    # solo se respondió una vez (una por el prompt de no vinculado)
    assert len(channel.sent) == 1


def test_telegram_channel_failure_does_not_raise():
    failing_channel = FakeChannel(deliver=False)
    telegram_repo, _, _, process = _build_telegram_stack(channel=failing_channel)
    create_code = CreateLinkCodeUseCase(telegram_repo)
    code = create_code.execute(user_id=USER_A, company_id=COMPANY_A)

    # no debe lanzar aunque el canal falle al entregar
    result = process.execute(
        {"update_id": 100, "message": {"chat": {"id": 222}, "text": f"/start {code.code}"}}
    )
    assert result["ok"] is True
    assert telegram_repo.get_account_by_chat(222) is not None


# --------------------------------------------------------------------------- #
# Notificación de alertas
# --------------------------------------------------------------------------- #
def _make_alert(company_id=COMPANY_A):
    return StockAlert(
        id_alerta=7,
        codigo_producto="CHEM001",
        id_proceso=uuid.uuid4(),
        tipo_alerta="stock_critico",
        cantidad_actual=5,
        cantidad_referencia=10,
        id_empresa=company_id,
        estado="activa",
        descripcion="Stock crítico global",
    )


def test_notify_alert_sends_to_linked_company_accounts():
    telegram_repo = FakeTelegramRepository()
    copilot_repo = FakeCopilotRepository()
    channel = FakeChannel()
    telegram_repo.upsert_account(
        TelegramAccount(user_id=USER_A, chat_id=321, id_empresa=COMPANY_A)
    )
    use_case = NotifyStockAlertUseCase(copilot_repo, telegram_repo, channel)

    sent = use_case.execute(_make_alert())

    assert sent == 1
    assert len(channel.sent) == 1
    # se creó una conversación vinculada a la alerta
    convs = copilot_repo.get_conversations_by_company(COMPANY_A)
    assert len(convs) == 1
    assert convs[0].alerta_id == 7


def test_notify_alert_skips_other_companies():
    telegram_repo = FakeTelegramRepository()
    copilot_repo = FakeCopilotRepository()
    channel = FakeChannel()
    telegram_repo.upsert_account(
        TelegramAccount(user_id=USER_A, chat_id=321, id_empresa=COMPANY_B)
    )
    use_case = NotifyStockAlertUseCase(copilot_repo, telegram_repo, channel)

    sent = use_case.execute(_make_alert(company_id=COMPANY_A))

    assert sent == 0
    assert channel.sent == []


def test_notify_alert_disabled_channel_returns_zero():
    telegram_repo = FakeTelegramRepository()
    copilot_repo = FakeCopilotRepository()
    channel = FakeChannel(enabled=False)
    telegram_repo.upsert_account(
        TelegramAccount(user_id=USER_A, chat_id=321, id_empresa=COMPANY_A)
    )
    use_case = NotifyStockAlertUseCase(copilot_repo, telegram_repo, channel)

    assert use_case.execute(_make_alert()) == 0


# --------------------------------------------------------------------------- #
# Reportes
# --------------------------------------------------------------------------- #
def _make_report_use_case(tmp_path):
    use_case = GenerateReportUseCase(
        product_repository=FakeProductRepository(
            [
                Product(
                    id_product="A0001",
                    name="Cloro",
                    generic_name="Hipoclorito de sodio",
                    price=10,
                    unit_measure="kg",
                    unit_price=12,
                    min_unit_price=8,
                    lead_time_days=5,
                    restorage="manual",
                    limite_critico=10,
                    company_id=COMPANY_A,
                )
            ]
        ),
        alert_repository=FakeAlertRepository([_make_alert()]),
        movement_repository=FakeMovementRepository(),
    )
    use_case._reports_dir = lambda: str(tmp_path)
    return use_case


def test_generate_report_creates_excel_file(tmp_path):
    use_case = _make_report_use_case(tmp_path)

    result = use_case.execute(company_id=COMPANY_A, tipo="inventario", formato="excel")

    assert result["formato"] == "excel"
    assert result["rows"] == 1
    assert result["url"].startswith("/copilot/reports/")
    assert (tmp_path / result["filename"]).exists()


def test_report_download_returns_attachment(tmp_path, monkeypatch):
    from app.infrastructure.adapters.into.http import copilot

    filename = "inventario-1234abcd.pdf"
    (tmp_path / filename).write_bytes(b"pdf content")
    monkeypatch.setattr(copilot, "_reports_directory", lambda: tmp_path)

    response = copilot.download_report(filename)

    assert response.media_type == "application/pdf"
    assert response.headers["content-disposition"] == f'attachment; filename="{filename}"'
    assert response.headers["cache-control"] == "private, no-store"


def test_report_download_rejects_unsafe_filename():
    from fastapi import HTTPException
    from app.infrastructure.adapters.into.http import copilot

    with pytest.raises(HTTPException) as error:
        copilot.download_report("../../secrets.pdf")

    assert error.value.status_code == 404


def test_generate_report_rejects_unknown_type(tmp_path):
    use_case = _make_report_use_case(tmp_path)

    with pytest.raises(ValueError):
        use_case.execute(company_id=COMPANY_A, tipo="desconocido", formato="excel")


def test_chat_report_action_appends_download_link(tmp_path):
    action = (
        "Claro, aquí tienes el reporte solicitado.\n"
        '```json\n{"action": "report", "tipo": "alertas", "formato": "pdf", '
        '"titulo": "Alertas de stock"}\n```'
    )
    use_case = make_chat_use_case(
        llm=FakeLlmProvider(content=action),
        report_use_case=_make_report_use_case(tmp_path),
    )

    result = use_case.execute(
        company_id=COMPANY_A, user_id=USER_A, message="genera un reporte de alertas"
    )

    assert "```json" not in result.reply
    assert "Reporte listo" in result.reply
    assert "/copilot/reports/" in result.reply
