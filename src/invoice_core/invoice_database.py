from src.db_client import _get_DB_Client, DatabaseClient
from src.invoice_core.schemas import InvoiceModelSchema
from src.invoice_core.models import (
    Products,
    Payment,
    Invoice
)
from sqlalchemy.orm import Session
from typing import List
from src.invoice_core.schemas import Page


class InvoiceDatabase:

    _DB_Client: DatabaseClient
    session: Session

    def __init__(self):
        self._DB_Client = _get_DB_Client()
        self.session = Session(
            self._DB_Client._engine,
            expire_on_commit=True,
            autoflush=False
        )

    def save_invoice_to_db(self, invoice_to_create: InvoiceModelSchema) -> Invoice:
        invoice_db = Invoice(
            total=invoice_to_create.total,
            rest=invoice_to_create.rest
        )

        for product_data in invoice_to_create.products:
            product_db = Products(
                **product_data.model_dump(),
                invoice=invoice_db,
            )
            invoice_db.products.append(product_db)

        payment_db = Payment(
            **invoice_to_create.payment.model_dump(),
            invoice=invoice_db
        )
        invoice_db.payment = payment_db

        self.session.add(invoice_db)
        self.session.commit()

        self.session.refresh(invoice_db)

        return invoice_db

    def get_invoices_from_db(self, page: Page) -> List[Invoice]:
        query = self.session.query(Invoice).join(Payment)

        # Sotring by invoice date of creation
        if page.start_date:
            query = query.filter(Invoice.created_at >= page.start_date)
        if page.end_date:
            query = query.filter(Invoice.created_at <= page.end_date)

        # Sorting by invoice amount
        if page.total_amount_min:
            query = query.filter(Invoice.total >= page.total_amount_min)
        if page.total_amount_max:
            query = query.filter(Invoice.total <= page.total_amount_max)

        # Sorting by invoice payment type
        if page.payment_type:
            query = query.filter(Payment.type == page.payment_type)

        invoices = query.offset(page.page_num * page.page_size).limit(page.page_size).all()

        return invoices
