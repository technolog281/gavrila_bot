from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo


def main_kb(user_tg_id: str):
    kb_list = [
        [KeyboardButton(text='Запуск приложения', web_app=types.web_app_info.WebAppInfo(url=f'https://fd35-2a01-540-8215-800-4c65-4c43-a9e5-bc0b.ngrok-free.app/{user_tg_id}'))],
    ]
    if user_tg_id in admins:
        kb_list.append([KeyboardButton(text="Админка")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Пиши, писатель..."
    )
    return keyboard


