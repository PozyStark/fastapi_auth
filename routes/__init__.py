from fastapi import APIRouter
from .auth import auth_routers
from .user import user_routers
from .user_role import user_role_routers
from .user_permission import user_permission_routers
from .user_group import user_group_routers
from .token_session import token_session_routers
from .role import role_routers
from .role_permission import role_permission_routers
from .permission import permission_routers
from .group import group_routers
from .group_permission import group_permission_routers


fastapi_auth_routes = APIRouter()

fastapi_auth_routes.include_router(auth_routers)

"""
Роуты для работы с админ панелью (в процессе создания)
"""
fastapi_auth_routes.include_router(user_routers)
fastapi_auth_routes.include_router(user_role_routers)
fastapi_auth_routes.include_router(user_permission_routers)
fastapi_auth_routes.include_router(user_group_routers)
fastapi_auth_routes.include_router(role_routers)
fastapi_auth_routes.include_router(role_permission_routers)
fastapi_auth_routes.include_router(permission_routers)
fastapi_auth_routes.include_router(group_routers)
fastapi_auth_routes.include_router(group_permission_routers)
fastapi_auth_routes.include_router(token_session_routers)