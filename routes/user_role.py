from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.user_role import AddUserRoleSchema, UpdateUserRoleSchema, UserRoleSchema
from services.user_role import UserRoleService
from dependencies import user_role_service

user_role_routers = APIRouter()

@user_role_routers.post('/add-user-role')
async def add_one(
    item: AddUserRoleSchema,
    service: Annotated[UserRoleService, Depends(user_role_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@user_role_routers.post('/add-user-roles')
async def add_many(
    items: list[AddUserRoleSchema],
    service: Annotated[UserRoleService, Depends(user_role_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@user_role_routers.get('/get-user-roles')
async def get(
    id: str,
    service: Annotated[UserRoleService, Depends(user_role_service)]
):
    result = await service.find_user_role_by_id(id)
    return result


@user_role_routers.get('/get-users-roles')
async def get_all(
    service: Annotated[UserRoleService, Depends(user_role_service)]
):
    result = await service.find_all()
    return result


@user_role_routers.patch('/update-user-role')
async def update(
    id: int,
    item: UpdateUserRoleSchema,
    service: Annotated[UserRoleService, Depends(user_role_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@user_role_routers.patch('/update-user-roles')
async def update_all(
    items: list[AddUserRoleSchema],
    service: Annotated[UserRoleService, Depends(user_role_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@user_role_routers.delete('/delete-user-role')
async def delete(
    id: int,
    service: Annotated[UserRoleService, Depends(user_role_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}
