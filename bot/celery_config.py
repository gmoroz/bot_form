from celery import Celery
from bot import settings
from bot.utils import form_write

app = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL
)


@app.task
def form_write_task(data: dict[str, str | int]):
    form_write(data)
