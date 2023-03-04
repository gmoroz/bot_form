from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData

from bot import settings

# конфигурация подключения к базе данных
engine = create_async_engine(settings.DB_URI, echo=True)
metadata = MetaData()
