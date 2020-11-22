from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from models import User
from config.app import dp, bot
from services.parser import parser
from helpers.permissions import is_admin
from states.AdminStates import RemoveConfirmation


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
async def admin_update(message: types.Message):
    if not await is_admin(message):
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
    try:
        if len(args) != 0:
            pages = int(tags[0])
            tags = args[2:]
        else:
            pages = 1
            tags = tags
    except ValueError:
        pages = 1
        tags = args

    await bot.send_message(message.chat.id, 'Начал обновлять список картинок')
    c = await parser.get_list(page, pages, tags, message.chat.id)
    await bot.send_message(message.chat.id, f'Завершил обновление ({c})')


@dp.message_handler(commands=['admin_count'], content_types=types.ContentTypes.TEXT, state='*')
async def admin_count(message: types.Message):
    if not await is_admin(message):
        return
    from config.database import db
    from models import Img

    count = db.connection(db.get_default_connection()).table(Img.__table__).count()
    await message.answer(f'Сейчас бот знает {count} картинок.')


@dp.message_handler(commands=['clear_list'], content_types=types.ContentTypes.TEXT, state='*')
async def clear_list(message: types.Message):
    if not await is_admin(message):
        return
    from config.database import db
    from models import Img

    await bot.send_message(message.chat.id, 'Начал удаление')
    db.connection(db.get_default_connection()).table(Img.__table__).truncate()
    await bot.send_message(message.chat.id, f'Завершил удаление')


@dp.message_handler(commands=['admin_leave'], content_types=types.ContentTypes.TEXT, state='*')
async def admin_leave(message: types.Message):
    if not await is_admin(message):
        return
    await RemoveConfirmation.need_confirming.set()
    await message.answer('Вы уверены, что хотите удалить себе пара администратора?\n'
                         'Отправь /cancel для отмены, /confirm для подтверждения')


@dp.message_handler(commands=['admin_upgrade_db'], content_types=types.ContentTypes.TEXT, state='*')
async def admin_upgrade_db(message: types.Message):
    if not await is_admin(message):
        return
    c = await parser.upgrade_db(message.chat.id)
    await message.answer(f'Было улучшено {c} файлов, если файлов меньше 100 - были обновлены все файлы')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('Отменено.')


@dp.message_handler(commands=['confirm'],
                    content_types=types.ContentTypes.TEXT,
                    state=RemoveConfirmation.need_confirming)
async def remove_confirmation(message: types.Message, state: FSMContext):
    if not await is_admin(message):
        return
    await state.finish()
    user = User.find(message.from_user.id)
    user.is_admin = False
    user.save()
    await message.answer('Права администратора успешно удалены')
