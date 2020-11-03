import random

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from config.app import dp, bot
from services.parser import parser


@dp.message_handler(commands=['give_random_images'], content_types=types.ContentTypes.TEXT, state='*')
async def test_states(message: types.Message):
    result = await parser.get_list(random.randint(1, 100))
    media = [
        types.InputMediaPhoto(
            item['file_url'],
            caption=f"Author: {item['author']}\nTags: {item['tags']}"
        )
        for item in result
        if item['rating'] != 'e'
    ]
    await bot.send_media_group(
        message.chat.id,
        media
    )
