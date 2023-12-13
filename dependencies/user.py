from services import UserService
from repositories import UserRepository


def user_service():
    return UserService(UserRepository)
