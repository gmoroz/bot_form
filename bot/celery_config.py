from celery import Celery
from bot import settings
from bot.utils import form_write
import asyncio
from aiohttp import ClientSession

app = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL
)


@app.task
def form_write_task(data: dict[str, str | int]) -> str:
    return form_write(data)


async def check_form_availability():
    while True:
        async with ClientSession() as session:
            async with session.get(settings.FORM_URL) as response:
                if response.status == 200:
                    print("Форма доступна!")
                else:
                    print(f"С формой что-то не так. Код ответа: {response.status}")
        await asyncio.sleep(600)


@app.task
def check_form_availability_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_form_availability())


check_form_availability_task.delay()
