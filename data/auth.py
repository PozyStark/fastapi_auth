from pydantic.dataclasses import dataclass

@dataclass
class AuthRequest:
    headers: dict = None
    cookies: dict = None
    token: str | None = None
    is_authinticated: bool = False
    is_superuser: bool = False
    has_permissions: bool = False
    token_id: str = None
    user_id: str = None
    user_permissions: list[str] = None
    user_roles: list[str] = None
    user_groups: list[str] = None