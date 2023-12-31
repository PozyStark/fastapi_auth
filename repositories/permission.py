from models import Permission
from repositories.sqlalchemy import SqlAlchemyRepository


class PermissionRepository(SqlAlchemyRepository):
    model = Permission
