from pydantic import BaseModel
from datetime import datetime


class TokenSessionSchema(BaseModel):
    id: str
    user_id: str
    expire: datetime

    
class AddTokenSessionSchema(BaseModel):
    user_id: str
    expire: datetime


class UpdateTokenSessionSchema(BaseModel):
    user_id: str
    expire: datetime