from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str | None = None


class RefreshToken(BaseModel):
    refresh_token: str | None = None