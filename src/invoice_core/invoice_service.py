from typing import List
from src.invoice_core.schemas import (
    Page,
    InvoiceModelCreateSchema,
    InvoiceModelSchema
)
from datetime import datetime
from fastapi import HTTPException
from src.invoice_core.invoice_database import InvoiceDatabase
from src.auth_core.models import User


def create_invoice(user_model: User, invoice_model: InvoiceModelCreateSchema) -> InvoiceModelSchema:

    total = sum([product.price * product.quantity for product in invoice_model.product])

    if total > invoice_model.payment.amount:
        raise HTTPException(status_code=400, detail="Payment funds are not enough to proceed the operation")

    if invoice_model.payment.type == "cash":
        rest = invoice_model.payment.amount - total
    elif invoice_model.payment.type == "cashless":
        rest = 0

    for product in invoice_model.product:
        product.total = product.price * product.quantity

    invoice = InvoiceModelSchema(
        product=invoice_model.product,
        payment=invoice_model.payment,
        total=total,
        rest=rest,
        created_at=datetime.now()
    )
    db_client = InvoiceDatabase()
    invoice_db = db_client.save_invoice_to_db(invoice, user_model)

    return InvoiceModelSchema.model_validate(invoice_db, from_attributes=True)


def get_invoices(user_model: User, page: Page) -> List[InvoiceModelSchema]:
    db_client = InvoiceDatabase()
    invoices = db_client.get_invoices_from_db(page, user_model)

    invoice_models = [InvoiceModelSchema.model_validate(invoice, from_attributes=True) for invoice in invoices]

    return invoice_models
