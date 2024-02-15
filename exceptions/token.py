from fastapi import HTTPException, status


TOKEN_TYPE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="invalid token_type",
    headers={"WWW-Authenticate": "Bearer"}
)

TOKEN_ID_NOT_EXIST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="token_id does not exist",
    headers={"WWW-Authenticate": "Bearer"}
)

TEMP_ID_NOT_EXIST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="such temp_id does not exist",
    headers={"WWW-Authenticate": "Bearer"}
)

TOKEN_SESSION_NOT_ACTIVE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="token not active",
    headers={"WWW-Authenticate": "Bearer"}
)

TOKEN_DECODE_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Token decode error",
    headers={"WWW-Authenticate": "Bearer"}
)