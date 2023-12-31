from repositories.sqlalchemy import SqlAlchemyRepository
from models import TokenSession


class TokenSessionRepository(SqlAlchemyRepository):
    model = TokenSession