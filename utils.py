from config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
from fastapi import HTTPException
from jwt import DecodeError, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
# from services import get_user_by_username
from exceptions import TOKEN_DECODE_ERROR
import jwt


ENCRYPT = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_hashed_password(password: str) -> str:
#     return ENCRYPT.hash(password)


# def password_verify(
#     plane_password: str,
#     hashed_password: str
# ) -> bool:
#     return ENCRYPT.verify(plane_password, hashed_password)


# async def authinticate_user(
#     async_session: AsyncSession,
#     username: str,
#     password: str
# ) -> User | None:
#     user = await get_user_by_username(async_session, username)
#     if not user:
#         return None
#     if not password_verify(password, user.hashed_password):
#         return None
#     return user


# def jwt_token_decode(
#     jwt_token: str
# ) -> dict | None:
#     try:
#         decoded_token = jwt.decode(
#             jwt=jwt_token,
#             key=SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )
#         return decoded_token
#     except DecodeError:
#         return None
#     except ExpiredSignatureError:
#         return None    


# def jwt_headers(
#     jwt_token: str
# ) -> dict:
#     return jwt.get_unverified_header(jwt_token)


# def jwt_payload(
#     jwt_token: str
# ) -> dict | None:
#     return jwt_token_decode(jwt_token)


# def create_jwt_token(
#     expire: datetime,
#     headers: dict | None = None,
#     payload: dict | None = None
# ) -> str | None:
#     if payload:
#         payload_copy = payload.copy()
#     payload_copy.update({'exp': expire})
#     token = jwt.encode(
#         headers=headers,
#         payload=payload_copy,
#         key=SECRET_KEY,
#         algorithm=ALGORITHM
#     )
#     return token
