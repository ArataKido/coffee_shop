from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import PostgresConfig

def new_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    database_uri = f"postgresql+psycopg://{psql_config.user}:{psql_config.password}@{psql_config.host}:{psql_config.port}/{psql_config.database}"

    engine = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)

def get_db():
    pass

# sync_db_url = f"postgresql+psycopg://{psql_config.login}:{psql_config.password}@{psql_config.host}:{psql_config.port}/{psql_config.database}"

# Синхронный генератор сессий для Celery
# sync_db_url = PostgresConfig.database_url.replace("+asyncpg", "")

def new_sync_session_maker(psql_config: PostgresConfig) -> sessionmaker[Session]:
    database_uri = f"postgresql+psycopg://{psql_config.user}:{psql_config.password}@{psql_config.host}:{psql_config.port}/{psql_config.database}"

    engine = create_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return sessionmaker(engine, class_=Session, autoflush=False, expire_on_commit=False)


# Синхронное соединение с базой данных для Celery
# Получаем URL без asyncpg префикса
# sync_engine = create_engine(
#     sync_db_url,
#     echo=False,  # Set to False in production
#     future=True,
# )


# # Создаем фабрику синхронных сессий для Celery
# SyncSessionLocal = sessionmaker(
#     sync_engine,
#     expire_on_commit=False,
# )
def get_db_sync():
    session = new_sync_session_maker()
    try:
        yield session
    finally:
        session.close()
