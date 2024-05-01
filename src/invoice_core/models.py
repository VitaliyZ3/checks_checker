from sqlalchemy import ForeignKey, func
from sqlalchemy import String
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column


Base = declarative_base()


class Products(Base):
    __tablename__ = "Products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(36))
    price: Mapped[int]
    quantity: Mapped[int]
    total: Mapped[int]
    invoice: Mapped["Invoice"] = relationship(back_populates="products", uselist=False)
    invoice_fk: Mapped[int] = mapped_column(ForeignKey('invoices.id'))


class PaymentType(Base):
    __tablename__ = "payment_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(8))


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_type: Mapped["PaymentType"] = relationship(uselist=True)
    payment_type_fk: Mapped[int] = mapped_column(ForeignKey('payment_types.id'))
    invoice: Mapped["Invoice"] = relationship(back_populates="payment", uselist=False)


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    products: Mapped[list["Products"]] = relationship(back_populates="invoice", uselist=True)
    payment: Mapped["Payment"] = relationship(back_populates="invoice", uselist=False)
    payment_fk: Mapped[int] = mapped_column(ForeignKey("payments.id"))
    total: Mapped[int]
    rest: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
