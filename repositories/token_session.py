from core.sqlalchemy_repository import SqlAlchemyRepository
from models import TokenSession


class TokenSessionRepository(SqlAlchemyRepository):
    model = TokenSession