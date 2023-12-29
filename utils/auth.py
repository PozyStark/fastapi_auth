from config import SECRET_KEY, ALGORITHM, SCHEMES, DEPRECATED
from dependencies import user_service, token_session_service
from datetime import datetime, timedelta
from fastapi import HTTPException
from jwt import DecodeError, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
# from services import get_user_by_username
from exceptions import TOKEN_DECODE_ERROR
import jwt
from typing import Annotated
from fastapi import Depends
from services import UserService, TokenSessionService
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINURES


ENCRYPT = CryptContext(schemes=SCHEMES, deprecated=DEPRECATED)


def get_hashed_password(password: str) -> str:
    return ENCRYPT.hash(password)


def password_verify(
    plane_password: str,
    hashed_password: str
) -> bool:
    return ENCRYPT.verify(plane_password, hashed_password)


def jwt_token_decode(
    jwt_token: str = ...,
    auto_error: bool = True
) -> dict | None | HTTPException:
    if not jwt_token:
        return None
    try:
        token_payload = jwt.decode(
            jwt=jwt_token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        token_headers = jwt.get_unverified_header(jwt_token)
        return {'headers': token_headers, 'payload': token_payload}
    except DecodeError:
        if auto_error:
            raise HTTPException(401, 'decode error')
        return None
    except ExpiredSignatureError:
        if auto_error:
            raise HTTPException(401, 'token expired')
        return None


def create_jwt_token(
    expire: datetime,
    headers: dict | None = None,
    payload: dict | None = None,
    key: str = SECRET_KEY,
    algoritm: str = ALGORITHM
) -> str | None:
    if payload:
        payload_copy = payload.copy()
    payload_copy.update({'exp': expire})
    token = jwt.encode(
        headers=headers,
        payload=payload_copy,
        key=key,
        algorithm=algoritm
    )
    return token