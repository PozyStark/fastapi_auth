from sqlalchemy import create_engine
from config import DB_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


# Подключение к БД в асинхронном режиме
sqlite_engine_async = create_async_engine(DB_URL)
async_session = async_sessionmaker(bind=sqlite_engine_async, class_=AsyncSession, expire_on_commit=False)