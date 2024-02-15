from typing import Any
from fastapi import HTTPException
from starlette import status
from dependencies import AuthRequest
from interfaces import AbstractPermission


class BasePermission(AbstractPermission):

    auth_request: AuthRequest
    
    def __init__(self, **kwargs):
        self.auth_request = kwargs.get('auth_request')

    def __call__(self, *args: Any, **kwds: Any) -> any:
        self.auth_request = kwds.get('auth_request')
        return self
    
    def exception(self, detail: str):
        raise HTTPException(
            status.HTTP_405_METHOD_NOT_ALLOWED,
            f"{detail}"
        )
        
    def has_permission(self) -> HTTPException:
        if not self.auth_request.user.is_authinticated:
            self.exception('Not allowed not authinticated')
        
    
class StrPermission(BasePermission):

    required_permission: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_permission = kwargs.get('required_permission')

    def has_permission(self) -> HTTPException:
        super().has_permission()
        if not self.required_permission in self.auth_request.user.user_permissions:
            self.exception(f'Not allowed has no permission {self.required_permission}')


class StrRole(BasePermission):

    required_role: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_role = kwargs.get('required_role')

    def has_permission(self) -> HTTPException:
        super().has_permission()
        if not self.required_role in self.auth_request.user.user_roles:
            self.exception(f'Not allowed has no role {self.required_role}')


class StrGroup(BasePermission):

    required_group: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_group = kwargs.get('required_group')

    def has_permission(self) -> HTTPException:
        super().has_permission()
        if not self.required_group in self.auth_request.user.user_groups:
            self.exception(f'Not allowed has no group {self.required_group}')


class AllowAny(BasePermission):

    def has_permission() -> HTTPException:
        pass


class IsAuthenticated(BasePermission):

    def has_permission(self) -> HTTPException:
        super().has_permission()
        
        
class IsSuperUser(BasePermission):

    def has_permission(self) -> bool | HTTPException:
        super().has_permission()
        if not self.auth_request.user.is_superuser:
            self.exception('Not allowed not a super_user')


class IsAdminUser(BasePermission):

    permission_code: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.permission_code = 'admin'

    def has_permission(self) ->  bool | HTTPException:
        if self.permission_code not in self.auth_request.user.user_roles:
            self.exception(f'Not allowed not admin')
 

class IsStuff(BasePermission):

    def has_permission(self) ->  bool | HTTPException:
        if not self.auth_request.user.is_stuff:
            self.exception(f'Not allowed not is_staff')