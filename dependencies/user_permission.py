from services import UserPermissionService
from repositories import UserPermissionRepository


def user_permission_service():
    return UserPermissionService(UserPermissionRepository)
