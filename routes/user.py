from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.user import AddUserSchema, UserSchema, UpdateUserSchema
from services.user import UserService
from dependencies import user_service


user_routers = APIRouter()


@user_routers.post('/add-user')
async def add_one(
    item: AddUserSchema,
    service: Annotated[UserService, Depends(user_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@user_routers.post('/add-users')
async def add_many(
    items: list[AddUserSchema],
    service: Annotated[UserService, Depends(user_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@user_routers.get('/get-user')
async def get(
    id: str,
    service: Annotated[UserService, Depends(user_service)]
):
    result = await service.find_by_id(id)
    return result


@user_routers.get('/get-users')
async def get_all(
    service: Annotated[UserService, Depends(user_service)]
):
    result = await service.find_all()
    return result


@user_routers.patch('/update-user')
async def update(
    id: str,
    item: UpdateUserSchema,
    service: Annotated[UserService, Depends(user_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@user_routers.patch('/update-users')
async def update_all(
    items: list[UserSchema],
    service: Annotated[UserService, Depends(user_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@user_routers.delete('/delete-user')
async def delete(
    id: str,
    service: Annotated[UserService, Depends(user_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}


