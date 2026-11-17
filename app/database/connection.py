from sqlalchemy import create_engine

from app.core.config import settings

if not settings.DATABASE_URL:
    raise ValueError("Database configuration is missing from .env")

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)