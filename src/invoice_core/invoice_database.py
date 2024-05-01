from src.db_client import _get_DB_Client, DatabaseClient


class InvoiceDatabase:

    DB_Client: DatabaseClient

    def __init__(self):
        self.DB_Client = _get_DB_Client()