from config import (
    ALGORITHM,
    ACCESS_SECRET_KEY,
    REFRESH_SECRET_KEY,
    SCHEMES,
    DEPRECATED
)
from datetime import datetime
from fastapi import HTTPException
from jwt import DecodeError, ExpiredSignatureError
from passlib.context import CryptContext
import jwt


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
    secret_key: str = ...,
    raise_error: bool = True
) -> dict | HTTPException:
    if not jwt_token:
        return dict()
    try:
        token_payload = jwt.decode(
            jwt=jwt_token,
            key=secret_key,
            algorithms=[ALGORITHM]
        )
        token_headers = jwt.get_unverified_header(jwt_token)
        return {'headers': token_headers, 'payload': token_payload}
    except DecodeError:
        if raise_error:
            raise HTTPException(401, 'decode error')
        return dict()
    except ExpiredSignatureError:
        if raise_error:
            raise HTTPException(401, 'token expired')
        return dict()


def create_jwt_token(
    key: str,
    expire: datetime,
    algoritm: str = ALGORITHM,
    headers: dict | None = None,
    payload: dict | None = None,
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