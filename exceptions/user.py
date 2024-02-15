from fastapi import HTTPException
from starlette import status


USER_NOT_EXIST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User not exist or bad password",
    headers={"WWW-Authenticate": "Bearer"}
)

USER_NOT_ACTIVE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User not active",
    headers={"WWW-Authenticate": "Bearer"}
)

USER_ALLREDY_EXIST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already exist",
    headers={"WWW-Authenticate": "Bearer"}
)