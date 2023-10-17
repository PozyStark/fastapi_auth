from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: int
    name: str

    
class AddRoleSchema(BaseModel):
    name: str


class UpdateRoleSchema(BaseModel):
    name: str