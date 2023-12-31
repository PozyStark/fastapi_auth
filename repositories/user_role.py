from select import select
from repositories.sqlalchemy import SqlAlchemyRepository
from models import Role, User, UserPermission, Permission, UserRole
from databases import async_session


class UserRoleRepository(SqlAlchemyRepository):

    model = UserRole

    async def find_user_role_by_id(self, user_id: str) -> list:
        async with async_session() as session:
            stmt = select(Role).join(
                        UserRole, UserRole.user_id==user_id
                    ).where(
                        UserRole.role_id==Role.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]
        
    async def find_user_role_by_name(self, username: str) -> list:
        async with async_session() as session:
            user_id = select(User.id).where(User.username==str(username))
            stmt = select(
                        Role
                    ).join(
                        UserRole, 
                        UserRole.user_id==(user_id)
                    ).where(
                        UserRole.role_id==Role.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]