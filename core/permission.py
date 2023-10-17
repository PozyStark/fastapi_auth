from abc import ABC, abstractmethod
from fastapi import HTTPException
from core.request import AuthRequest
from sqlalchemy.ext.asyncio import AsyncSession


class BasePermission(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def has_permission(
        auth_request: AuthRequest,
        async_session: AsyncSession,
        auto_error: bool = True
    ) -> bool | HTTPException:
        pass