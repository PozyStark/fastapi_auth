from fastapi import HTTPException
from starlette import status


TOKEN_DECODE_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Token decode error",
    headers={"WWW-Authenticate": "Bearer"}
)

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"}
)

UNAUTHORIZED_NO_SUCH_TOKEN_ID = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No token with this token_id",
    headers={"WWW-Authenticate": "Bearer"}
)

UNAUTHORIZED_TOKEN_NOT_VERIFYED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token not verifyed",
    headers={"WWW-Authenticate": "Bearer"}
)

UNAUTHORIZED_NO_SUCH_USER = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No such user or bad password",
    headers={"WWW-Authenticate": "Bearer"}
)

UNAUTHORIZED_NOT_PERMITED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not permited for this user",
    headers={"WWW-Authenticate": "Bearer"}
)

TOKEN_ID_NOT_UUID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="token_id must be a uuid",
    headers={"WWW-Authenticate": "Bearer"}
)