from models import Group
from core.sqlalchemy_repository import SqlAlchemyRepository


class GroupRepository(SqlAlchemyRepository):
    model = Group
