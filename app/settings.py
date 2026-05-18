from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    STAGE: str = Field(..., env="STAGE")
    DB_URL : str = Field(..., env="DB_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    ADMIN_ROLE_ID: str = Field(..., env="ADMIN_ROLE_ID")
    OBSERVER_ROLE_ID: str = Field(..., env="OBSERVER_ROLE_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

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