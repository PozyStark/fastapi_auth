from fastapi import Request


class AuthRequest:

    request: Request
    is_authinticated: bool
    user_id: str | None
    token: str | None
    context: dict

    def __init__(
            self,
            request: Request = ...,
    ):
        self.request = request
        self.is_authinticated = False
        self.user_id = None
        self.token = None
        self.context = dict()

    def set_context(self, context: dict):
        self.context = context

    def update_context(self, context: dict):
        self.context.update(context)

    def set_token(self, token: str):
        self.token = token

    def set_user_id(self, user_id: str):
        self.user_id = user_id

    def set_is_authinticated(self, is_authinticated: bool):
        self.is_authinticated = is_authinticated

    def set_request(self, request: Request):
        self.request = request
