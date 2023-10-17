from sqlalchemy import select, union
from models import GroupPermission, Permission, RolePermission, User, UserGroup, UserPermission, UserRole
from databases import async_session
from core.sqlalchemy_repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def find_user_permissions_by_id(user_id: str):
        async with async_session.begin() as session:
            user_permission_query = select(
                UserPermission.perrmission_id,
                Permission.id,
                Permission.codename
            ).where(
                UserPermission.user_id==user_id
            ).join(
                Permission,
                Permission.id==UserPermission.perrmission_id
            )

            role_permission_query = select(
                UserRole.role_id,
                Permission.id,
                Permission.codename
            ).where(
                UserRole.user_id==user_id
            ).join(
                RolePermission,
                RolePermission.role_id==UserRole.role_id
            ).join(
                Permission,
                Permission.id==RolePermission.perrmission_id
            )

            group_permission_query = select(
                UserGroup.group_id,
                Permission.id,
                Permission.codename,
            ).where(
                UserGroup.user_id==user_id
            ).join(
                GroupPermission,
                GroupPermission.group_id==UserGroup.group_id,
            ).join(
                Permission,
                Permission.id==GroupPermission.perrmission_id
            )
            
            permissions_union = union(
                user_permission_query,
                role_permission_query,
                group_permission_query
            ).order_by(Permission.id)

            all_permissions_query = select(
                Permission.id,
                Permission.codename
            ).from_statement(permissions_union)

            permissions = await session.execute(all_permissions_query)
            return [row for row in permissions.scalars()]

