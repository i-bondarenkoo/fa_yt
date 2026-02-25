from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, Depends, HTTPException, status, Header
import secrets

router = APIRouter(
    prefix="/demo-auth",
    tags=["Demo Auth"],
)

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_password = {
    "admin": "admin",
    "john": "secret",
}


static_auth_token_to_username = {
    "d79ecaff459f187a18336a4fb33335": "admin",
    "35bf1d248b8dbec1621390d7346b9f": "secret",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if static_token not in static_auth_token_to_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="неверный токен",
        )
    return static_auth_token_to_username[static_token]


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не правильный логин или пароль",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_password.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi! {auth_username}",
        "username": auth_username,
    }


@router.get("/some-http-header-auth/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi! {username}",
        "username": username,
    }
