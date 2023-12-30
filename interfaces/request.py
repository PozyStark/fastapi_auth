from fastapi import Request
from interfaces import AbstractPermission
from abc import ABC 

class AbstractRequest(ABC):

    request: Request
    is_authinticated: bool
    is_superuser: bool
    has_permission: bool
    token: str | None
    token_id: str | None
    user_id: str | None
    user_permissions: list[AbstractPermission | str]
    user_roles: list[str]
    user_groups: list[str]