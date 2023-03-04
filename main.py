import asyncio
from bot.models import create_tables
from bot.database import engine
from bot.handlers import dp


async def main():
    try:
        await create_tables()
        await dp.start_polling()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
