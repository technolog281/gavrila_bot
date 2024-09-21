from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from keyboards.all_kb import main_kb
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo
from create_bot import dp

start_router = Router()


@start_router.message(Command('start'))
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}',
                         reply_markup=main_kb(message.from_user.id))
