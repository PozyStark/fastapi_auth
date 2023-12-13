from services import UserRoleService
from repositories import UserRoleRepository


def user_role_service():
    return UserRoleService(UserRoleRepository)
