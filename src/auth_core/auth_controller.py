from fastapi import APIRouter
from src.auth_core.auth.base_config import auth_backend
from src.auth_core.auth.base_config import fastapi_users
from src.auth_core.schemas import UserRead, UserCreate


router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
