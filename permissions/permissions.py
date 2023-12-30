from typing import Any
from fastapi import HTTPException
from starlette import status
from interfaces import AbstractPermission
from data import AuthRequest
from exceptions.exceptions import UNAUTHORIZED


class BasePermission(AbstractPermission):

    auto_error: bool
    auth_request: AuthRequest
    
    def __init__(self, **kwargs):
        self.auth_request = kwargs.get('auth_request')
        self.auto_error = kwargs.get('auto_error')

    def __call__(self, *args: Any, **kwds: Any) -> any:
        self.auth_request = kwds.get('auth_request')
        self.auto_error = kwds.get('auto_error')
        return self
    
    def exception(self, detail: str):
        raise HTTPException(
            status.HTTP_405_METHOD_NOT_ALLOWED,
            f"{detail}"
        )
        
    def has_permission(self) -> bool | HTTPException:
        print(f'BasePermission {self.auth_request.is_authinticated} {self.auto_error}')
        if not self.auth_request.is_authinticated:
            if self.auto_error:
                raise UNAUTHORIZED
            return False
        return True
        
    
class StrPermission(BasePermission):

    required_permission: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_permission = kwargs.get('required_permission')

    def has_permission(self) -> bool | HTTPException:
        super().has_permission()
        print('StrPermission')
        print(self.auth_request.user_permissions)
        if not self.required_permission in self.auth_request.user_permissions:
            if self.auto_error:
                self.exception(f'not allowed no permission {self.required_permission}')
            return False
        return True


class StrRole(BasePermission):

    required_role: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_role = kwargs.get('required_role')

    def has_permission(self) -> bool | HTTPException:
        super().has_permission()
        if not self.required_role in self.auth_request.user_roles:
            if self.auto_error:
                self.exception(f'not allowed no role {self.required_role}')
            return False
        return True


class StrGroup(BasePermission):

    required_group: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_group = kwargs.get('required_group')

    def has_permission(self) -> bool | HTTPException:
        super().has_permission()
        if not self.required_group in self.auth_request.user_groups:
            if self.auto_error:
                self.exception(f'not allowed no group {self.required_group}')
            return False
        return True


class AllowAny(BasePermission):

    def has_permission() -> bool:
        return True


class IsAuthenticated(BasePermission):

    def has_permission(self) -> bool | HTTPException:
        return super().has_permission()
        
        
class IsSuperUser(BasePermission):

    def has_permission(self) -> bool | HTTPException:
        super().has_permission()
        if not self.auth_request.is_superuser:
            if self.auto_error:
                self.exception('not allowed not super_user')
            return False
        return True
    

class IsAdminUser(BasePermission):

    permission_code: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.permission_code = 'admin'

    def has_permission(self) ->  bool | HTTPException:
        if self.permission_code not in self.auth_request.user_roles:
            if self.auto_error:
                self.exception(f'not allowed not admin')
            return False
        return True
 

# class IsActive(BasePermission):
    # pass