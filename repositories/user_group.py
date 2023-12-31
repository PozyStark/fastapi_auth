from select import select
from repositories.sqlalchemy import SqlAlchemyRepository
from models import Group, User, UserGroup
from databases import async_session


class UserGroupRepository(SqlAlchemyRepository):

    model = UserGroup

    async def find_user_group_by_id(self, user_id: str) -> list:
        async with async_session() as session:
            stmt = select(Group).join(
                        UserGroup, UserGroup.user_id==user_id
                    ).where(
                        UserGroup.role_id==Group.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]
        
    async def find_user_group_by_name(self, username: str) -> list:
        async with async_session() as session:
            user_id = select(User.id).where(User.username==str(username))
            stmt = select(
                        Group
                    ).join(
                        UserGroup, 
                        UserGroup.user_id==(user_id)
                    ).where(
                        UserGroup.role_id==Group.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]