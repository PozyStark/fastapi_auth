from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class AuthinticationScheme(BaseModel):

    username: str = ...
    password: str = ...


class RequestToken(BaseModel):
    token: str | None = None
    token_id: str | None = None
    temp_id: str | None = None
    user_id: str | None = None


class RequestUser(BaseModel):
    id: str = None
    username: str = 'anonimus'
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    is_authinticated: bool = False
    is_superuser: bool = False
    is_stuff: bool = False
    is_active: bool = False
    age: int | None = None
    avatar: str | None = None
    user_permissions: list | None = None
    user_roles: list | None = None
    user_groups: list | None = None
    created_at: datetime | None
    last_login: datetime | None
    last_updated: datetime | None


class RegistrationScheme(BaseModel):

    username: str = ...
    password: str = ...
    confirm_password: str = ...
    age: int | None = None
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None

    @field_validator('password')
    def password_symbol_validator(cls, value):
        pass_symbols = '!@#$%&*'
        for symbol in pass_symbols:
            if symbol in value:
                return value
        raise ValueError(f'It\'s to week password must have one of {pass_symbols}')
            
    @field_validator('password')
    def password_length_validator(cls, value):
        if len(value) < 10:
            raise ValueError(f'Password is to short')
        return value
    
    @field_validator('confirm_password')
    def confirm_password_validator(cls, v, values):
        if v != values.data['password']:
            raise ValueError(f'Password don\'t match')
        return v  

    # @validator('username')
    # def username_must_be_phone_number(cls, value):
    #     pattern = re.compile(r'^((\+7|7|8)+([0-9]){10})$')
    #     if not re.match(pattern, value):
    #         raise ValueError('username mast be a phone number')
    #     return value