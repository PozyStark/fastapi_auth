from interfaces import AbstractRepository
from schemas import AddUserGroupSchema, UpdateUserGroupSchema, UserGroupSchema


class UserGroupService:

    repository: AbstractRepository

    def __init__(self, repository: AbstractRepository):
        self.repository = repository()

    async def find_user_group_by_id(self, user_id: str):
        result = await self.repository.find_user_group_by_name(user_id)
        return result
    
    async def find_user_group_by_name(self, username: str):
        result = await self.repository.find_user_group_by_name(username)
        return result

    async def add_one(self, item: AddUserGroupSchema):
        return await self.repository.add_one(item.model_dump())
    
    async def add_many(self, items: list[AddUserGroupSchema]):
        return await self.repository.add_many([item.model_dump() for item in items])

    async def find_by_id(self, item_id: int):
        result = await self.repository.find_one_or_none(filters=[self.repository.model.id == item_id])
        return result
    
    async def find_all(self):
        result = await self.repository.find_all()
        return result
    
    async def update(self, item_id: int, item: UpdateUserGroupSchema):
        result = await self.repository.update_one(item.model_dump(), [self.repository.model.id == item_id])
        return result
    
    async def update_all(self, items: list[UserGroupSchema]):
        result = await self.repository.update_all([item.model_dump() for item in items])
        return result
    
    async def delete_by_id(self, item_id: int):
        result = await self.repository.delete([self.repository.model.id==item_id])
        return result