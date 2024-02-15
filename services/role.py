from interfaces import AbstractRepository
from repositories import RoleRepository
from schemas import AddRoleSchema, RoleSchema, UpdateRoleSchema


class RoleService:

    repository: AbstractRepository

    def __init__(self, repository: AbstractRepository):
        self.repository = repository()

    async def add_one(self, item: AddRoleSchema):
        return await self.repository.add_one(item.model_dump())
    
    async def add_many(self, items: list[AddRoleSchema]):
        return await self.repository.add_many([item.model_dump() for item in items])
    
    async def find_by_id(self, item_id: int):
        result = await self.repository.find_one_or_none(filters=[self.repository.model.id == item_id])
        return result
    
    async def find_all(self):
        result = await self.repository.find_all()
        return result
    
    async def update(self, item_id: int, item: UpdateRoleSchema):
        result = await self.repository.update_one(item.model_dump(), [self.repository.model.id == item_id])
        return result
    
    async def update_all(self, items: list[RoleSchema]):
        result = await self.repository.update_all([item.model_dump() for item in items])
        return result
    
    async def delete_by_id(self, item_id: int):
        result = await self.repository.delete([self.repository.model.id==item_id])
        return result