from pydantic import BaseModel, validator


class Token(BaseModel):
    token: str | None = None


class AuthinticationScheme(BaseModel):

    username: str = ...
    password: str = ...


class RegistrationScheme(BaseModel):

    username: str = ...
    password: str = ...
    age: int = ...
    email: str = None
    first_name: str = None
    middle_name: str = None
    last_name: str = None

    @validator('password')
    def password_symbol_validator(cls, value):
        pass_symbols = '!@#$%&*'
        for symbol in pass_symbols:
            if symbol in value:
                return value
        raise ValueError(f'It\'s to week password must have one of {pass_symbols}')
            
    @validator('password')
    def password_length_validator(cls, value):
        if len(value) < 10:
            raise ValueError(f'Password is to short')
        return value


    # @validator('username')
    # def username_must_be_phone_number(cls, value):
    #     pattern = re.compile(r'^((\+7|7|8)+([0-9]){10})$')
    #     if not re.match(pattern, value):
    #         raise ValueError('username mast be a phone number')
    #     return value

    # @validator('password_confirm')
    # def passwords_match(cls, values):
    #     print(values['password'], values['password_confirm'])
    #     if values['password'] != values['password_confirm']:
    #         raise ValueError('passwords do not match')
    #     return values['password']