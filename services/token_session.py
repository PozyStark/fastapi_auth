from uuid import uuid4
from core.repository import AbstractRepository
from schemas import AddTokenSessionSchema, TokenSessionSchema, UpdateTokenSessionSchema

class TokenSessionService:

    repository: AbstractRepository

    def __init__(self, repository: AbstractRepository):
        self.repository = repository()

    async def add_one(self, item: AddTokenSessionSchema):
        item_dict = item.model_dump()
        item_dict.update({'id': str(uuid4())})
        return await self.repository.add_one(item_dict)
    
    async def add_many(self, items: list[AddTokenSessionSchema]):
        item_list = list()
        for item in items:
            item_dict = item.model_dump()
            item_dict.update({'id': str(uuid4())})
            item_list.append(item_dict)
        return await self.repository.add_many(item_list)
    
    async def find_by_id(self, item_id: str):
        result = await self.repository.find_one_or_none(filters=[self.repository.model.id == item_id])
        return result
    
    async def find_all(self):
        result = await self.repository.find_all()
        return result
    
    async def update(self, item_id: str, item: UpdateTokenSessionSchema):
        result = await self.repository.update(item.model_dump(), [self.repository.model.id == item_id])
        return result
    
    async def update_all(self, items: list[UpdateTokenSessionSchema]):
        result = await self.repository.update_all([item.model_dump() for item in items])
        return result
    
    async def delete_by_id(self, item_id: str):
        result = await self.repository.delete([self.repository.model.id==item_id])
        return result