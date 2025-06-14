from dishka import AsyncContainer, make_async_container

from app.config import Config
from app.dependencies.providers import (
    conn_provider, repo_provider, service_provider
)


config = Config()
def create_container() -> AsyncContainer:
    container = make_async_container(
    conn_provider.ConnectionProvider(),
    repo_provider.RepoProvider(),
    service_provider.ServiceProvider(),
    context={Config: config}
    )

    return container

