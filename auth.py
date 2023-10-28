from enum import Enum
import random
from typing import Annotated, Any, AsyncGenerator
import uuid
from fastapi.param_functions import Form
from fastapi import Depends, HTTPException, Request
import jwt
from pydantic import BaseModel
from sqlalchemy import select
from exceptions import UNAUTHORIZED_NOT_PERMITED, UNAUTHORIZED_TOKEN_NOT_VERIFYED, UNAUTHORIZED_NO_SUCH_TOKEN_ID, TOKEN_DECODE_ERROR, TOKEN_ID_NOT_UUID
from models import Permission, User
from permissions import AllowAny, BasePermission
from schemas.auth import AccessToken, RefreshToken
from core.request import AuthRequest
from utils import jwt_headers, jwt_payload, jwt_token_decode
from sqlalchemy.ext.asyncio import AsyncSession
from databases import async_session

from services.token_session import TokenSessionService
from services.user import UserService
from services.user_role import UserRoleService
from services.user_group import UserGroupService


from dependencies import token_session_service, user_service, user_role_service, user_group_service


class SearchMode(Enum):
    HEADER_MODE = 0
    COOKIE_MODE = 1
    

class BearerAuth:

    HEADER_MODE: int = SearchMode.HEADER_MODE
    COOKIE_MODE: int = SearchMode.COOKIE_MODE

    token_type: AccessToken | RefreshToken
    search_mode: SearchMode
    verify_token_signature: bool
    verify_token_id: bool
    required_permission: list[BasePermission | str]

    def __init__(
        self,
        token_type: AccessToken | RefreshToken,
        verify_token_signature: bool = True,
        verify_token_id: bool = True,
        search_mode: SearchMode = COOKIE_MODE,
        auto_error: bool = True,
        required_permission: list[BasePermission | str] = None
    ):
        self.token_type = token_type
        self.auto_error = auto_error
        self.search_mode = search_mode
        self.verify_token_signature = verify_token_signature
        self.verify_token_id = verify_token_id
        self.required_permission = required_permission


    @staticmethod
    async def check_permission(
        permission: BasePermission | str,
        auth_request: AuthRequest
    ) -> bool | ValueError:
        user_permissions = auth_request.context.get('user_permissions', None)
        if not user_permissions:
            return False
        if isinstance(permission, str):
            if permission in user_permissions:
                return True
            return False
        elif issubclass(permission, BasePermission):
            return await permission.has_permission(auth_request, async_session, False)
        raise ValueError(permission)


    def __get_token(
        self,
        token: AccessToken | RefreshToken | None = None
    ) -> str | None:
        if isinstance(token, AccessToken):
            return token.access_token
        if isinstance(token, RefreshToken):
            return token.refresh_token

        
    async def __verify_token_id(
        self,
        service: Annotated[TokenSessionService, Depends(token_session_service)],
        token: str
    ) -> bool:
        
        token_id = jwt_headers(token).get('token_id')
        
        token_in_base = await service.find_by_id(token_id)

        if not token_in_base:
            return False
        
        return True
    

    async def __is_authinticated(self, token: str) -> bool | HTTPException:

        if not token:
            return False

        if not jwt_token_decode(token) and self.verify_token_signature:
            if self.auto_error:
                raise UNAUTHORIZED_TOKEN_NOT_VERIFYED
            else:
                return False
        
        if not await self.__verify_token_id(token) and self.verify_token_id:
            if self.auto_error:
                raise UNAUTHORIZED_NO_SUCH_TOKEN_ID
            else:
                return False
        
        return True


    async def __get_user_permissions(
        self,
        service: Annotated[UserService, Depends(user_service)],
        token: str
    ) -> list[BaseModel]:
        if not token or not self.auth_permissions.required_permissions:
            return list()
        user_id = jwt_token_decode(token).get('user_id')
        user_permissions = await service.find_user_permissions_by_id(user_id)
        return user_permissions
    

    async def __get_user_roles(
        self,
        service: Annotated[UserRoleService, Depends(user_role_service)],
        token: str
    ) -> list[BaseModel] | None:
        if not token or not self.auth_permissions.required_roles:
            return list()
        user_id = jwt_token_decode(token).get('user_id')
        user_roles = await service.find_user_role_by_id(user_id)
        return user_roles
    

    async def __get_user_groups(
        self,
        service: Annotated[UserGroupService, Depends(user_group_service)],
        token: str
    ) -> list[BaseModel] | None:
        if not token or not self.auth_permissions.required_groups:
            return list()
        user_id = jwt_token_decode(token).get('user_id')
        user_groups = await service.find_user_group_by_id(user_id)
        return user_groups
    

    def __get_user_id(self, token: str):
        if not token:
            return None
        decoded_token = jwt_token_decode(token)
        if not decoded_token:
            return None
        return decoded_token.get('user_id')
    
    
    async def __get_auth_request(self, token: str, request: Request) -> AuthRequest:

        is_authinticated = await self.__is_authinticated(token)

        auth_request = AuthRequest(request)
        auth_request.set_is_authinticated(is_authinticated)
        auth_request.set_token(token)

        if is_authinticated:

            user_id = self.__get_user_id(token)

            user_permissions = await self.__get_user_permissions(token)
            
            user_roles = await self.__get_user_roles(token)

            user_groups = await self.__get_user_groups(token)

            auth_request.set_user_id(user_id)
            auth_request.update_context(
                {
                    'user_permissions': [permission._asdict().get('codename') for permission in user_permissions],
                    'user_roles': [role._asdict().get('name') for role in user_roles],
                    'user_groups': [group._asdict().get('name') for group in user_groups]
                }
            )

        return auth_request

    
    async def find_require(
            self,
            auth_request: AuthRequest,
            list_requires: list,
            require_dict: str
    ) -> bool | HTTPException:
        
        for require in list_requires:
            if isinstance(require, str):
                if require not in auth_request.context.get(require_dict, list()):
                    if self.auto_error:
                        raise UNAUTHORIZED_NOT_PERMITED
                    return False

            elif issubclass(require, BasePermission):
                if not await require.has_permission(auth_request, async_session, self.auto_error):
                    return False
        return True


    async def check_permissions(self, auth_request: AuthRequest) -> bool | HTTPException:
        user_permisions: bool = await self.find_require(
            auth_request,
            self.auth_permissions.required_permissions,
            'user_permissions'
        )
        user_roles: bool = await self.find_require(
            auth_request,
            self.auth_permissions.required_roles,
            'user_roles'
        )
        user_groups: bool = await self.find_require(
            auth_request,
            self.auth_permissions.required_groups,
            'user_groups'
        )

        return user_permisions and user_roles and user_groups


    async def __call__(
        self,
        request: Request
    ) -> AuthRequest | HTTPException:
        
        if self.search_mode == SearchMode.COOKIE_MODE:
            auth_token = self.token_type(**request.cookies)
        if self.search_mode == SearchMode.HEADER_MODE:
            auth_token = self.token_type(**request.headers)

        token = self.__get_token(auth_token)
        print(f'call_token: {token}')

        auth_request = await self.__get_auth_request(token, request)
        print(f'call_auth_request: {auth_request}')

        permissions = await self.check_permissions(auth_request)
        auth_request.update_context({'has_permissions': permissions})

        return auth_request

