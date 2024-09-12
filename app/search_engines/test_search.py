import asyncio
from app.search_engines.base import BaseSearchEngine


X_HOST = 'https://x.com'

class TestSearch(BaseSearchEngine):

    async def search(self, query: str, limit:int = 10, timeout:int=5, **kwargs) -> list:
        await asyncio.sleep(2)
        return [{
            'link': f'{X_HOST}/{query}',
            'title': f'{query}',
            'createdAt': '2023-01-01',
            'description': f'{query}',
            'content': f'test--{query}',
            'source': 'test'
        }]


