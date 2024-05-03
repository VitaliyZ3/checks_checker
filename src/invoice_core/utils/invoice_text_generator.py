from datetime import datetime
from src.invoice_core.schemas import (
    InvoiceModelSchema,
    Product,
    Payment
)


class InvoiceTextGenerator():
    """
    Class InvoiceTextGenerator is used for generation
    invoice print text from InvoiceModelSchema

    line_length: length of you`r printed invoice
    username: name of the user, whom created invoice
    """
    invoice: InvoiceModelSchema
    line_length: str
    username: str

    def __init__(self, invoice: InvoiceModelSchema, line_length: int, username: str) -> None:
        self.invoice = invoice
        self.line_length = line_length
        self.username = username

    def _generate_separator(self, char: str = '-') -> str:
        return char * self.line_length

    def _format_product_line(self, product: Product) -> str:
        return f"{product.quantity} x {product.price:>10,.2f}\n{product.name:<29} {product.total:>10,.2f}"

    def _format_total_line(self, total: int) -> str:
        return f"{'СУМА':<29} {total:>10,.2f}"

    def _format_payment_line(self, payment: Payment) -> str:
        return f"{'Картка':<29} {payment.amount:>10,.2f}"

    def _format_rest_line(self, rest: int) -> str:
        return f"{'Решта':<29} {rest:>10,.2f}"

    def _format_datetime_line(self, created_at: datetime) -> str:
        return f"{'Дата та час':<23} {created_at:%d.%m.%Y %H:%M}"

    def generate_invoice_text(self) -> str:
        receipt_text = ""
        receipt_text += f"{f'ФОП {self.username}':^40}\n"
        receipt_text += self._generate_separator('=') + '\n'

        for product in self.invoice.product:
            receipt_text += self._format_product_line(product) + '\n'
            receipt_text += self._generate_separator('-') + '\n'

        receipt_text += self._format_total_line(self.invoice.total) + '\n'
        receipt_text += self._format_payment_line(self.invoice.payment) + '\n'
        receipt_text += self._format_rest_line(self.invoice.rest) + '\n'

        receipt_text += self._generate_separator('=') + '\n'

        receipt_text += self._format_datetime_line(self.invoice.created_at) + '\n'

        receipt_text += f"{'Дякуємо за покупку!':^40}\n"

        return receipt_text
