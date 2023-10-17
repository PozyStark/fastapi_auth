from abc import ABC, abstractmethod

from fastapi import HTTPException
from core.permission import BasePermission
from exceptions import UNAUTHORIZED_NOT_PERMITED
from core.request import AuthRequest
# from services import get_token_id, get_user_by_id
# from utils import jwt_headers
from sqlalchemy.ext.asyncio import AsyncSession


class AllowAny(BasePermission):

    async def has_permission(
        auth_request: AuthRequest,
        async_session: AsyncSession,
        auto_error: bool = True
    ) -> bool | HTTPException:
        return True
    

# class IsAuthenticated(BasePermission):
   
#     async def has_permission(
#         auth_request: AuthRequest,
#         async_session: AsyncSession,
#         auto_error: bool = True
#     ) -> bool | HTTPException:
#         if not auth_request.is_authinticated:
#             if auto_error:
#                 raise UNAUTHORIZED_NOT_PERMITED
#             return False
#         return True
        

# class IsAdminUser(BasePermission):

#     async def has_permission(
#         auth_request: AuthRequest,
#         async_session: AsyncSession,
#         auto_error: bool = True
#     ) ->  bool | HTTPException:
                
#         if not auth_request.is_authinticated:
#             if auto_error:
#                 raise UNAUTHORIZED_NOT_PERMITED
#             return False
        
#         user_roles = auth_request.context.get('user_roles')

#         if 'admin' not in user_roles:
#             if auto_error:
#                 raise UNAUTHORIZED_NOT_PERMITED
#             return False
        
#         return True


# class IsSuperUser(BasePermission):

#     async def has_permission(
#         auth_request: AuthRequest,
#         async_session: AsyncSession,
#         auto_error: bool = True
#     ) -> bool | HTTPException:
        
#         if not auth_request.is_authinticated:
#             if auto_error:
#                 raise UNAUTHORIZED_NOT_PERMITED
#             return False
        
#         user_id = auth_request.context.get('user_id')
#         user = await get_user_by_id(async_session, user_id)

#         if not user.is_superuser:
#             if auto_error:
#                 raise UNAUTHORIZED_NOT_PERMITED
#             return False
        
#         return True
 

# class IsActive(BasePermission):

#     async def has_permission(
#         auth_request: AuthRequest,
#         async_session: AsyncSession,
#         auto_error: bool = True
#     ) -> bool | HTTPException:
    
#         if not auth_request.is_authinticated:
#             if auto_error:
#                 raise UNAUTHORIZED_NOT_PERMITED
#             return False
        
#         user_id = auth_request.context.get('user_id')
#         user = await get_user_by_id(async_session, user_id)

#         if not user.is_active:
#             if auto_error:
#                 raise HTTPException(403, 'User is not active')
#             return False
        
#         return True
