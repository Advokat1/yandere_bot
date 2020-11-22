import asyncio

import aiohttp
from aiogram import types


class Parser:
    base_uri = 'https://danbooru.donmai.us'

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_list(self, page, pages=1, tags=None, initiator=None) -> int:
        if tags is None:
            tags = ['rating:s']
        uri = '/posts.json'
        c = 0
        for i in range(page, page+pages):
            params = {
                'limit': 200,
                'page': i,
                'tags': ' '.join(tags)
            }
            async with self.session.get(self.base_uri + uri, params=params) as response:
                json = await response.json()
                c += await self.save(json, initiator)

        return c

    async def save(self, array: list, initiator) -> int:
        from models import Img

        c = 0
        last_ten = []
        for item in array:
            if 'id' not in item:
                continue
            if item['file_ext'] not in ['png', 'jpg']:
                continue
            img = Img()
            img.id = item['id']
            img.tags = item['tag_string'].split(' ')
            img.author = item['tag_string_artist']
            img.source = item['source']
            img.file_url = item['file_url']
            img.score = item['score']
            img.rating = item['rating']
            img.is_rating_locked = item['is_rating_locked']
            img.has_children = item['has_visible_children']
            if img.save():
                c += 1
                last_ten.append(img)
                if len(last_ten) == 10:
                    await self.send_media_group(last_ten, initiator)
                    await asyncio.sleep(3)
                    last_ten = []

        await self.send_media_group(last_ten, initiator)

        return c

    async def send_media_group(self, imgs, chat_id):
        media = types.MediaGroup()
        for i in imgs:
            media.attach_photo(i.file_url)
        try:
            from config.app import bot
            reply = await bot.send_media_group(chat_id=chat_id, media=media, disable_notification=True)
            for each, img in zip(reply, imgs):
                if each.photo[0].file_id:
                    img.resource_id = each.photo[0].file_id
                    img.save()
        except:
            pass

    async def upgrade_db(self, iniciator):
        from models import Img

        processed = 0
        imgs = Img.where_null('resource_id').order_by_raw('RAND()').limit(5).get()
        while imgs and processed < 100:
            await self.send_media_group(imgs, iniciator)
            processed += len(imgs)
            await asyncio.sleep(2.5)
            imgs = Img.where_null('resource_id').order_by_raw('RAND()').limit(5).get()

        return processed



parser = Parser()
