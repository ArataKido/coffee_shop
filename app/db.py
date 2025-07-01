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


def get_db_sync():
    session = new_sync_session_maker()
    try:
        yield session
    finally:
        session.close()
