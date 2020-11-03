import aiohttp


class Parser:
    base_uri = 'https://yande.re'

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_list(self, page, limit=10, tags=''):
        uri = '/post.json'
        params = {
            'limit': limit,
            'page': page,
            'tags': tags
        }
        async with self.session.get(self.base_uri + uri, params=params) as response:
            json = await response.json()
            return json


parser = Parser()