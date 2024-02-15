from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.group_permission import AddGroupPermissionSchema, UpdateGroupPermissionSchema, GroupPermissionSchema
from services.group_permission import GroupPermissionService
from dependencies import group_permission_service


group_permission_routers = APIRouter()


@group_permission_routers.post('/add-group-permission')
async def add_one(
    item: AddGroupPermissionSchema,
    service: Annotated[GroupPermissionService, Depends(group_permission_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@group_permission_routers.post('/add-group-permissions')
async def add_many(
    items: list[AddGroupPermissionSchema],
    service: Annotated[GroupPermissionService, Depends(group_permission_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@group_permission_routers.get('/get-group-permissions')
async def get(
    id: int,
    service: Annotated[GroupPermissionService, Depends(group_permission_service)]
):
    result = await service.find_group_permissions_by_id(id)
    return result


@group_permission_routers.get('/get-groups-permissions')
async def get_all(
    service: Annotated[GroupPermissionService, Depends(group_permission_service)]
):
    result = await service.find_all()
    return result


@group_permission_routers.patch('/update-group-permission')
async def update(
    id: int,
    item: UpdateGroupPermissionSchema,
    service: Annotated[GroupPermissionService, Depends(group_permission_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@group_permission_routers.patch('/update-group-permissions')
async def update_all(
    items: list[GroupPermissionSchema],
    service: Annotated[GroupPermissionService, Depends(group_permission_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@group_permission_routers.delete('/delete-group-permission')
async def delete(
    id: int,
    service: Annotated[GroupPermissionService, Depends(group_permission_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}