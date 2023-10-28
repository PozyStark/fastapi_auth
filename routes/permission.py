from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.permission import AddPermissionSchema, UpdatePermissionSchema, PermissionSchema
from services.permission import PermissionService
from dependencies import permission_service


permission_routers = APIRouter()


@permission_routers.post('/add-permission')
async def add_one(
    item: AddPermissionSchema,
    service: Annotated[PermissionService, Depends(permission_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@permission_routers.post('/add-permissions')
async def add_many(
    items: list[AddPermissionSchema],
    service: Annotated[PermissionService, Depends(permission_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@permission_routers.get('/get-permission')
async def get(
    id: int,
    service: Annotated[PermissionService, Depends(permission_service)]
):
    result = await service.find_by_id(id)
    return result


@permission_routers.get('/get-permissions')
async def get_all(
    service: Annotated[PermissionService, Depends(permission_service)]
):
    result = await service.find_all()
    return result


@permission_routers.patch('/update-permission')
async def update(
    id: int,
    item: UpdatePermissionSchema,
    service: Annotated[PermissionService, Depends(permission_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@permission_routers.patch('/update-permissions')
async def update_all(
    items: list[PermissionSchema],
    service: Annotated[PermissionService, Depends(permission_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@permission_routers.delete('/delete-permission')
async def delete(
    id: int,
    service: Annotated[PermissionService, Depends(permission_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}
