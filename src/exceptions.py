# service exceptions

class CalculationError(BaseException):
    pass


class TotalIncorrectError(CalculationError):
    pass


# database exceptions

from sqlalchemy.exc import SQLAlchemyError


class UnprocessableEntity(SQLAlchemyError):
    pass
