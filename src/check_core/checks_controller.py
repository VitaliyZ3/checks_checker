from fastapi import APIRouter, Request
from src.check_core import checks_service
router = APIRouter()


@router.post(
    "",
)
def create_check(request: Request):
    return checks_service.create_check(
        request=request
    )


@router.get(
    "",
)
def get_check_data(request: Request):
    return checks_service.get_check_data(
        request=request
    )