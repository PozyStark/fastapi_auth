from pydantic import BaseModel
from datetime import datetime


class TokenSessionSchema(BaseModel):
    id: str = ...
    user_id: str = ...
    temp_id: str = ...
    expire: datetime = ...
    is_active: bool = ...

    
class AddTokenSessionSchema(BaseModel):
    user_id: str
    expire: datetime
    is_active: bool = True


class UpdateTokenSessionSchema(BaseModel):
    temp_id: str | None = None
    expire: datetime | None = None
    is_active: bool | None = None