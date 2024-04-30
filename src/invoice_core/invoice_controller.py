from fastapi import APIRouter, Request, Query, Depends
from src.invoice_core import invoice_service
from typing import Optional, List
from src.config import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE
)
from src.enums import (
    InvoiceOrderingFields,
    SortOrder
)
from src.invoice_core.schemas import (
    Page,
    InvoiceModelSchema,
    InvoiceModelCreateSchema
)
from src.auth import get_current_user_into
from src.auth_core.schemas import CurrentUserInfo

router = APIRouter()


@router.post(
    "",
    response_model=InvoiceModelSchema
)
def create_invoice(
    invoice_defition: InvoiceModelCreateSchema,
    user_info: CurrentUserInfo = Depends(get_current_user_into)
) -> InvoiceModelSchema:
    return invoice_service.create_check(
        user_info=user_info,
        invoice_defition=invoice_defition
    )


@router.get(
    "",
    response_model=List[InvoiceModelSchema]
)
def get_invoices_data(
    user_info: CurrentUserInfo = Depends(get_current_user_into),
    page_size: Optional[int] = Query(DEFAULT_PAGE_SIZE, description="Page Size"),
    page_num: Optional[int] = Query(DEFAULT_PAGE_NUMBER, description="Page number", ge=0),
    order_by: Optional[InvoiceOrderingFields] = Query(InvoiceOrderingFields.date, description="Page ordering field"),
    order_mode: Optional[SortOrder] = Query(SortOrder.asc, description="Page sort order")
):
    invoices, total_count = invoice_service.get_checks_data(
        user_info=user_info,
        page=Page(page_size=page_size, page_num=page_num, order_by=order_by, sort_order=order_mode)
    )
    return list(InvoiceModelSchema)
