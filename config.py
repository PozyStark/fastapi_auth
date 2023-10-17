import os
from dotenv import load_dotenv
# from models import User

# Префикс для таблицы в БД
APP_PREFIX = 'fastapi_auth'

# Модель пользователя для аутентификации
# USER_MODEL = User

# Подгружаем переменные окружения .env
load_dotenv()

# Настроки подключения к базе данных
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRESS_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

# Настроки секретного ключа и алгоритма шифрования для токена
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

# Настроки времени жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = 360
REFRESH_TOKEN_EXPIRE_MINURES = 720
