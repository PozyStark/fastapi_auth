from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from schemas.token_session import AddTokenSessionSchema, UpdateTokenSessionSchema, TokenSessionSchema
from services.token_session import TokenSessionService
from dependencies import token_session_service


token_session_routers = APIRouter()


@token_session_routers.post('/add-token-session')
async def add_one(
    item: AddTokenSessionSchema,
    service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    result = await service.add_one(item)
    return {'insert': result}


@token_session_routers.post('/add-token-sessions')
async def add_many(
    items: list[AddTokenSessionSchema],
    service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    result = await service.add_many(items)
    return {'insert': result}


@token_session_routers.get('/get-token-session')
async def get(
    id: str,
    service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    result = await service.find_by_id(id)
    return result


@token_session_routers.get('/get-token-sessions')
async def get_all(
    service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    result = await service.find_all()
    return result


@token_session_routers.patch('/update-token-session')
async def update(
    id: str,
    item: UpdateTokenSessionSchema,
    service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    result = await service.update(id, item)
    return {'updated': result}


@token_session_routers.patch('/update-token-sessions')
async def update_all(
    items: list[TokenSessionSchema],
    service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    result = await service.update_all(items)
    return {'updated': result}


@token_session_routers.delete('/delete-token-session')
async def delete(
    id: str,
    service: Annotated[TokenSessionService, Depends(token_session_service)]
):
    result = await service.delete_by_id(id)
    return {'delete_rows': result}


