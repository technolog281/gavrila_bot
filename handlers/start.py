from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from keyboards.all_kb import main_kb
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo
from create_bot import dp
from decouple import config
from contextlib import closing
import sqlite3

router = Router()
connection = sqlite3.connect('gavrila_bot.db')


def initial():
    with closing(connection.cursor()) as cursor:
        cursor.execute('''CREATE TABLE "vtg_users" (
	                        "first_name"	TEXT NOT NULL,
	                        "second_name"	TEXT NOT NULL,
	                        "work_schema"	INTEGER,
	                        "tg_id"	NUMERIC,
	                        "reg_id"	NUMERIC,
	                        "user_name"	TEXT,
	                        PRIMARY KEY("reg_id")
                    )''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Ирина', 'Шишкина', '1', '', '9125296269', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Артём', 'Шабалин', '1', '', '9128368646', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Тутова', 'Любовь', '1', '', '9195826516', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Роман', 'Логинов', '2', '', '9630053850', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Дмитрий', 'Логинов', '2', '', '9091715672', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Иван', 'Кочев', '2', '', '9125230203', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Всеволод', 'Атаманюк', '1', '', '9195910701', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Елена', 'Гайдабурова', '2', '', '9512628870', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Матвей', 'Галковский', '1', '', '9965580490', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Александр', 'Ершов', '1', '', '9323163803', '');''')
        cursor.execute(
            '''INSERT INTO "main"."vtg_users" ("first_name", "second_name", "work_schema", "tg_id", "reg_id", "user_name") VALUES ('Тест', 'Тестовый', '1', '', '777', '');''')
        connection.commit()


@router.message(Command('start'))
async def start(message: types.Message):
    with closing(connection.cursor()) as cursor:
        check_db = cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='vtg_users';''')
        if not check_db.fetchall():
            initial()
        cursor.execute(f'''SELECT first_name FROM vtg_users where tg_id = '{message.from_user.id}';''')
        result = cursor.fetchone()
        if result is not None:
            await message.answer(f'Привет, {message.from_user.first_name}. '
                                 f'\n Запускай приложение и начнём считать ;)',
                                 reply_markup=main_kb(message.from_user.id))
        else:
            await message.answer(f'Привет, мы не знакомы. Напиши свой идентификатор.')


@router.message(F.text)
async def get_id(message):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f'''SELECT first_name FROM vtg_users where reg_id = '{message.text}';''')
        check_reg_id = cursor.fetchone()
        if check_reg_id is not None:
            cursor.execute(
                f'''UPDATE vtg_users SET tg_id='{message.from_user.id}',
                     user_name='{message.from_user.first_name}' WHERE reg_id='{message.text}';''')
            connection.commit()
            await message.answer(f'Привет, {check_reg_id[0]}, теперь мы знакомы :)',
                                 reply_markup=main_kb(str(message.from_user.id)))
        else:
            await message.answer(f'Ты кто такой? Иди нахуй отсюда, я тебя не звал.')
