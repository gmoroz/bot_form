from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot import settings
from bot.db_queries import save_data_to_db

# создаем объекты бота и память для состояний
bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    name = State()
    surname = State()
    email = State()
    phone = State()
    birthdate = State()


@dp.message_handler(Command("form"))
async def start_form(message: Message):
    await Form.name.set()
    await message.reply(
        "Привет! Пожалуйста, введите данные для заполнения формы. Напишите ваше имя"
    )


@dp.message_handler(state=Form.name)
async def process_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    await Form.next()
    await message.reply("Введите вашу фамилию")


@dp.message_handler(state=Form.surname)
async def process_surname(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["surname"] = message.text

    await Form.next()
    await message.reply("Введите ваш email")


@dp.message_handler(state=Form.email)
async def process_email(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["email"] = message.text

    await Form.next()
    await message.reply("Введите ваш телефон")


@dp.message_handler(state=Form.phone)
async def process_phone(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text

    await Form.next()
    await message.reply("Введите вашу дату рождения в формате ГГГГ-ММ-ДД")


@dp.message_handler(state=Form.birthdate)
async def process_birthdate(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["birthdate"] = message.text
        await message.answer(f"ваши данные: {data.items()}")

    # После получения всех данных сохраняем их в базу данных
    await save_data_to_db(data)

    await state.finish()
    await message.reply("Спасибо за заполнение формы!")
