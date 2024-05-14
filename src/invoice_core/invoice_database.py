from sqlalchemy.orm import Session
from typing import List
from src.db_client import _get_DB_Client, DatabaseClient
from src.invoice_core.schemas import InvoiceModelSchema
from src.invoice_core.models import (
    Product,
    Payment,
    Invoice
)
from src.invoice_core.schemas import Page
from src.auth_core.models import User


class InvoiceDatabase:
    """
    Class is using like a database connector for invoice operation
    If you need particular invoice db iteration, please extend this class
    by writing new methods

    Using in invoice_service.py
    """

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

        for product_data in invoice_to_create.product:
            product_db = Product(
                **product_data.model_dump(),
                invoice=invoice_db,
            )
            invoice_db.product.append(product_db)

        payment_db = Payment(
            **invoice_to_create.payment.model_dump(),
            invoice=invoice_db
        )
        invoice_db.payment = payment_db
        # invoice_db.user_fk = user_model.id
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

        # Filtering by user
        # if user_model:
        #     query = query.filter(Invoice.user_fk == user_model.id)

        invoices = query.offset(page.page_num * page.page_size).limit(page.page_size).all()

        return invoices

    def get_invoice_by_id(self, invoice_id: int) -> Invoice:
        return self.session.query(Invoice).filter(Invoice.id == invoice_id).first()

    def save_invoice_file(self, invoice_id: int, file_path: str) -> Invoice:
        invoice_db = self.session.query(Invoice).filter(Invoice.id == invoice_id).first()
        invoice_db.text_invoice_file_path = file_path
        self.session.add(invoice_db)
        self.session.commit()
        return invoice_db
