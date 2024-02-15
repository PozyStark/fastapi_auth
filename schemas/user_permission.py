from pydantic import BaseModel


class UserPermissionSchema(BaseModel):
    id: int
    user_id: str
    permission_id: int

    
class AddUserPermissionSchema(BaseModel):
    user_id: str
    permission_id: int


class UpdateUserPermissionSchema(BaseModel):
    user_id: str
    permission_id: int