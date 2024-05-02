from fastapi import Depends
from fastapi_users_db_sync_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session

from src.auth_core.models import User
from src.db_client import _get_db_session


def get_user_db(session: Session = Depends(_get_db_session)):
    return SQLAlchemyUserDatabase(session, User)
