from sqlalchemy import select
from repositories.sqlalchemy import SqlAlchemyRepository
from models import Permission, Role, RolePermission
from databases import async_session

class RolePermissionRepository(SqlAlchemyRepository):

    model = RolePermission

    async def find_role_permissions_by_id(self, role_id: int) -> list:
        async with async_session() as session:
            stmt = select(
                        Permission
                    ).join(
                        RolePermission, RolePermission.role_id==role_id
                    ).where(
                        RolePermission.permission_id==Permission.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]
        
    async def find_role_permissions_by_name(self, role_name: str) -> list:
        async with async_session() as session:
            role_id = select(Role.id).where(Role.name==str(role_name))
            stmt = select(
                        Permission
                    ).join(
                        RolePermission, 
                        RolePermission.role_id==(role_id)
                    ).where(
                        RolePermission.permission_id==Permission.id
                    )
            result = await session.execute(stmt)
            return [row for row in result.scalars()]