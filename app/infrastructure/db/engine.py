from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.settings import settings

engine: Engine = create_engine(
    settings.DB_URL,
    pool_pre_ping=True,
)
