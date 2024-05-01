from pydantic import BaseModel, Field
from datetime import datetime
from src.enums import (
    SortOrder,
    InvoiceOrderingFields
)
    
from typing import Optional, List, Literal


class Page(BaseModel):
    page_size: int
    page_num: int
    order_by: Optional[InvoiceOrderingFields]
    sort_order: SortOrder = SortOrder.asc


class Product(BaseModel):
    name: str
    price: int
    quantity: int
    total: int


class PaymentType(BaseModel):
    name: Literal['cash', 'cashless']


class Payment(BaseModel):
    type: PaymentType
    amount: int


class InvoiceModelCreateSchema(BaseModel):
    products: List[Product]
    payment: Payment


class InvoiceModelSchema(BaseModel):
    id: int = Field(None, description="Id of created invoice")
    products: List[Product]
    payment: Payment
    total: int
    rest: int
    created_at: datetime
