from src.auth_core.schemas import CurrentUserInfo
from src.invoice_core.schemas import (
    Page,
    InvoiceModelSchema
)


def create_check(user_info: CurrentUserInfo, model: InvoiceModelSchema) -> None:
    return None


def get_checks_data(user_info: CurrentUserInfo, page: Page) -> None:
    return None