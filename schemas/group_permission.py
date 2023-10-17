from pydantic import BaseModel


class GroupPermissionSchema(BaseModel):
    id: int
    group_id: int
    permission_id: int

    
class AddGroupPermissionSchema(BaseModel):
    group_id: int
    permission_id: int


class UpdateGroupPermissionSchema(BaseModel):
    group_id: int
    permission_id: int