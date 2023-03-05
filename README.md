### Запуск приложения через docker-compose:

Создайте файл .env.docker в соответствии .env.docker.example
При желании можно прописать только BOT_TOKEN
Далее склонировать репо и запустить docker контейнеры:

    git clone https://github.com/gmoroz/bot_form
    cd cd bot_form
    docker-compose up -d

### Остановка приложения через docker-compose:

Если надо удалить данные бд, добавьте в конце команды флаг `-v`

    docker-compose down

### Запуск через docker (бот и celery):

Создайте файл .env в соответствии .env.example
Запустите и настройте redis, postgres

Соберите контейнер и запустите celery и бота:

    docker build -t form .
    docker run --name bot_form -v images:/code/images form python main.py
    docker run --name celery_form -v images:/code/images form celery -A bot.celery_config worker -B
