from pydantic import BaseModel


class RolePermissionSchema(BaseModel):
    id: int
    role_id: int
    permission_id: int

    
class AddRolePermissionSchema(BaseModel):
    role_id: int
    permission_id: int


class UpdateRolePermissionSchema(BaseModel):
    role_id: int
    permission_id: int