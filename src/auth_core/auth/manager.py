from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)

from src.auth_core.models import User
from src.auth_core.auth.utils import get_user_db
from src.config import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_AUTH
    verification_token_secret = settings.SECRET_AUTH


def get_user_manager(user_db=Depends(get_user_db)):
    return UserManager(user_db)
