from typing import Any
from sqlalchemy import delete, insert, select, update
from core.repository import AbstractRepository
from databases import async_session
from models import Role, Group, Permission, User, UserGroup, UserRole, UserPermission, RolePermission, GroupPermission, TokenSession


class SqlAlchemyRepository(AbstractRepository):

    model = None

    async def add_one(self, data: dict) -> Any:
        async with async_session() as session:
            stmt = insert(self.model).values(data).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()
            await session.close()
            return result.scalar_one_or_none()

    async def add_many(self, data: list[dict]) -> list[Any]:
        async with async_session() as session:
            stmt = insert(self.model).values(data).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()
            await session.close()
            return [row for row in result.scalars()]

    async def find_one_or_none(self, filters: list = []) -> Any | None:
        async with async_session() as session:
            stmt = select(self.model)
            for filter in filters:
                stmt = stmt.where(filter)
            result = await session.execute(stmt)
            await session.close()
            return result.scalar_one_or_none()

    async def find_all(self, filters: list = []) -> list[Any]:
        async with async_session() as session:
            stmt = select(self.model)
            for filter in filters:
                stmt = stmt.where(filter)
            result = await session.execute(stmt)
            return [raw for raw in result.scalars()]

    async def update(self, update_data: dict, filters: list = []) -> Any | None:
        async with async_session() as session:
            stmt = update(self.model).values(update_data).returning(self.model)
            for filter in filters:
                stmt = stmt.where(filter)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

    async def update_all(self, data: list[dict]) -> list[Any]:
        async with async_session() as session:
            result_list = list()
            for value in data:
                stmt = update(self.model).values(value).where(
                    self.model.id == value.get('id')
                ).returning(self.model)
                result = await session.execute(stmt)
                result_value = result.scalar_one()
                result_list.append(result_value)
            await session.commit()
            return result_list

    async def delete(self, filters: list = []) -> int:
        stmt = delete(self.model)
        for filter in filters:
            stmt = stmt.where(filter)
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount