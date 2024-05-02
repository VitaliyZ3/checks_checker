from sqlalchemy import ForeignKey, func
from sqlalchemy import String
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from src.auth_core.models import User
from src.base import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(36))
    price: Mapped[int]
    quantity: Mapped[int]
    total: Mapped[int]
    invoice: Mapped["Invoice"] = relationship(back_populates="product",
                                              uselist=False)
    invoice_fk: Mapped[int] = mapped_column(ForeignKey('invoice.id'))


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(8))
    amount: Mapped[int]
    invoice: Mapped["Invoice"] = relationship(back_populates="payment",
                                              uselist=False)


class Invoice(Base):
    __tablename__ = "invoice"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[User] = relationship(uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))

    product: Mapped[list["Product"]] = relationship(back_populates="invoice",
                                                      uselist=True)
    payment: Mapped["Payment"] = relationship(back_populates="invoice",
                                              uselist=False)
    payment_fk: Mapped[int] = mapped_column(ForeignKey("payment.id"))
    total: Mapped[int]
    rest: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())