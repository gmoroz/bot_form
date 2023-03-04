from sqlalchemy import Table, Column, Integer, String, Date

from bot.database import metadata, engine


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("email", String),
    Column("phone", String),
    Column("birthdate", Date),
)


async def create_tables():
    """Создает таблицы в бд"""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all, tables=[users])
