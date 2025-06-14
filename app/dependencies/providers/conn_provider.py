from dishka import from_context, provide, Provider, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import AsyncIterable

from app.config import Config
from app.db import new_session_maker

class ConnectionProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session
