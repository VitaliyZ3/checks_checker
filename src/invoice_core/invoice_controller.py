from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from typing import List
from src.invoice_core.schemas import (
    Page,
    InvoiceModelSchema,
    InvoiceModelCreateSchema
)
from src.invoice_core import invoice_service
from src.auth_core.auth.base_config import current_user
import time

router = APIRouter()


@router.post("", response_model=InvoiceModelSchema)
def create_invoice(
    invoice_defition: InvoiceModelCreateSchema,
    # user_info=Depends(current_user)
) -> InvoiceModelSchema:
    return invoice_service.create_invoice(
        # user_model=user_info,
        invoice_model=invoice_defition
    )


@router.get("", response_model=List[InvoiceModelSchema])
def get_invoices(
    filters: Page = Depends(),
    # user_info=Depends(current_user)
) -> List[InvoiceModelSchema]:
    invoices = invoice_service.get_invoices(
        # user_model=user_info,
        page=filters
    )
    return invoices


@router.get(
    "/invoice-file/{invoice_id}",
)
def get_invoice_text(invoice_id: int) -> FileResponse:
    invoice_file_path = invoice_service.get_invoice_print_file(invoice_id)
    return FileResponse(invoice_file_path, media_type="text/plain", filename="invoice.txt")


@router.get("/health")
def health() -> int:
    time.sleep(2)
    return 200