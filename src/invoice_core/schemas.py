from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Literal
from fastapi import Query
from src.config import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE
)


class Page(BaseModel):
    page_size: Optional[int] = Field (Query(DEFAULT_PAGE_SIZE, description="Page Size"))
    page_num: int = Field (Query(DEFAULT_PAGE_NUMBER, description="Page number", ge=0))
    total_amount_min: Optional[int] = Field (Query(None, description="Minimun invoice sum"))
    total_amount_max: Optional[int] = Field (Query(None, description="Maximum invoice sum"))
    start_date: Optional[datetime] = Field (Query(None, description="Invoice start date (from)"))
    end_date: Optional[datetime] = Field (Query(None, description="Invoice start date (to)"))
    payment_type: Optional[Literal["cash", "cashless"]] = Field (Query(None, description="Invoice payment type"))


class Product(BaseModel):
    name: str
    price: int
    quantity: int
    total: int = None


class Payment(BaseModel):
    type: Literal['cash', 'cashless']
    amount: int


class InvoiceModelCreateSchema(BaseModel):
    product: List[Product]
    payment: Payment


class InvoiceModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(None, description="Id of created invoice")
    product: List[Product]
    payment: Payment
    total: int
    rest: int
    created_at: datetime
