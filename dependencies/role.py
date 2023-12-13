from services import RoleService
from repositories import RoleRepository

def role_service():
    return RoleService(RoleRepository)