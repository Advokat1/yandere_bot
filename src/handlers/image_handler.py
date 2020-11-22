import asyncio

from aiogram import types
from config.app import dp


@dp.message_handler(commands=['take'], content_types=types.ContentTypes.TEXT, state='*')
async def take_image(message: types.Message):
    from models import Img

    def try_parse_int(s, base=10, val=False):
        try:
            return int(s, base)
        except ValueError:
            return val

    ln = 2
    if message.get_args():
        args = message.get_args().split()
        if len(args) != 0 and try_parse_int(args[0]):
            ln = int(args[0])
            if not 1 <= ln <= 10:
                await message.reply('Количество изображений может быть в диапазоне от 1 до 10')
                return

    m = False
    i = 0
    max_tries = 3
    while not m and i < max_tries:
        try:
            imgs = Img.normal().order_by_raw('RAND()').limit(ln).get()
            media_group = [
                types.InputMediaPhoto(
                    img.resource_id if img.resource_id else img.file_url,
                    caption=f'Author: {img.author} | Rating: {img.rating}\nTags: {" ".join(img.tags)}'
                ) for img in imgs
            ]
            m = await message.answer_media_group(media_group)
            for each, img in zip(m, imgs):
                if not img.resource_id and each.photo[0].file_id:
                    img.resource_id = each.photo[0].file_id
                    img.save()
        except:
            i += 1
            if i == max_tries:
                await message.answer('Произошла ошибка, попробуйте позже')
            await asyncio.sleep(1)
