from sqlalchemy import URL, create_engine, Engine
from src.config import settings
import functools
from sqlalchemy.orm import Session


class DatabaseClient:
    _engine: Engine

    def __init__(self, url, echo: bool = False) -> None:
        self._engine = create_engine(
            url=url,
            echo=echo,
            pool_size=10
        )


@functools.cache
def _get_DB_Client() -> DatabaseClient:
    url_object = URL.create(
        "postgresql+pg8000",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_database,
    )
    DBClient = DatabaseClient(
        url=url_object,
        echo=False
    )
    return DBClient


@functools.cache
def _get_db_session() -> Session:
    db_client = _get_DB_Client()
    session = Session(
        db_client._engine,
        expire_on_commit=True,
        autoflush=False
    )
    return session
