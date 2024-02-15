from sqlalchemy import select
from repositories.sqlalchemy import SqlAlchemyRepository
from models import Group, GroupPermission, Permission, Role, RolePermission
from databases import async_session

class GroupPermissionRepository(SqlAlchemyRepository):

    model = GroupPermission

    async def find_group_permissions_by_id(self, group_id: int) -> list:
        async with async_session() as session:
            stmt = select(
                        Permission
                    ).join(
                        GroupPermission, GroupPermission.group_id==group_id
                    ).where(
                        GroupPermission.permission_id==Permission.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]
        
    async def find_group_permissions_by_name(self, group_name: str) -> list:
        async with async_session() as session:
            group_id = select(Group.id).where(Group.name==group_name)
            stmt = select(
                        Permission
                    ).join(
                        GroupPermission, 
                        GroupPermission.group_id==(group_id)
                    ).where(
                        GroupPermission.permission_id==Permission.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]