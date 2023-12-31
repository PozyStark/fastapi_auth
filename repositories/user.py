from sqlalchemy import select, union, union_all
from models import GroupPermission, Permission, RolePermission, User, UserGroup, UserPermission, UserRole, Role, Group
from databases import async_session
from repositories.sqlalchemy import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):

    model = User

    async def find_by_username(self, username: str) -> User | None:
        result = await self.find_one_or_none(filters=[User.username==username])
        return result
    
    async def find_user_roles(self, user_id: str) -> list[Role]:
        async with async_session.begin() as session:
            user_role_query = select(
                Role,
                UserRole.role_id
            ).where(
                UserRole.user_id==user_id
            ).join(
                Role,
                Role.id==UserRole.role_id
            )

            user_role_result = await session.execute(user_role_query)

            return [raw.name for raw in user_role_result.scalars()]
        
    async def find_user_groups(self, user_id: str) -> list[Group]:
        async with async_session.begin() as session:
            user_group_query = select(
                Group,
                UserGroup.group_id
            ).where(
                UserGroup.user_id==user_id
            ).join(
                Group,
                Group.id==UserGroup.group_id
            )

            user_group_result = await session.execute(user_group_query)
            
            return [raw.name for raw in user_group_result.scalars()]

    async def find_user_permissions_by_id(self, user_id: str) -> list[Permission]:
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

            user_permissions_list = [row.codename for row in user_permissions.scalars()]
            role_permissions_list = [row.codename for row in role_permissions.scalars()]
            group_permissions_list = [row.codename for row in group_permissions.scalars()]

            return list(set(user_permissions_list+role_permissions_list+group_permissions_list))

