from sqlalchemy import select, union, union_all
from models import GroupPermission, Permission, RolePermission, User, UserGroup, UserPermission, UserRole
from databases import async_session
from core.sqlalchemy_repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):

    model = User

    async def find_by_username(self, username: str) -> User | None:
        result = await self.find_one_or_none(filters=[User.username==username])
        return result
    
    async def find_user_permissions_by_id(self, user_id: str) -> list:
        async with async_session.begin() as session:
            user_permission_query = select(
                Permission,
                UserPermission.permission_id
            ).where(
                UserPermission.user_id==user_id
            ).join(
                Permission,
                Permission.id==UserPermission.permission_id
            )

            role_permission_query = select(
                Permission,
                UserRole.role_id
            ).where(
                UserRole.user_id==user_id
            ).join(
                RolePermission,
                RolePermission.role_id==UserRole.role_id
            ).join(
                Permission,
                Permission.id==RolePermission.permission_id
            )

            group_permission_query = select(
                Permission,
                UserGroup.group_id
            ).where(
                UserGroup.user_id==user_id
            ).join(
                GroupPermission,
                GroupPermission.group_id==UserGroup.group_id,
            ).join(
                Permission,
                Permission.id==GroupPermission.permission_id
            )

            user_permissions = await session.execute(user_permission_query)
            role_permissions = await session.execute(role_permission_query)
            group_permissions = await session.execute(group_permission_query)

            user_permissions_list = [row for row in user_permissions.scalars()]
            role_permissions_list = [row for row in role_permissions.scalars()]
            group_permissions_list = [row for row in group_permissions.scalars()]

            return set(user_permissions_list+role_permissions_list+group_permissions_list)

