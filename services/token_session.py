from uuid import uuid4
from models import TokenSession
from interfaces import AbstractRepository
from schemas import AddTokenSessionSchema, TokenSessionSchema, UpdateTokenSessionSchema

class TokenSessionService:

    repository: AbstractRepository

    def __init__(self, repository: AbstractRepository):
        self.repository = repository()

    async def add_one(self, item: AddTokenSessionSchema) -> TokenSession | None:
        token_session = TokenSessionSchema(
            id=str(uuid4()),
            temp_id=str(uuid4()),
            **item.model_dump()
        )
        return await self.repository.add_one(token_session.model_dump())
    
    async def add_many(self, items: list[AddTokenSessionSchema]):
        item_list = list()
        for item in items:
            token_session = TokenSessionSchema(
                id=str(uuid4()),
                temp_id=str(uuid4()),
                **item.model_dump()
            )
            item_list.append(token_session.model_dump())
        return await self.repository.add_many(item_list)
    
    async def find_by_id(self, item_id: str) -> TokenSession | None:
        if not item_id:
            return None
        result = await self.repository.find_one_or_none(filters=[self.repository.model.id == item_id])
        return result
    
    async def find_all(self):
        result = await self.repository.find_all()
        return result
    
    async def update(self, item_id: str, item: UpdateTokenSessionSchema, exclude_none: bool = False) -> TokenSession:
        result = await self.repository.update_one(item.model_dump(exclude_none=exclude_none), [self.repository.model.id == item_id])
        return result
    
    async def close_all_sessions(self, user_id: str, item: UpdateTokenSessionSchema,  exclude_none: bool = False) -> TokenSession:
        result = await self.repository.update_many(item.model_dump(exclude_none=exclude_none), [self.repository.model.user_id == user_id])
        return result
    
    async def close_all_sessions_exclude_current(self, token_id: str,  user_id: str, item: UpdateTokenSessionSchema, exclude_none: bool = False):
        if not token_id or not user_id:
            return None
        result = await self.repository.update_many(
            item.model_dump(exclude_none=exclude_none),
            [self.repository.model.id != token_id, self.repository.model.user_id == user_id]
        )
        return result
    
    async def update_all(self, items: list[UpdateTokenSessionSchema]):
        result = await self.repository.update_all([item.model_dump() for item in items])
        return result
    
    async def delete_by_id(self, item_id: str):
        result = await self.repository.delete([self.repository.model.id==item_id])
        return result