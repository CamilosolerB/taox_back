from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    STAGE: str = Field(validation_alias=AliasChoices("STAGE", "stage"))
    DB_URL: str = Field(
        validation_alias=AliasChoices("DB_URL", "db_url", "DB_URL_RAILWAY", "db_url_railway")
    )
    JWT_SECRET_KEY: str = Field(
        validation_alias=AliasChoices("JWT_SECRET_KEY", "jwt_secret_key")
    )
    ADMIN_ROLE_ID: str = Field(
        validation_alias=AliasChoices("ADMIN_ROLE_ID", "admin_role_id")
    )
    OBSERVER_ROLE_ID: str = Field(
        validation_alias=AliasChoices("OBSERVER_ROLE_ID", "observer_role_id")
    )

    # --- Copiloto IA (MiniMax) ---
    MINIMAX_API_KEY: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MINIMAX_API_KEY", "minimax_api_key"),
    )
    MINIMAX_MODEL: str = Field(
        default="MiniMax-M3.1-Flash",
        validation_alias=AliasChoices("MINIMAX_MODEL", "minimax_model"),
    )
    MINIMAX_BASE_URL: str = Field(
        default="https://api.minimax.io/v1",
        validation_alias=AliasChoices("MINIMAX_BASE_URL", "minimax_base_url"),
    )

    # --- Copiloto IA (proveedor OpenAI-compatible alternativo: Groq) ---
    GROQ_API_KEY: str | None = Field(
        default=None,
        validation_alias=AliasChoices("GROQ_API_KEY", "groq_api_key"),
    )
    GROQ_MODEL: str = Field(
        default="openai/gpt-oss-120b",
        validation_alias=AliasChoices("GROQ_MODEL", "groq_model"),
    )
    GROQ_BASE_URL: str = Field(
        default="https://api.groq.com/openai/v1",
        validation_alias=AliasChoices("GROQ_BASE_URL", "groq_base_url"),
    )

    COPILOT_LLM_PROVIDER: str = Field(
        default="minimax",
        validation_alias=AliasChoices("COPILOT_LLM_PROVIDER", "copilot_llm_provider"),
    )
    COPILOT_MAX_TOKENS: int = Field(
        default=1024,
        validation_alias=AliasChoices("COPILOT_MAX_TOKENS", "copilot_max_tokens"),
    )
    COPILOT_TIMEOUT_SECONDS: int = Field(
        default=60,
        validation_alias=AliasChoices("COPILOT_TIMEOUT_SECONDS", "copilot_timeout_seconds"),
    )
    PUBLIC_BASE_URL: str | None = Field(
        default=None,
        validation_alias=AliasChoices("PUBLIC_BASE_URL", "public_base_url"),
    )

    # --- Canal Telegram ---
    TELEGRAM_BOT_TOKEN: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_BOT_TOKEN", "telegram_bot_token"),
    )
    TELEGRAM_BOT_USERNAME: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_BOT_USERNAME", "telegram_bot_username"),
    )
    TELEGRAM_BOT_LINK: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_BOT_LINK", "telegram_bot_link"),
    )
    TELEGRAM_WEBHOOK_SECRET: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_WEBHOOK_SECRET", "telegram_webhook_secret"),
    )

    def get_company_admin_role(self, company_id: str) -> str:
        """Generate company-specific admin role ID"""
        return f"company_admin_{company_id}"
    
    def is_global_admin(self, role_id: str) -> bool:
        """Check if role is global admin"""
        return role_id == self.ADMIN_ROLE_ID
    
    def is_company_admin(self, role_id: str, company_id: str) -> bool:
        """Check if role is company admin for specific company"""
        return role_id == self.get_company_admin_role(company_id)


settings = Settings()