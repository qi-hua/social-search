import asyncio
import asyncpraw
from aiohttp import ClientSession

from app.search_engines.base import BaseSearchEngine


REDDIT_HOST = 'https://www.reddit.com'

class RedditSearch(BaseSearchEngine):
    def __init__(self, _loop, **kwargs):
        """需要一个loop异步运行aiohttp（保证线程安全？）"""
        self.reddit = asyncpraw.Reddit(
            requestor_kwargs={"session": ClientSession(
                trust_env=True,
                loop=_loop
            )},
            client_id="2TMNCWUHY9PCDhgd-xK87A",
            client_secret="USzYY0zGzQQG-2ahU_1irj_gBfHKVQ",
            # redirect_uri="http://localhost:8080",
            user_agent="testscript by u/qihua147",
            # username="qihua147",
            # password="myreddit.com147",
        )
        super().__init__(**kwargs)

    def transform_data(self, data):
        return {
            'id': data.id,
            'link': f"{REDDIT_HOST}{data.permalink}",
            'title': f"{data.subreddit_name_prefixed}: {data.title}",
            'host': REDDIT_HOST,
            'content': data.selftext,
            'createdAt': data.created,

            'author': data.author.name,
            # 'author_avatar': None,
            'source': 'Reddit'
        }
    
    async def search(self, query: str, limit:int = 10, timeout:int=5, **kwargs) -> list:
        subreddit = await self.reddit.subreddit("all")
        submissions = subreddit.search(
                        query=query,
                        sort="new",
                        limit=limit
                    )
        
        results = []
        async for submission in submissions:
            results.append(self.transform_data(submission))
        return results
        