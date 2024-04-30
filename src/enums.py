from enum import Enum
from typing import Any


class StrEnum(str, Enum):
    pass


class EnumToListMixin(Enum):
    @classmethod
    def to_list(cls) -> list[Any]:
        return [f.value for f in cls]


class InvoiceOrderingFields(EnumToListMixin, StrEnum):
    date = "date"
    amount = "amount"
    payment_type = "payment_type"


class SortOrder(StrEnum):
    asc = "asc"
    desc = "desc"
