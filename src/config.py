from pydantic_settings import BaseSettings

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 0


class ConfigSettings(BaseSettings):
    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_database: str


settings = ConfigSettings()
