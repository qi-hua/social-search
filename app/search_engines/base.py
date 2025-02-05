import json
import asyncio
import threading
from concurrent.futures import Future
from typing import Any, Awaitable, Dict, Optional, Type, Union

from typing import List
from abc import abstractmethod


class BaseSearchEngine:
    def __init__(self, headers: dict = None, proxy: str = None, timeout: int = 10, source: str = None):
        self.headers = headers
        self.proxy = proxy
        self.timeout = timeout
        self.source = source

    # TODO: 增加初始化测试，判断engine是否有效

    @abstractmethod
    async def search(self, query: str, limit: int = 10, timeout: int = 5, **kwargs) -> list:
        pass

    # 备选方案，当默认搜索失败时，使用备选方案
    async def search_alternative(self, query: str, limit: int = 10, timeout: int = 5, **kwargs) -> list:
        return []

    async def _search(self, query: str, limit: int = 10, timeout: int = 5, **kwargs) -> list:
        try:
            return await asyncio.wait_for(self.search(query, limit, timeout, **kwargs), timeout=timeout)
        except Exception as e:
            # print(e)
            # raise e
            try:
                return await asyncio.wait_for(self.search_alternative(query, limit, timeout, **kwargs), timeout=timeout)
            except Exception as e:
                # print(e)
                # raise e
                return []

class SearchEngineManager:
    _loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    threading.Thread(target=_loop.run_forever, daemon=True).start()

    def __init__(self, headers: dict = None, proxy: str = None, timeout: int = 10, engines: List[BaseSearchEngine] = None):
        self.headers = headers
        self.proxy = proxy
        self.timeout = timeout
        if engines:
            self.engines = engines
        else:
            self.init_engines()
        
    def init_engines(self):
        self.engines = [
            # DDGS(self.headers, self.proxy, self.timeout),
        ]
    
    async def _search(self, query: Union[str,List[str]], limit: int = 10, timeout: int = 5,  engines: List[BaseSearchEngine] = None, **kwargs) -> list:
        if isinstance(query, str):
            queries = [query]
        elif isinstance(query, list):
            queries = query
        else:
            raise TypeError("query must be str or list")
        if not engines:
            engines = self.engines
        results = []
        tasks = []
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(engine._search(query, limit, timeout, **kwargs)) for query in queries for engine in engines]
        for task in tasks:
            results_ = task.result()
            results.extend(results_)
        # TODO: 根据相关性排序，并返回limit个与query相似的结果，并限定其中内容的长度


        return results
    
    def search(self, query: str, limit: int = 10, timeout: int = 5,  engines: List[BaseSearchEngine] = None, **kwargs) -> list:
        return self._run_async_in_thread(self._search(query, limit, timeout, engines, **kwargs))
        # return asyncio.run(self._search(query, limit, timeout, engines, **kwargs))
    
    def _run_async_in_thread(self, coro: Awaitable[Any]) -> Any:
        """Runs an async coroutine in a separate thread."""
        future: Future[Any] = asyncio.run_coroutine_threadsafe(coro, self._loop)
        result = future.result()
        return result