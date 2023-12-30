from fastapi import APIRouter, Response
from fastapi import Depends
from typing import Annotated

from dependencies import auth_token_pair

from exceptions import UNAUTHORIZED_NO_SUCH_USER

from dependencies import AuthRequest
from dependencies import BearerAuth
from core import IsAuthenticated, IsSuperUser, BasePermission, StrPermission, StrRole, StrGroup
from utils import jwt_token_decode

auth_routers = APIRouter()


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


@auth_routers.post('/token')
async def token(
    response: Response,
    auth_token_pair: Annotated[dict, Depends(auth_token_pair)]
):
        access_token = auth_token_pair.get('access_token')
        refresh_token = auth_token_pair.get('refresh_token')
        
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
        return {'access_token': access_token, 'refresh_token': refresh_token}


@auth_routers.get('/token-verify')
def token_verify(
    auth_request: Annotated[
        AuthRequest,
        Depends(
            BearerAuth(
                token_type=BearerAuth.ACCESS_TOKEN,
                search_mode=BearerAuth.COOKIE_MODE,
                auto_error=False
            )
        )
    ]
):
    if jwt_token_decode(jwt_token=auth_request.token, auto_error=False):
        return {'verify': True}
    return {'verify': False}


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

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest,
        Depends(
            BearerAuth(
                token_type=BearerAuth.ACCESS_TOKEN,
                search_mode=BearerAuth.COOKIE_MODE,
                auto_error=True,
                required_permissions=[
                    # IsAuthenticated,
                    # IsSuperUser,
                    StrPermission(required_permission='perm_2'),
                    StrRole(required_role='string_role_2'),
                    StrGroup(required_group='string_group_3')
                ]
            )
        )
    ]
):
    return {
        'token': auth_request.token,
        'token_id': auth_request.token_id,
        'user_id': auth_request.user_id,
        'is_authinticated': auth_request.is_authinticated,
        'is_superuser': auth_request.is_superuser,
        'user_permissions': auth_request.user_permissions,
        'user_roles': auth_request.user_roles,
        'user_groups': auth_request.user_groups
    }


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