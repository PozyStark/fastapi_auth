from models import Role
from core.sqlalchemy_repository import SqlAlchemyRepository


class RoleRepository(SqlAlchemyRepository):
    model = Role
