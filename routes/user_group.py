from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.user_group import AddUserGroupSchema, UpdateUserGroupSchema, UserGroupSchema
from services.user_group import UserGroupService
from dependencies import user_group_service


user_group_routers = APIRouter()


@user_group_routers.post('/add-user-group')
async def add_one(
    item: AddUserGroupSchema,
    service: Annotated[UserGroupService, Depends(user_group_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@user_group_routers.post('/add-user-groups')
async def add_many(
    items: list[AddUserGroupSchema],
    service: Annotated[UserGroupService, Depends(user_group_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@user_group_routers.get('/get-user-groups')
async def get(
    id: int,
    service: Annotated[UserGroupService, Depends(user_group_service)]
):
    result = await service.find_group_permissions_by_id(id)
    return result


@user_group_routers.get('/get-users-groups')
async def get_all(
    service: Annotated[UserGroupService, Depends(user_group_service)]
):
    result = await service.find_all()
    return result


@user_group_routers.patch('/update-user-group')
async def update(
    id: int,
    item: UpdateUserGroupSchema,
    service: Annotated[UserGroupService, Depends(user_group_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@user_group_routers.patch('/update-user-groups')
async def update_all(
    items: list[UserGroupSchema],
    service: Annotated[UserGroupService, Depends(user_group_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@user_group_routers.delete('/delete-user-group')
async def delete(
    id: int,
    service: Annotated[UserGroupService, Depends(user_group_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}
