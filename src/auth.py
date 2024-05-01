from fastapi import Header, HTTPException
from src.auth_core.schemas import CurrentUserInfo
import jwt
from jwt.exceptions import DecodeError 


# def get_current_user_into(authorization: str = Header()) -> CurrentUserInfo:
    # try:
    #     authorization = jwt.decode(authorization, options={"vetify_signature": True})
    #     return CurrentUserInfo()
    # except (DecodeError, KeyError) as error:
    #     raise HTTPException(
    #         status_code=403,
    #         detail=str(error)
    #     )

def get_current_user_into() -> CurrentUserInfo:
    # try:
    #     authorization = jwt.decode(authorization, options={"vetify_signature": True})
    #     return CurrentUserInfo()
    # except (DecodeError, KeyError) as error:
    #     raise HTTPException(
    #         status_code=403,
    #         detail=str(error)
    #     )
    return CurrentUserInfo(user_name="Vitaliy", email="somemail@gmail.com")
