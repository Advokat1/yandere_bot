import asyncio

from aiogram import types
from config.app import dp, bot
from models import User
from services.parser import parser


@dp.message_handler(commands=['give_random_images'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    from models import Img
    img = Img.normal().order_by_raw('RAND()').limit(1).get()
    m = False
    while not m:
        try:
            m = await bot.send_photo(message.chat.id, img[0].file_url)
        except:
            await asyncio.sleep(1)


@dp.message_handler(commands=['update_list'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    await bot.send_message(message.chat.id, 'Начал обновлять список картинок')
    await parser.get_list(1, 1000)
    await bot.send_message(message.chat.id, 'Завершил обновление')


@dp.message_handler(commands=['init_img'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    await bot.send_message(message.chat.id, 'Начал загружать список картинок')
    for i in range(1, 50):
        await parser.get_list(i, 1000)
    await bot.send_message(message.chat.id, 'Завершил обновление')
