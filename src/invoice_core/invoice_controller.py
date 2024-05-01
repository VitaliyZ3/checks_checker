from fastapi import APIRouter, Depends
from src.invoice_core import invoice_service
from typing import List
from src.invoice_core.schemas import (
    Page,
    InvoiceModelSchema,
    InvoiceModelCreateSchema
)
from src.auth import get_current_user_into
from src.auth_core.schemas import CurrentUserInfo


router = APIRouter()


@router.post("", response_model=InvoiceModelSchema)
def create_invoice(
    invoice_defition: InvoiceModelCreateSchema,
    user_info: CurrentUserInfo = Depends(get_current_user_into)
) -> InvoiceModelSchema:
    return invoice_service.create_invoice(
        user_info=user_info,
        invoice_model=invoice_defition
    )


@router.get("", response_model=List[InvoiceModelSchema])
def get_invoices(
    user_info: CurrentUserInfo = Depends(get_current_user_into),
    filters: Page = Depends()
) -> List[InvoiceModelSchema]:
    invoices = invoice_service.get_invoices(
        user_info=user_info,
        page=filters
    )
    return invoices
