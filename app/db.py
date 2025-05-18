from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings  # Assuming you have a settings module for configuration

# Create an async engine with a connection pool
engine = create_async_engine(
    settings.database_url,
    echo=False,  # Set to False in production to disable SQL logging
    future=True,
)

# Create a session factory for async sessions
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Синхронное соединение с базой данных для Celery
# Получаем URL без asyncpg префикса
sync_db_url = settings.database_url.replace("+asyncpg", "")
sync_engine = create_engine(
    sync_db_url,
    echo=False,  # Set to False in production
    future=True,
)

# Создаем фабрику синхронных сессий для Celery
SyncSessionLocal = sessionmaker(
    sync_engine,
    expire_on_commit=False,
)


# Асинхронный генератор сессий для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Синхронный генератор сессий для Celery
def get_db_sync():
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()
