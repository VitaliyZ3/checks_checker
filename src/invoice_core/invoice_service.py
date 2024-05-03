from typing import List
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from src.invoice_core.schemas import (
    Page,
    InvoiceModelCreateSchema,
    InvoiceModelSchema
)
from src.invoice_core.invoice_database import InvoiceDatabase
from src.auth_core.models import User
from src.invoice_core.utils.invoice_text_generator import InvoiceTextGenerator
from src import config
from src.exceptions import TotalIncorrectError
# This file is using for storing all Invoice business logic


def create_invoice(user_model: User, invoice_model: InvoiceModelCreateSchema) -> InvoiceModelSchema:
    try:
        invoice = _calculate_invoice_model(invoice_model)
    except TotalIncorrectError:
        raise HTTPException(status_code=400, detail="Payment funds are not enough to proceed the operation")

    db_client = InvoiceDatabase()

    try:
        invoice_db = db_client.save_invoice_to_db(invoice, user_model)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=e._message)

    invoice_model = InvoiceModelSchema.model_validate(invoice_db, from_attributes=True)
    invoice_text = _create_invoice_text(invoice, username=invoice_db.user.email)

    try:
        invoice_file_path = _create_invoice_text_file(
            invoice_text=invoice_text,
            invoice_id=invoice_db.id,
            user_id=invoice_db.user_fk
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error ocured while saving invoice text file")

    db_client.save_invoice_file(
        invoice_id=invoice_db.id,
        file_path=invoice_file_path
    )
    return invoice_model


def get_invoices(user_model: User, page: Page) -> List[InvoiceModelSchema]:
    db_client = InvoiceDatabase()
    try:
        invoices = db_client.get_invoices_from_db(page, user_model)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=e._message)

    invoice_models = [InvoiceModelSchema.model_validate(invoice, from_attributes=True) for invoice in invoices]
    return invoice_models


def get_invoice_print_file(invoice_id: int) -> str:
    db_client = InvoiceDatabase()
    try:
        invoice_model = db_client.get_invoice_by_id(invoice_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=e._message)

    return invoice_model.text_invoice_file_path


def _create_invoice_text(invoice_model: InvoiceModelSchema, username: str) -> str:
    invoice_text_gen = InvoiceTextGenerator(
        invoice=invoice_model,
        line_length=40,
        username=username
    )
    invoice_text = invoice_text_gen.generate_invoice_text()
    return invoice_text


def _create_invoice_text_file(invoice_text: str, invoice_id: int, user_id: int) -> str:
    file_path = f"{config.FILE_STORAGE_PATH}/{invoice_id}.txt"
    with open(file_path, "w") as file:
        file.write(invoice_text)
    return file_path


def _calculate_invoice_model(invoice_model: InvoiceModelCreateSchema) -> InvoiceModelSchema:
    # Here we calculate total for product, rest and total for invoice

    total = sum([product.price * product.quantity for product in invoice_model.product])

    if total > invoice_model.payment.amount:
        raise TotalIncorrectError()

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
    return invoice