import os
from dotenv import load_dotenv
from enums import SearchMode


# Подгружаем переменные окружения .env
load_dotenv()


# Префикс для таблицы в БД
APP_PREFIX = 'fastapi_auth'


# Настроки подключения к базе данных
# DB_HOST = os.environ.get('DB_HOST')
# DB_PORT = os.environ.get('DB_PORT')
# DB_NAME = os.environ.get('POSTGRESS_DB')
# DB_USER = os.environ.get('POSTGRES_USER')
# DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
# DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DB_URL = 'sqlite+aiosqlite:///auth_data.sqlite'



# Настроки секретного ключа и алгоритма шифрования для токена
ACCESS_SECRET_KEY = os.environ.get('ACCESS_SECRET_KEY')
REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY')

ALGORITHM = os.environ.get('ALGORITHM')
SCHEMES = ['bcrypt']
DEPRECATED = 'auto'


# Настроки времени жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINURES = 720


# Настройки режима поиска токена по умолчанию
SEARCH_MODE = SearchMode.COOKIE_MODE


# Настройка сохранения токена в cookie при авторизации
SAVE_IN_COOKIE = True