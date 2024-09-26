from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from keyboards.all_kb import main_kb
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo
from create_bot import dp
import psycopg2
import psycopg2.extras
from decouple import config
from contextlib import closing

router = Router()
db_conn_link = config('PG_LINK')


def vtg_socket(user_first_name, tg_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 1488))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                conn.sendall(user_first_name, tg_id)
                break


@router.message(Command('start'))
async def start(message: types.Message):
    with closing(psycopg2.connect(db_conn_link)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''SELECT first_name FROM vtg_users where telegram_id = '{message.from_user.id}';''')
            result = cursor.fetchone()
            vtg_socket(message.from_user.first_name, message.from_user.id)
    if result is not None:
        await message.answer(f'Привет, {message.from_user.first_name}. '
                             f'\n Запускай приложение и начнём считать ;)',
                             reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer(f'Привет, мы не знакомы. Напиши свой идентификатор.')


@router.message(F.text)
async def get_id(message):
    with closing(psycopg2.connect(db_conn_link)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''SELECT first_name FROM vtg_users where reg_id = '{message.text}';''')
            check_reg_id = cursor.fetchone()
            if check_reg_id is not None:
                cursor.execute(
                    f'''UPDATE vtg_users SET telegram_id='{message.from_user.id}',
                     user_name='{message.from_user.first_name}' WHERE reg_id='{message.text}';''')
                conn.commit()
                await message.answer(f'Привет, {check_reg_id[0]}, теперь мы знакомы :)',
                                     reply_markup=main_kb(message.from_user.id))
                vtg_socket(message.from_user.first_name, message.from_user.id)
            else:
                await message.answer(f'Ты кто такой? Иди нахуй отсюда, я тебя не звал.')
