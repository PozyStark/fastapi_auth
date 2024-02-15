from models import Group
from repositories.sqlalchemy import SqlAlchemyRepository


class GroupRepository(SqlAlchemyRepository):
    model = Group
