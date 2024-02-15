from pydantic import BaseModel


class UserGroupSchema(BaseModel):
    id: int
    user_id: str
    group_id: int

    
class AddUserGroupSchema(BaseModel):
    user_id: str
    group_id: int


class UpdateUserGroupSchema(BaseModel):
    user_id: str
    group_id: int