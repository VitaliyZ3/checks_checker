from pydantic_settings import BaseSettings

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 0
FILE_STORAGE_PATH = "/invoices"


class ConfigSettings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_database: str
    SECRET_AUTH: str


settings = ConfigSettings()
