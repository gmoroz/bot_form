from celery import Celery
from bot import settings
from bot.utils import form_write
import asyncio
from aiohttp import ClientSession

app = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(600.0, check_form_availability_task)


@app.task
def form_write_task(data: dict[str, str | int]) -> str:
    return form_write(data)


async def check_form_availability():
    async with ClientSession() as session:
        async with session.get(settings.FORM_URL) as response:
            if response.status == 200:
                print("Форма доступна!")
            else:
                print(f"С формой что-то не так. Код ответа: {response.status}")


@app.task
def check_form_availability_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_form_availability())
