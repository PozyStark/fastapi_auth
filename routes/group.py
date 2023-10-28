from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.group import AddGroupSchema, UpdateGroupSchema, GroupSchema
from services.group import GroupService
from dependencies import group_service


group_routers = APIRouter()


@group_routers.post('/add-group')
async def add_one(
    item: AddGroupSchema,
    service: Annotated[GroupService, Depends(group_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@group_routers.post('/add-groups')
async def add_many(
    items: list[AddGroupSchema],
    service: Annotated[GroupService, Depends(group_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@group_routers.get('/get-group')
async def get(
    id: int,
    service: Annotated[GroupService, Depends(group_service)]
):
    result = await service.find_by_id(id)
    return result


@group_routers.get('/get-groups')
async def get_all(
    service: Annotated[GroupService, Depends(group_service)]
):
    result = await service.find_all()
    return result


@group_routers.patch('/update-group')
async def update(
    id: int,
    item: UpdateGroupSchema,
    service: Annotated[GroupService, Depends(group_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@group_routers.patch('/update-groups')
async def update_all(
    items: list[GroupSchema],
    service: Annotated[GroupService, Depends(group_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@group_routers.delete('/delete-group')
async def delete(
    id: int,
    service: Annotated[GroupService, Depends(group_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}
