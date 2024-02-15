from services import PermissionService
from repositories import PermissionRepository

def permission_service():
    return PermissionService(PermissionRepository)
