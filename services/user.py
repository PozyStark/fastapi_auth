from uuid import uuid4
from datetime import datetime
from core.repository import AbstractRepository
from repositories.user import User
from schemas.user import AddUserSchema, UserSchema, UpdateUserSchema


class UserService:

    repository: AbstractRepository

    def __init__(self, repository: AbstractRepository):
        self.repository = repository()

    async def add_one(self, item: AddUserSchema):
        item_dict = item.model_dump()
        item_dict.update(
            {
                'id': str(uuid4()),
                'created_at': datetime.utcnow(),
                'last_updated': datetime.utcnow(),
                'last_login': datetime.utcnow()
            }
        )
        return await self.repository.add_one(item_dict)
    
    async def add_many(self, items: list[AddUserSchema]):
        item_list = list()
        for item in items:
            item_dict = item.model_dump()
            item_dict.update(
                {
                    'id': str(uuid4()),
                    'created_at': datetime.utcnow(),
                    'last_updated': datetime.utcnow(),
                    'last_login': datetime.utcnow()
                }
            )
            item_list.append(item_dict)
        return await self.repository.add_many(item_list)
    
    async def find_by_id(self, item_id: int):
        result = await self.repository.find_one_or_none(filters=[self.repository.model.id == item_id])
        return result
    
    async def find_by_username(self, username: str) -> User | None:
        result = await self.repository.find_by_username(username)
        return result
    
    async def find_all(self):
        result = await self.repository.find_all()
        return result
    
    async def find_user_permissions_by_id(self, user_id: str):
        result = await self.repository.find_user_permissions_by_id(user_id)
        return result
    
    async def update(self, item_id: str, item: UpdateUserSchema):
        update_item = item.model_dump()
        update_item.update({"last_updated": datetime.utcnow()})
        result = await self.repository.update(update_item, [self.repository.model.id == item_id])
        return result
    
    async def update_all(self, items: list[UserSchema]):
        item_list = list()
        for item in items:
            item_dict = item.model_dump()
            item_dict.update({'last_updated': datetime.utcnow()})
            item_list.append(item_dict)
        result = await self.repository.update_all(item_list)
        return result
    
    async def delete_by_id(self, item_id: int):
        result = await self.repository.delete([self.repository.model.id==item_id])
        return result