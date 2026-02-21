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


settings = Settings()