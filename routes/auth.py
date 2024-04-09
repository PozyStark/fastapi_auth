from datetime import timedelta, datetime, UTC
from uuid import uuid4
from fastapi import APIRouter, Request, Response
from fastapi import Depends
from typing import Annotated
from config import (
    ACCESS_SECRET_KEY,
    REFRESH_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINURES,
    SAVE_IN_COOKIE
)
from enums import TokenType
from dependencies.auth import AuthRequest, get_request_token, get_token
from dependencies.token_session import token_session_service
from dependencies.user import user_service

from dependencies import AuthRequest
from dependencies import BearerAuth
from exceptions import USER_NOT_EXIST, USER_ALLREDY_EXIST
from schemas import AuthinticationScheme, RegistrationScheme, AddTokenSessionSchema, UpdateTokenSessionSchema
from schemas.user import AddUserSchema, UpdateUserSchema
from services.token_session import TokenSessionService
from services.user import UserService
from utils import jwt_token_decode
from utils import create_jwt_token, password_verify


auth_routers = APIRouter()


@auth_routers.post('/registration')
async def registration(
    registration_scheme: RegistrationScheme,
    user_service: Annotated[UserService, Depends(user_service)]
):
    user = await user_service.find_by_username(registration_scheme.username)
    if user:
        raise USER_ALLREDY_EXIST
    add_user = AddUserSchema(**registration_scheme.model_dump())
    user = await user_service.add_one(add_user)

    return {'detail': f'User {user.username} created success'}


@auth_routers.post('/token')
async def token(
    response: Response,         
    authintication_scheme: AuthinticationScheme,
    user_service: Annotated[UserService, Depends(user_service)],
    token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    access_expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expire = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINURES)

    user = await user_service.find_by_username(authintication_scheme.username)

    if user and password_verify(authintication_scheme.password, user.password):
        token = await token_session_service.add_one(AddTokenSessionSchema(user_id=user.id, expire=refresh_expire))
        headers = {
            'token_id': token.id,
            'temp_id': token.temp_id
        }
        payload = {
            'user_id': str(user.id)
        }
        access_token = create_jwt_token(
            key=ACCESS_SECRET_KEY,
            expire=access_expire,
            headers=headers,
            payload=payload
        )
        refresh_token = create_jwt_token(
            key=REFRESH_SECRET_KEY,
            expire=refresh_expire,
            headers=headers,
            payload=payload
        )

        if SAVE_IN_COOKIE:
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True
            )
        await user_service.update(user.id, UpdateUserSchema(last_login=datetime.now(UTC)), exclude_none=True)
        return {'access_token': access_token, 'refresh_token': refresh_token}
    raise USER_NOT_EXIST



@auth_routers.get('/token-verify')
def token_verify(request: Request):
    token = get_token(request)
    if jwt_token_decode(
        jwt_token=token,
        secret_key=ACCESS_SECRET_KEY,
        raise_error=False
    ):
        return {'verify': True}
    return {'verify': False}



@auth_routers.post('/token-refresh')
async def token_refresh(
    response: Response,
    auth_request: Annotated[
        AuthRequest,
        Depends(
            BearerAuth(token_type=BearerAuth.REFRESH_TOKEN)
        )
    ],
    token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    access_expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expire = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINURES)

    updated_token = await token_session_service.update(
        auth_request.request_token.token_id,
        UpdateTokenSessionSchema(temp_id=str(uuid4()), expire=refresh_expire),
        exclude_none=True
    )
    headers = {
        'token_id': auth_request.request_token.token_id,
        'temp_id': updated_token.temp_id
    }
    payload = {
        'user_id': str(auth_request.user.id)
    }

    access_token = create_jwt_token(
        key=ACCESS_SECRET_KEY,
        expire=access_expire,
        headers=headers,
        payload=payload
    )
    refresh_token = create_jwt_token(
        key=REFRESH_SECRET_KEY,
        expire=refresh_expire,
        headers=headers,
        payload=payload
    )

    if SAVE_IN_COOKIE:
        response.set_cookie('access_token', access_token)
        response.set_cookie('refresh_token', refresh_token)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@auth_routers.post('/logout')
async def logout(
    request: Request,
    response: Response,
    token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    token = get_token(request, token_type=TokenType.REFRESH_TOKEN)
    request_token = get_request_token(token, raise_error=False)

    await token_session_service.update(request_token.token_id, UpdateTokenSessionSchema(is_active=False), exclude_none=True)
    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')

    return {'detail': f'token_id: {request_token.token_id} logout success'}


@auth_routers.post('/close-all-sessions')
async def logout(
    request: Request,
    response: Response,
    token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    token = get_token(request, token_type=TokenType.REFRESH_TOKEN)
    request_token = get_request_token(token, raise_error=False)
    
    await token_session_service.close_all_sessions(request_token.user_id, UpdateTokenSessionSchema(is_active=False), exclude_none=True)

    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')

    return {'detail': f'all sessions for: {request_token.user_id} closed success'}


@auth_routers.post('/close-all-sessions-exclude-current')
async def logout(
    request: Request,
    response: Response,
    token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    token = get_token(request, token_type=TokenType.REFRESH_TOKEN)
    request_token = get_request_token(token, raise_error=False)
    
    await token_session_service.close_all_sessions_exclude_current(
        request_token.token_id,
        request_token.user_id,
        UpdateTokenSessionSchema(is_active=False), exclude_none=True
    )

    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')

    return {'detail': f'all sessions for: {request_token.user_id} exclude current {request_token.token_id} closed success'}


@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest,
        Depends(
            BearerAuth(
                required_permissions=[
                    # IsAuthenticated,
                    # IsSuperUser,
                    # StrPermission(required_permission='perm_2'),
                    # StrRole(required_role='string_role_2'),
                    # StrGroup(required_group='string_group_3')
                ]
            )
        )
    ]
):
    return {
        'user':auth_request.user
        # 'request_token': auth_request.request_token.model_dump(),
        # 'token_session': auth_request.token_session.model_dump(),
        # 'user': auth_request.user.model_dump()
    }