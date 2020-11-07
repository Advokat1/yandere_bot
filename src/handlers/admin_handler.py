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


@dp.message_handler(commands=['admin_update'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    args = message.get_args().split(' ')
    try:
        if len(args) != 0:
            page = int(args[0])
            tags = args[1:]
        else:
            page = 1
            tags = args
    except ValueError:
        page = 1
        tags = args
    await bot.send_message(message.chat.id, 'Начал обновлять список картинок')
    c = await parser.get_list(page, 1000, tags)
    await bot.send_message(message.chat.id, f'Завершил обновление ({c})')


@dp.message_handler(commands=['admin_count'], content_types=types.ContentTypes.TEXT, state='*')
async def admin_count(message: types.Message):
    from config.database import db
    from models import Img

    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    count = db.connection(db.get_default_connection()).table(Img.__table__).count()
    await message.answer(f'Сейчас бот знает {count} картинок.')


@dp.message_handler(commands=['clear_list'], content_types=types.ContentTypes.TEXT, state='*')
async def clear_list(message: types.Message):
    from config.database import db
    from models import Img

    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    await bot.send_message(message.chat.id, 'Начал удаление')
    db.connection(db.get_default_connection()).table(Img.__table__).truncate()
    await bot.send_message(message.chat.id, f'Завершил удаление')


