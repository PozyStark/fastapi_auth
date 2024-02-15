from services import RolePermissionService
from repositories import RolePermissionRepository

def role_permission_service():
    return RolePermissionService(RolePermissionRepository)
