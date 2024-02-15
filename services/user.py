from uuid import uuid4
from interfaces import AbstractRepository
from repositories.user import User
from schemas.user import AddUserSchema, UpdateUserSchema, UserWithPasswordSchema


class UserService:

    repository: AbstractRepository

    def __init__(self, repository: AbstractRepository):
        self.repository = repository()

    async def add_one(self, item: AddUserSchema, uuid = uuid4()):
        user_model = UserWithPasswordSchema(
            id=str(uuid4()),
            **item.model_dump()
        )
        return await self.repository.add_one(user_model.model_dump())
    
    async def add_many(self, items: list[AddUserSchema]):
        item_list = list()
        for item in items:
            item_dict = UserWithPasswordSchema(
                id=str(uuid4()),
                **item.model_dump()
            )
            item_list.append(item_dict.model_dump())
        return await self.repository.add_many(item_list)
    
    async def find_by_id(self, item_id: str) -> User | None:
        if not item_id:
            return None
        result = await self.repository.find_one_or_none(filters=[self.repository.model.id == item_id])
        return result
    
    async def find_by_username(self, username: str) -> User | None:
        result = await self.repository.find_by_username(username)
        return result
    
    async def find_all(self):
        result = await self.repository.find_all()
        return result
    
    async def find_user_permissions_by_id(self, user_id: str) -> list[str]:
        if not user_id:
            return list()
        result = await self.repository.find_user_permissions_by_id(user_id)
        return result
    
    async def find_user_roles_by_id(self, user_id: str) -> list[str]:
        if not user_id:
            return list()
        result = await self.repository.find_user_roles(user_id)
        return result
    
    async def find_user_groups_by_id(self, user_id: str) -> list[str]:
        if not user_id:
            return list()
        result = await self.repository.find_user_groups(user_id)
        return result
    
    async def update(self, item_id: str, item: UpdateUserSchema, exclude_none: bool = False):
        update_item = item.model_dump(exclude_none=exclude_none)
        result = await self.repository.update_one(update_item, [self.repository.model.id == item_id])
        return result
    
    async def update_all(self, items: list[UpdateUserSchema], exclude_none: bool = False):
        item_list = list()
        for item in items:
            item_dict = item.model_dump(exclude_none=exclude_none)
            item_list.append(item_dict)
        result = await self.repository.update_all(item_list)
        return result
    
    async def delete_by_id(self, item_id: str):
        result = await self.repository.delete([self.repository.model.id==item_id])
        return result