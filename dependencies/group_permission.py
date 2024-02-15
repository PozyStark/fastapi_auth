from services import GroupPermissionService
from repositories import GroupPermissionRepository


def group_permission_service():
    return GroupPermissionService(GroupPermissionRepository)
