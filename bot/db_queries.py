from bot.database import engine
from bot.models import users


async def save_data_to_db(data: dict[str, str]) -> int:
    async with engine.begin() as conn:
        result = await conn.execute(users.insert(), [data])
        return result.inserted_primary_key[0]
