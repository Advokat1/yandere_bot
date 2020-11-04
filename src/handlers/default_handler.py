from aiogram import types

from config.app import dp
from models import User


@dp.message_handler(commands=['start'], content_types=types.ContentTypes.TEXT, state="*")
async def all_other_messages(message: types.Message):
    if not User.find(message.from_user.id):
        user = User()
        user.id = message.from_user.id
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        user.username = message.from_user.username
        user.save()
    await message.answer('Welcome!')


@dp.message_handler(commands=['make_admin'], content_types=types.ContentTypes.TEXT, state="*")
async def all_other_messages(message: types.Message):
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


@dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
async def all_other_messages(message: types.Message):
    if message.content_type == "text":
        await message.reply("I don't know what it means...")
    else:
        await message.reply("WHAT IS IT?! I don't understand anything but a text.")
