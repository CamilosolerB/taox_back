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