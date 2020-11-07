import aiohttp


class Parser:
    base_uri = 'https://danbooru.donmai.us'

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_list(self, page, limit=500, tags=[]) -> int:
        if tags is []:
            tags = ['rating:s', 'rating:q']
        uri = '/posts.json'
        params = {
            'limit': limit,
            'page': page,
            'tags': ' '.join(tags)
        }
        async with self.session.get(self.base_uri + uri, params=params) as response:
            json = await response.json()
            return self.save(json)

    def save(self, array: list) -> int:
        from models import Img

        c = 0
        for item in array:
            if 'id' not in item:
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
        return c


parser = Parser()
