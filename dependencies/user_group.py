from services import UserGroupService
from repositories import UserGroupRepository


def user_group_service():
    return UserGroupService(UserGroupRepository)
