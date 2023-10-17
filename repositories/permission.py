from models import Permission
from core.sqlalchemy_repository import SqlAlchemyRepository


class PermissionRepository(SqlAlchemyRepository):
    model = Permission
