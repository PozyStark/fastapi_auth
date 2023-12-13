
from enum import Enum
from fastapi import Depends, HTTPException, Request
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel
from dependencies import user_service, token_session_service, user_group_service, user_role_service
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINURES
from exceptions import UNAUTHORIZED_NOT_PERMITED, UNAUTHORIZED_TOKEN_NOT_VERIFYED, UNAUTHORIZED_NO_SUCH_TOKEN_ID
from schemas import AuthinticationScheme, AccessToken, RefreshToken
from schemas import AddTokenSessionSchema
from services import UserService, TokenSessionService, UserRoleService, UserPermissionService, UserGroupService
from utils import create_jwt_token, jwt_token_decode, jwt_headers, jwt_payload
from permissions import BasePermission
from core.request import AuthRequest

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
    
"""
    *Класс зависимость для проверки аутентификации пользователя
    *Для проверки доступов пользователя
"""
class BearerAuth:

    HEADER_MODE: int = SearchMode.HEADER_MODE
    COOKIE_MODE: int = SearchMode.COOKIE_MODE

    token_type: AccessToken | RefreshToken
    search_mode: SearchMode
    verify_token_signature: bool
    verify_token_id: bool
    required_permission: list[BasePermission | str]
    required_roles: list[BasePermission | str]
    required_groups: list[BasePermission | str]

    def __init__(
        self,
        token_type: AccessToken | RefreshToken,
        verify_token_signature: bool = True,
        verify_token_id: bool = True,
        search_mode: SearchMode = COOKIE_MODE,
        auto_error: bool = True,
        required_permission: list[BasePermission | str] = None,
        required_roles: list[BasePermission | str] = None,
        required_groups: list[BasePermission | str] = None
    ):
        self.token_type = token_type
        self.auto_error = auto_error
        self.search_mode = search_mode
        self.verify_token_signature = verify_token_signature
        self.verify_token_id = verify_token_id
        self.required_permission = required_permission
        self.required_roles = required_roles
        self.required_groups = required_groups

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
            self.required_permission,
            'user_permissions'
        )
        user_roles: bool = await self.find_require(
            auth_request,
            self.required_roles,
            'user_roles'
        )
        user_groups: bool = await self.find_require(
            auth_request,
            self.required_groups,
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


