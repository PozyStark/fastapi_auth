from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.user_permission import AddUserPermissionSchema, UpdateUserPermissionSchema, UserPermissionSchema
from services.user_permission import UserPermissionService
from dependencies import user_permission_service


user_permission_routers = APIRouter()


@user_permission_routers.post('/add-user-permission')
async def add_one(
    item: AddUserPermissionSchema,
    service: Annotated[UserPermissionService, Depends(user_permission_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@user_permission_routers.post('/add-user-permissions')
async def add_many(
    items: list[AddUserPermissionSchema],
    service: Annotated[UserPermissionService, Depends(user_permission_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@user_permission_routers.get('/get-user-permissions')
async def get(
    id: int,
    service: Annotated[UserPermissionService, Depends(user_permission_service)]
):
    result = await service.find_group_permissions_by_id(id)
    return result


@user_permission_routers.get('/get-users-permissions')
async def get_all(
    service: Annotated[UserPermissionService, Depends(user_permission_service)]
):
    result = await service.find_all()
    return result


@user_permission_routers.patch('/update-user-permission')
async def update(
    id: int,
    item: UpdateUserPermissionSchema,
    service: Annotated[UserPermissionService, Depends(user_permission_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@user_permission_routers.patch('/update-user-permissions')
async def update_all(
    items: list[UserPermissionSchema],
    service: Annotated[UserPermissionService, Depends(user_permission_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@user_permission_routers.delete('/delete-user-permission')
async def delete(
    id: int,
    service: Annotated[UserPermissionService, Depends(user_permission_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}
