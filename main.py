import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot import settings
from bot.models import create_tables
from bot.database import engine


# создаем объекты бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    try:
        await create_tables()
        await dp.start_polling()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
