from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.role import AddRoleSchema, UpdateRoleSchema, RoleSchema
from services.role import RoleService
from dependencies import role_service


role_routers = APIRouter()


@role_routers.post('/add-role')
async def add_one(
    item: AddRoleSchema,
    service: Annotated[RoleService, Depends(role_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@role_routers.post('/add-roles')
async def add_many(
    items: list[AddRoleSchema],
    service: Annotated[RoleService, Depends(role_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@role_routers.get('/get-role')
async def get(
    id: int,
    service: Annotated[RoleService, Depends(role_service)]
):
    result = await service.find_by_id(id)
    return result


@role_routers.get('/get-roles')
async def get_all(
    service: Annotated[RoleService, Depends(role_service)]
):
    result = await service.find_all()
    return result


@role_routers.patch('/update-role')
async def update(
    id: int,
    item: UpdateRoleSchema,
    service: Annotated[RoleService, Depends(role_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@role_routers.patch('/update-roles')
async def update_all(
    items: list[RoleSchema],
    service: Annotated[RoleService, Depends(role_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@role_routers.delete('/delete-role')
async def delete_role(
    id: int,
    service: Annotated[RoleService, Depends(role_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}
