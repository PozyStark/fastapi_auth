from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class UserSchema(BaseModel):
    id: str = ...
    username: str = ...
    email: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    password: str = ...
    is_superuser: bool
    is_active: bool
    age: int | None
    avatar: str | None

    
class AddUserSchema(BaseModel):
    username: str = ...
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    password: str = ...
    is_superuser: bool = False
    is_active: bool = True
    age: int | None = None
    avatar: str | None = None


class UpdateUserSchema(BaseModel):
    username: str = ...
    email: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    password: str = ...
    is_superuser: bool = False
    is_active: bool = True
    age: int | None
    avatar: str | None


class UpdadeUserPassword(BaseModel):
    old_password: str = ...
    new_password: str = ...
    confirm_password: str = ...

    @validator('confirm_password')
    def paswords_match(cls, value):
        if cls.new_password != cls.confirm_password:
            raise ValueError('passwords dont match')