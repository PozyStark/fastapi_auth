from services import GroupService
from repositories import GroupRepository

def group_service():
    return GroupService(GroupRepository)