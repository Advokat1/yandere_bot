from aiogram import types

from models import User
from config.app import dp, bot
from services.parser import parser


@dp.message_handler(commands=['make_admin'], content_types=types.ContentTypes.TEXT, state="*")
async def make_admin(message: types.Message):
    from os import getenv
    password = message.get_args()
    secret = getenv('ADMIN_PASSWORD', False)
    user = User.find(message.from_user.id)
    if user.is_admin:
        await message.answer('Теперь уже админ!')
        return
    if secret and secret == password:
        user.is_admin = True
        user.save()
        await message.answer('Теперь ты админ!')
    else:
        await message.answer('Неправильный пароль!')


@dp.message_handler(commands=['update_list'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    await bot.send_message(message.chat.id, 'Начал обновлять список картинок')
    c = await parser.get_list(1, 1000, message.get_args().split(' '))
    await bot.send_message(message.chat.id, f'Завершил обновление ({c})')


@dp.message_handler(commands=['init_img'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    import asyncio
    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    await bot.send_message(message.chat.id, 'Начал загружать список картинок')
    for i in range(1, 50):
        c = await parser.get_list(i, 1000)
        await asyncio.sleep(1)
    await bot.send_message(message.chat.id, f'Завершил обновление ({c})')


@dp.message_handler(commands=['clear_list'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    from config.database import db
    from models import Img

    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    await bot.send_message(message.chat.id, 'Начал удаление')
    db.connection(db.get_default_connection()).table(Img.__table__).truncate()
    await bot.send_message(message.chat.id, f'Завершил удаление')


