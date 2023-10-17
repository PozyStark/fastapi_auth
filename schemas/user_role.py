from pydantic import BaseModel


class UserRoleSchema(BaseModel):
    id: int
    user_id: str
    role_id: int

    
class AddUserRoleSchema(BaseModel):
    user_id: str
    role_id: int


class UpdateUserRoleSchema(BaseModel):
    user_id: str
    role_id: int