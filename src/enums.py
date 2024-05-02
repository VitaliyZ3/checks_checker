from enum import Enum
from typing import Any


class StrEnum(str, Enum):
    pass


class EnumToListMixin(Enum):
    @classmethod
    def to_list(cls) -> list[Any]:
        return [f.value for f in cls]