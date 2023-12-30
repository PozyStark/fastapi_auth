from datetime import datetime, timedelta
import time
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from uuid import uuid4
from fastapi import Depends, Response
from fastapi.routing import APIRouter
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import group_permission_service, group_service, role_permission_service, role_service, permission_service, user_group_service, user_permission_service, user_role_service, user_service
from exceptions import UNAUTHORIZED_NO_SUCH_USER
from models import Permission, Role, RolePermission
# from permissions import AllowAny, IsAdminUser, IsAuthenticated, IsSuperUser
from schemas.group import AddGroupSchema, GroupSchema, UpdateGroupSchema
from schemas.group_permission import AddGroupPermissionSchema, GroupPermissionSchema, UpdateGroupPermissionSchema
from schemas.role_permission import AddRolePermissionSchema, RolePermissionSchema, UpdateRolePermissionSchema
from schemas.user import AddUserSchema, UserSchema, UpdateUserSchema
from schemas.user_permission import AddUserPermissionSchema, UserPermissionSchema
from schemas.user_role import AddUserRoleSchema, UserRoleSchema, UpdateUserRoleSchema
from schemas.user_group import UserGroupSchema, AddUserGroupSchema, UpdateUserGroupSchema
from services.group import GroupService
from services.group_permission import GroupPermissionService
from services.role import RoleService
from services.permission import PermissionService
# from utils import authinticate_user, get_hashed_password, jwt_headers, jwt_payload, create_jwt_token, jwt_token_decode
from schemas.role import AddRoleSchema, RoleSchema, UpdateRoleSchema
from schemas.permission import AddPermissionSchema, PermissionSchema, UpdatePermissionSchema
from databases import async_session
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINURES
from services.role_permission import RolePermissionService
from services.user import UserService
from services.user_permission import UserPermissionService
from services.user_role import UserRoleService
from services.user_group import UserGroupService
# from auth import BearerAuth
# from schemas.auth import AccessToken, RefreshToken

auth_routers = APIRouter()

# registration_permissions = AuthPermissions(
#     required_permissions=[AllowAny]
# )


# @auth_routers.post('/registartion')
# async def registration(
#     registration_scheme: RegistrationScheme,
#     auth_request: Annotated[
#         AuthRequest,
#         Depends(
#             BearerAuth(
#                 token_type=AccessToken,
#                 auth_permissions=registration_permissions
#             )
#         )
#     ]
# ):
#     # 1 Проверка на существование пользователя
#     # 2 Стоит добавлять функционал создания пользователя как админа или супер пользователя
#     # 3 Сразу задавать все необходимые роли и доступы?
#     #
#     return auth_request.is_authinticated


# @auth_routers.post('/token')
# async def token(
#     response: Response,
#     authintication_scheme: AuthinticationScheme
# ):
#     user = await authinticate_user(
#         async_session=async_session,
#         username=authintication_scheme.username,
#         password=authintication_scheme.password
#     )

#     if user:
#         token_id = str(uuid4())
#         headers = {
#             'token_id': token_id
#         }
#         payload = {
#             'user_id': str(user.id)
#         }

#         access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

#         refresh_expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINURES)

#         access_token = create_jwt_token(
#             expire=access_expire,
#             headers=headers,
#             payload=payload
#         )
#         refresh_token = create_jwt_token(
#             expire=refresh_expire,
#             headers=headers,
#             payload=payload
#         )
#         await add_token_id(
#             async_session=async_session,
#             token_id=token_id,
#             user_id=user.id,
#             expire=refresh_expire
#         )
#         response.set_cookie(
#             key='access_token',
#             value=access_token,
#             httponly=True
#         )
#         response.set_cookie(
#             key='refresh_token',
#             value=refresh_token,
#             httponly=True
#         )
#         return {'access_token': access_token, 'refresh_token': refresh_token}
#     raise UNAUTHORIZED_NO_SUCH_USER


# @auth_routers.get('/token-verify')
# def token_verify(
#     auth_request: Annotated[
#         AuthRequest,
#         Depends(
#             BearerAuth(
#                 token_type=AccessToken,
#                 verify_token_signature=False,
#                 search_mode=BearerAuth.HEADER_MODE,
#                 verify_token_id=False
#             )
#         )
#     ]
# ):
#     if jwt_token_decode(jwt_token=auth_request.token):
#         return {'verify': True}
#     return {'verify': False}


# refresh_permissions = AuthPermissions(
#     required_permissions=[
#         IsAuthenticated
#     ]
# )


# @auth_routers.post('/token-refresh')
# async def token_refresh(
#     response: Response,
#     auth_request: Annotated[
#         AuthRequest,
#         Depends(
#             BearerAuth(
#                 token_type=RefreshToken,
#                 search_mode=BearerAuth.HEADER_MODE,
#                 auth_permissions=refresh_permissions
#             )
#         )
#     ]
# ):
#     token_headers = jwt_headers(auth_request.token)
#     token_payload = jwt_payload(auth_request.token)
#     token_id = token_headers.get('token_id')
#     user_id = token_payload.get('user_id')

#     await delete_token_id(async_session, token_id)

#     token_id = str(uuid4())
#     access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     refresh_expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINURES)

#     headers = {
#         'token_id': token_id
#     }
#     payload = {
#         'user_id': str(user_id)
#     }

#     await add_token_id(async_session, token_id, user_id, refresh_expire)
#     access_token = create_jwt_token(
#         expire=access_expire,
#         headers=headers,
#         payload=payload
#     )
#     refresh_token = create_jwt_token(
#         expire=refresh_expire,
#         headers=headers,
#         payload=payload
#     )
#     response.set_cookie('access_token', access_token)
#     response.set_cookie('refresh_token', refresh_token)
#     return {'access_token': access_token, 'refresh_token': refresh_token}


# @auth_routers.post('/logout')
# async def logout(
#     response: Response,
#     auth_request: Annotated[
#         AuthRequest,
#         Depends(
#             BearerAuth(
#                 search_mode=BearerAuth.HEADER_MODE,
#                 token_type=RefreshToken,
#                 auto_error=False
#             )
#         )
#     ]
# ):
#     response.delete_cookie('refresh_token')
#     response.delete_cookie('access_token')

#     if auth_request.is_authinticated:
#         token_headers = jwt_headers(auth_request.token)
#         token_id = token_headers.get('token_id')
#         await delete_token_id(async_session, token_id)
#         return {'detail': 'Logout success'}

#     return {'detail': 'You not authinticated'}


# protected_url_permission = AuthPermissions(
#     required_permissions=[
#         AllowAny,
#         # IsAuthenticated,
#         # 'view_group'
#     ],
#     required_roles=[
#         # 'admin',
#         # 'moderator'
#     ]
# )


# @auth_routers.get('/protected-url')
# async def protected_url(
#     auth_request: Annotated[
#         AuthRequest,
#         Depends(
#             BearerAuth(
#                 token_type=AccessToken,
#                 search_mode=BearerAuth.HEADER_MODE,
#                 auto_error=True,
#                 auth_permissions=protected_url_permission
#             )
#         )
#     ]
# ):

#     return {
#         'token': auth_request.token,
#         'user_id': auth_request.user_id,
#         'auth_status': auth_request.is_authinticated,
#         'context': auth_request.context,
#         'has_permission': await BearerAuth.check_permission('view_group', auth_request)
#     }
