from pydantic import BaseModel


class PermissionSchema(BaseModel):
    id: int
    codename: str
    description: str

    
class AddPermissionSchema(BaseModel):
    codename: str
    description: str


class UpdatePermissionSchema(BaseModel):
    codename: str
    description: str