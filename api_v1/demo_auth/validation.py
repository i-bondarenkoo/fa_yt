from unittest.util import strclass
from fastapi.security import OAuth2PasswordBearer
from api_v1.demo_auth.crud import users_db
from auth import utils as auth_utils
from fastapi import Depends, HTTPException, status, Form
from jwt.exceptions import InvalidTokenError
from api_v1.demo_auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-auth/jwt/login/",
)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неправильный username или password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не активен",
        )
    return user


def get_current_token_payload(
    token: strclass = Depends(oauth2_scheme),
) -> dict:

    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"передан не верный токен: {e}",
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"неправильный тип токена {current_token_type!r} ожидается {token_type!r}",
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="не действительный токен (пользователь не найден)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(
        self,
        token_type: str,
    ):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="пользователь не активен",
    )


# def get_current_auth_user(
#     payload: dict = Depends(get_current_token_payload),
# ) -> UserSchema:
#     validate_token_type(
#         payload,
#         ACCESS_TOKEN_TYPE,
#     )
#     return get_user_by_token_sub(payload)


# def get_current_auth_user_for_refresh(
#     payload: dict = Depends(get_current_token_payload),
# ):
#     validate_token_type(
#         payload,
#         REFRESH_TOKEN_TYPE,
#     )

#     return get_user_by_token_sub(payload)
