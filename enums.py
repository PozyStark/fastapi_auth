from enum import Enum


class SearchMode(Enum):
    HEADER_MODE = 0
    COOKIE_MODE = 1


class TokenType(Enum):
    ACCESS_TOKEN = 0
    REFRESH_TOKEN = 1