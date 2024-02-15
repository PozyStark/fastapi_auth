from models import Role
from repositories.sqlalchemy import SqlAlchemyRepository


class RoleRepository(SqlAlchemyRepository):
    model = Role
