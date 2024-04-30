from sqlalchemy import URL, create_engine, Engine
from src.config import settings


class DatabaseHelper:
    engine: Engine

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


db_helper = DatabaseHelper(
    url=url_object,
    echo=True
)