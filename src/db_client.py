from sqlalchemy import URL, create_engine, Engine
from src.config import settings
import functools


class DatabaseClient:
    _engine: Engine

    def __init__(self, url, echo: bool = False) -> None:
        self.engine = create_engine(
            url=url,
            echo=echo
        )


url_object = URL.create(
    "postgresql+pg8000",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    database=settings.postgres_database,
)


@functools.cache
def _get_DB_Client() -> DatabaseClient:
    DBClient = DatabaseClient(
        url=url_object,
        echo=True
    )
    return DBClient
