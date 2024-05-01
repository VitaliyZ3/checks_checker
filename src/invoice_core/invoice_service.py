from typing import List
from src.auth_core.schemas import CurrentUserInfo
from src.invoice_core.schemas import (
    Page,
    InvoiceModelCreateSchema,
    InvoiceModelSchema
)
from datetime import datetime
from fastapi import HTTPException
from src.invoice_core.invoice_database import InvoiceDatabase


def create_invoice(user_info: CurrentUserInfo, invoice_model: InvoiceModelCreateSchema) -> InvoiceModelSchema:

    total = sum([product.price * product.quantity for product in invoice_model.products])

    if total > invoice_model.payment.amount:
        raise HTTPException(status_code=400, detail="Payment funds are not enough to proceed the operation")

    if invoice_model.payment.type == "cash":
        rest = invoice_model.payment.amount - total
    elif invoice_model.payment.type == "cashless":
        rest = 0

    for product in invoice_model.products:
        product.total = product.price * product.quantity

    invoice = InvoiceModelSchema(
        products=invoice_model.products,
        payment=invoice_model.payment,
        total=total,
        rest=rest,
        created_at=datetime.now()
    )
    db_client = InvoiceDatabase()
    invoice_db = db_client.save_invoice_to_db(invoice)

    return InvoiceModelSchema.model_validate(invoice_db, from_attributes=True)


def get_invoices(user_info: CurrentUserInfo, page: Page) -> List[InvoiceModelSchema]:
    db_client = InvoiceDatabase()
    invoices = db_client.get_invoices_from_db(page)

    invoice_models = [InvoiceModelSchema.model_validate(invoice, from_attributes=True) for invoice in invoices]

    return invoice_models
