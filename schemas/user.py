from datetime import datetime
from pydantic import BaseModel, field_serializer, field_validator

from utils.auth import get_hashed_password


class UserSchema(BaseModel):
    id: str = ...
    username: str = ...
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    is_superuser: bool = ...
    is_stuff: bool = ...
    is_active: bool = ...
    age: int | None = None
    avatar: str | None = None
    created_at: datetime = ...
    last_login: datetime = ...
    last_updated: datetime = ...


class UserWithPasswordSchema(UserSchema):

    password: str = ...

    
class AddUserSchema(BaseModel):
    username: str = ...
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    password: str = ...
    is_superuser: bool = False
    is_stuff: bool = False
    is_active: bool = True
    age: int | None = None
    avatar: str | None = None
    created_at: datetime = datetime.utcnow()
    last_login: datetime = datetime.utcnow()
    last_updated: datetime = datetime.utcnow()


    @field_serializer('password')
    def get_hashed_password(self, password):
        return get_hashed_password(password)


class UpdateUserSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    is_superuser: bool = None
    is_stuff: bool | None = None
    is_active: bool | None = None
    age: int | None = None
    avatar: str | None = None
    created_at: datetime | None = None
    last_login: datetime | None = None
    last_updated: datetime | None = None


class UpdadeUserPassword(BaseModel):
    old_password: str = ...
    new_password: str = ...
    confirm_password: str = ...

    @field_validator('new_password', 'confirm_password')
    def confirm_password_validator(cls, new_password, confirm_password):
        if new_password != confirm_password:
            raise ValueError('Passwords don\'t match')