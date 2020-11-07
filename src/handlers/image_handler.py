import asyncio

from aiogram import types
from config.app import dp, bot
from models import User
from services.parser import parser


@dp.message_handler(commands=['give_random_images'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    from models import Img
    img = Img.normal().order_by_raw('RAND()').limit(2).get()
    m = False
    i = 0
    while not m and i < 2:
        try:
            m = await bot.send_photo(message.chat.id, img[i].file_url)
        except:
            i += 1
            await message.answer('Что-то не так, попробую еще раз')
            await asyncio.sleep(1)


@dp.message_handler(commands=['update_list'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    user = User.find(message.from_user.id)
    if not user.is_admin:
        await message.answer('Ты не админ!')
        return
    await bot.send_message(message.chat.id, 'Начал обновлять список картинок')
    c = await parser.get_list(1, 1000, message.get_args())
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
