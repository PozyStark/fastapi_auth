from sqlalchemy import create_engine
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

# Для работы в асинхронном режиме
# pg_engine_async = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
# async_session = async_sessionmaker(bind=pg_engine_async, class_=AsyncSession, expire_on_commit=False)

# Для работы в синхронном режиме
# pg_engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
# sync_session = sessionmaker(bind=pg_engine, expire_on_commit=False)

# Для работы с SqlLite в асинхронном режиме
sqlite_engine_async = create_async_engine(f'sqlite+aiosqlite:///auth_data.sqlite')
async_session = async_sessionmaker(bind=sqlite_engine_async, class_=AsyncSession, expire_on_commit=False)