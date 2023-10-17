from repositories.group import GroupRepository
from repositories.group_permission import GroupPermissionRepository
from repositories.permission import PermissionRepository
from repositories.role import RoleRepository
from repositories.token_session import TokenSessionRepository
from repositories.user import UserRepository
from repositories.role_permission import RolePermissionRepository
from repositories.user_group import UserGroupRepository
from repositories.user_permission import UserPermissionRepository
from repositories.user_role import UserRoleRepository
from services.group import GroupService
from services.group_permission import GroupPermissionService
from services.permission import PermissionService
from services.role import RoleService
from services.token_session import TokenSessionService
from services.user import UserService
from services.role_permission import RolePermissionService
from services.user_group import UserGroupService
from services.user_permission import UserPermissionService
from services.user_role import UserRoleService


def role_service():
    return RoleService(RoleRepository)

def group_service():
    return GroupService(GroupRepository)

def permission_service():
    return PermissionService(PermissionRepository)

def user_service():
    return UserService(UserRepository)

def role_permission_service():
    return RolePermissionService(RolePermissionRepository)

def group_permission_service():
    return GroupPermissionService(GroupPermissionRepository)

def user_permission_service():
    return UserPermissionService(UserPermissionRepository)

def user_role_service():
    return UserRoleService(UserRoleRepository)

def user_group_service():
    return UserGroupService(UserGroupRepository)

def token_session_service():
    return TokenSessionService(TokenSessionRepository)