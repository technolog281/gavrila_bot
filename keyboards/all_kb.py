from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text='Запуск приложения', web_app=types.web_app_info.WebAppInfo(url='https://76ff-2a01-540-8f01-9500-f895-20f9-1cf7-aab9.ngrok-free.app'))],
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="Админка")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Пиши, писатель..."
    )
    return keyboard


