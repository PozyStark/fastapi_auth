from enum import Enum
from fastapi import Depends, HTTPException, Request
from datetime import datetime, timedelta
from typing import Annotated, Any
from pydantic import BaseModel
from dependencies import user_service, token_session_service
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINURES
from exceptions import UNAUTHORIZED_NOT_PERMITED, UNAUTHORIZED_TOKEN_NOT_VERIFYED, UNAUTHORIZED_NO_SUCH_TOKEN_ID
from schemas import AuthinticationScheme, AddTokenSessionSchema, Token
from services import UserService, TokenSessionService
from utils import create_jwt_token, jwt_token_decode
from interfaces import AbstractPermission
from data import AuthRequest
from core import IsAuthenticated, BasePermission, StrPermission


async def auth_token_pair(
        authintication_scheme: AuthinticationScheme,
        user_service: Annotated[UserService, Depends(user_service)],
        token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
) -> dict:
    access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINURES)

    user = await user_service.find_by_username(authintication_scheme.username)

    if user:
        token = await token_session_service.add_one(AddTokenSessionSchema(user_id=user.id, expire=refresh_expire))
        headers = {
            'token_id': token.id
        }
        payload = {
            'user_id': str(user.id)
        }
    access_token = create_jwt_token(
        expire=access_expire,
        headers=headers,
        payload=payload
    )
    refresh_token = create_jwt_token(
        expire=refresh_expire,
        headers=headers,
        payload=payload
    )

    return {'access_token': access_token, 'refresh_token': refresh_token}


class SearchMode(Enum):
    HEADER_MODE = 0
    COOKIE_MODE = 1


class TokenType(Enum):
    ACCESS_TOKEN = 0
    REFRESH_TOKEN = 1


class BearerAuth:

    HEADER_MODE: int = SearchMode.HEADER_MODE
    COOKIE_MODE: int = SearchMode.COOKIE_MODE

    ACCESS_TOKEN: int = TokenType.ACCESS_TOKEN
    REFRESH_TOKEN: int = TokenType.REFRESH_TOKEN

    token_type: TokenType
    search_mode: SearchMode
    # verify_token_signature: bool
    # verify_token_id: bool
    required_permissions: list[AbstractPermission]

    def __init__(
        self,
        token_type: TokenType = ACCESS_TOKEN,
        # verify_token_signature: bool = True,
        # verify_token_id: bool = True,
        search_mode: SearchMode = COOKIE_MODE,
        auto_error: bool = True,
        required_permissions: list[AbstractPermission] = list(),
    ):
        self.token_type = token_type
        self.auto_error = auto_error
        self.search_mode = search_mode
        # self.verify_token_signature = verify_token_signature
        # self.verify_token_id = verify_token_id
        self.required_permissions = required_permissions

    def __get_token(self, request: Request) -> str | None:
        request_dict: dict = dict()
        if self.search_mode == SearchMode.COOKIE_MODE:
            request_dict = request.cookies
        if self.search_mode == SearchMode.HEADER_MODE:
            request_dict = request.headers
        if self.token_type == TokenType.ACCESS_TOKEN:
            return request_dict.get('access_token')
        if self.token_type == TokenType.REFRESH_TOKEN:
            return request_dict.get('refresh_token')
        
    def __has_permissions(
        self,
        auth_request: AuthRequest,
    ) -> bool | HTTPException:
        auth_data = dict(auth_request=auth_request, auto_error=self.auto_error)
        for perm in self.required_permissions:
            if not perm(**auth_data).has_permission():
                return False
        return True

    async def __get_auth_request(
        self,
        request: Request,
        user_service: UserService,
        token_session_service: TokenSessionService
    ) -> AuthRequest:
        
        token = self.__get_token(request)

        auth_request = AuthRequest(
            headers=request.headers,
            cookies=request.cookies,
            token=token
        )

        decoded_token = jwt_token_decode(token, self.auto_error)

        if decoded_token:
            token_headers: dict = decoded_token.get('headers')
            token_payload: dict = decoded_token.get('payload')

            auth_request.token_id = token_headers.get('token_id')
            auth_request.user_id = token_payload.get('user_id')

            token_id = token_headers.get('token_id')
            user_id = token_payload.get('user_id')

            token_exist = await token_session_service.find_by_id(token_id)

            if self.auto_error and not token_exist:
                raise HTTPException(401, "token not exist") # *
            
            if token_exist:
                auth_request.is_authinticated = True

                user = await user_service.find_by_id(user_id)

                if self.auto_error and not user:
                    raise HTTPException(401, "No such user") # *

                roles = await user_service.find_user_roles_by_id(user_id)
                groups = await user_service.find_user_groups_by_id(user_id)
                user_permissions = await user_service.find_user_permissions_by_id(user_id)

                auth_request.user_permissions = user_permissions
                auth_request.is_superuser = user.is_superuser
                auth_request.user_groups = groups
                auth_request.user_roles = roles

        return auth_request
    
    async def __call__(
        self,
        request: Request,
        user_service: Annotated[UserService, Depends(user_service)],
        token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
    ) -> AuthRequest | HTTPException:

        auth_request = await self.__get_auth_request(request, user_service, token_session_service)

        has_permissions = self.__has_permissions(auth_request)

        print(f'has_permissions-{has_permissions}')

        return auth_request