from fastapi import Depends, HTTPException, Request
from typing import Annotated
from dependencies import user_service, token_session_service
from config import SEARCH_MODE
from exceptions import (
    TOKEN_TYPE_EXCEPTION,
    TOKEN_ID_NOT_EXIST,
    TEMP_ID_NOT_EXIST,
    TOKEN_SESSION_NOT_ACTIVE,
    USER_NOT_EXIST,
    USER_NOT_ACTIVE
)
from schemas import RequestToken, RequestUser
from services import UserService, TokenSessionService
from utils import jwt_token_decode
from interfaces import AbstractPermission
from enums import TokenType, SearchMode


def get_token(
    request: Request,
    search_mode: SearchMode = SEARCH_MODE,
    token_type: TokenType = TokenType.ACCESS_TOKEN
) -> str | None:
    if search_mode == SearchMode.COOKIE_MODE:
        token = request.cookies.get(token_type.name.lower())
        return token
    if search_mode == SearchMode.HEADER_MODE:
        token = request.headers.get(token_type.name.lower())
        return token


def get_request_token(token: str, raise_error: bool = True) -> RequestToken:
    decoded_token = jwt_token_decode(token, raise_error)

    token_headers: dict = decoded_token.get('headers', dict())
    token_payload: dict = decoded_token.get('payload', dict())

    return RequestToken(
        token=token,
        **token_headers,
        **token_payload
    )


class AuthRequest:

    request: Request = None
    request_token: RequestToken = None
    user: RequestUser = None

    __search_mode: SearchMode
    __token_type: TokenType

    def __init__(
        self,
        request: Request,
        token_type: TokenType,
        search_mode: SearchMode
    ):
        self.request = request
        self.__search_mode = search_mode
        self.__token_type = token_type
        self.request_token = self.__get_request_token(
            self.__get_token(request)
        )
    
    def __get_token(
        self,
        request: Request
    ) -> str | None:
        return get_token(request, self.__search_mode,  self.__token_type)
        
    def __get_request_token(self, token: str) -> RequestToken:
        return get_request_token(token)

    async def __validate_token_session(self, token_session_service: TokenSessionService) -> None:
        token_session = await token_session_service.find_by_id(self.request_token.token_id)
        if self.request_token.token:
            if not token_session:
                raise TOKEN_ID_NOT_EXIST
            if not token_session.is_active:
                raise TOKEN_SESSION_NOT_ACTIVE
            if self.request_token.token_type != self.__token_type.value:
                raise TOKEN_TYPE_EXCEPTION
            if self.request_token.temp_id != token_session.temp_id:
                raise TEMP_ID_NOT_EXIST
    
    async def __find_user(self, user_service: UserService) -> RequestUser:
        user = await user_service.find_by_id(self.request_token.user_id)
        if self.request_token.token:
            if not user:
                raise USER_NOT_EXIST
            if not user.is_active:
                raise USER_NOT_ACTIVE
            return RequestUser(**user.__dict__)
        return RequestUser()

    async def __find_user_permissions(self, user_service: UserService) -> list[str]:
        user_permissions = await user_service.find_user_permissions_by_id(self.request_token.user_id)
        return user_permissions
    
    async def __find_user_roles(self, user_service: UserService) -> list[str]:
        user_roles = await user_service.find_user_roles_by_id(self.request_token.user_id)
        return user_roles

    async def __find_user_groups(self, user_service: UserService) -> list[str]:
        user_groups = await user_service.find_user_groups_by_id(self.request_token.user_id)
        return user_groups

    async def __call__(
        self,
        token_session_service: TokenSessionService,
        user_service: UserService
    ):

        await self.__validate_token_session(token_session_service)

        self.user = await self.__find_user(user_service)

        if self.user.is_active:
            self.user.user_permissions = await self.__find_user_permissions(user_service)
            self.user.user_roles = await self.__find_user_roles(user_service)
            self.user.user_groups = await self.__find_user_groups(user_service)
            self.user.is_authinticated = True

        return self


class BearerAuth:

    HEADER_MODE = SearchMode.HEADER_MODE
    COOKIE_MODE = SearchMode.COOKIE_MODE

    ACCESS_TOKEN = TokenType.ACCESS_TOKEN
    REFRESH_TOKEN = TokenType.REFRESH_TOKEN

    token_type: TokenType
    search_mode: SearchMode

    required_permissions: list[AbstractPermission]

    def __init__(
        self,
        search_mode: SearchMode = SEARCH_MODE,
        token_type: TokenType = ACCESS_TOKEN,
        required_permissions: list[AbstractPermission] = list(),
    ):
        self.token_type = token_type
        self.search_mode = search_mode
        self.required_permissions = required_permissions

    def __has_permission(
        self,
        auth_request: AuthRequest,
    ) -> bool | HTTPException:
        auth_data = dict(auth_request=auth_request)
        for perm in self.required_permissions:
            perm(**auth_data).has_permission()
            
    async def __get_auth_request(
        self,
        request: Request,
        user_service: UserService,
        token_session_service: TokenSessionService
    ) -> AuthRequest:

        auth_request = AuthRequest(request, self.token_type, self.search_mode)
        auth_request = await auth_request(token_session_service, user_service)
        self.__has_permission(auth_request)

        return auth_request
    
    async def __call__(
        self,
        request: Request,
        user_service: Annotated[UserService, Depends(user_service)],
        token_session_service: Annotated[TokenSessionService, Depends(token_session_service)]
    ) -> AuthRequest | HTTPException:

        auth_request = await self.__get_auth_request(request, user_service, token_session_service)
        return auth_request