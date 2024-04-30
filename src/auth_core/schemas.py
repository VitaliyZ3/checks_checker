from pydantic import BaseModel


class CurrentUserInfo(BaseModel):
    user_name: str
    email: str
