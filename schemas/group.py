from pydantic import BaseModel


class GroupSchema(BaseModel):
    id: int
    name: str

    
class AddGroupSchema(BaseModel):
    name: str


class UpdateGroupSchema(BaseModel):
    name: str