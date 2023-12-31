from select import select
from repositories.sqlalchemy import SqlAlchemyRepository
from models import User, UserPermission, Permission
from databases import async_session


class UserPermissionRepository(SqlAlchemyRepository):

    model = UserPermission

    async def find_user_permissions_by_id(self, user_id: str) -> list:
        async with async_session() as session:
            stmt = select(Permission).join(
                        UserPermission, UserPermission.user_id==user_id
                    ).where(
                        UserPermission.permission_id==Permission.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]
        
    async def find_user_permissions_by_name(self, username: str) -> list:
        async with async_session() as session:
            user_id = select(User.id).where(User.username==str(username))
            stmt = select(
                        Permission
                    ).join(
                        UserPermission, 
                        UserPermission.user_id==(user_id)
                    ).where(
                        UserPermission.permission_id==Permission.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]