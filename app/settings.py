from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    STAGE: str = Field(..., env="STAGE")
    DB_URL : str = Field(..., env="DB_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()