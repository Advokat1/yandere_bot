import aiohttp


class Parser:
    base_uri = 'https://yande.re'

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_list(self, page, limit=10, tags=None):
        if tags is None:
            tags = []
        uri = '/post.json'
        params = {
            'limit': limit,
            'page': page,
            'tags': ' '.join(tags)
        }
        async with self.session.get(self.base_uri + uri, params=params) as response:
            json = await response.json()
            self.save(json)

    def save(self, array: list) -> bool:
        from models import Img

        for item in array:
            img = Img()
            img.id = item['id']
            img.tags = item['tags'].split(' ')
            img.author = item['author']
            img.source = item['source']
            img.file_url = item['file_url']
            img.score = item['score']
            img.rating = item['rating']
            img.is_rating_locked = item['is_rating_locked']
            img.has_children = item['has_children']
            img.save()
        return True


parser = Parser()