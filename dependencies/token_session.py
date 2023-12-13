from services import TokenSessionService
from repositories import TokenSessionRepository


def token_session_service():
    return TokenSessionService(TokenSessionRepository)