
from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.role_permission import AddRolePermissionSchema, UpdateRolePermissionSchema, RolePermissionSchema
from services.role_permission import RolePermissionService
from dependencies import role_permission_service


role_permission_routers = APIRouter()


@role_permission_routers.post('/add-role-permission')
async def add_one(
    item: AddRolePermissionSchema,
    service: Annotated[RolePermissionService, Depends(role_permission_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@role_permission_routers.post('/add-role-permissions')
async def add_many(
    items: list[AddRolePermissionSchema],
    service: Annotated[RolePermissionService, Depends(role_permission_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@role_permission_routers.get('/get-role-permissions')
async def get(
    id: int,
    service: Annotated[RolePermissionService, Depends(role_permission_service)]
):
    result = await service.find_role_permissions_by_id(id)
    return result


@role_permission_routers.get('/get-roles-permissions')
async def get_all(
    service: Annotated[RolePermissionService, Depends(role_permission_service)]
):
    result = await service.find_all()
    return result


@role_permission_routers.patch('/update-role-permission')
async def update(
    id: int,
    item: UpdateRolePermissionSchema,
    service: Annotated[RolePermissionService, Depends(role_permission_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@role_permission_routers.patch('/update-role-permissions')
async def update_all(
    items: list[RolePermissionSchema],
    service: Annotated[RolePermissionService, Depends(role_permission_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@role_permission_routers.delete('/delete-role-permission')
async def delete(
    id: int,
    service: Annotated[RolePermissionService, Depends(role_permission_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}
