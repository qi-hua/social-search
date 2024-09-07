import asyncio

from flask import Flask, g, request, jsonify
from flask_restx import Api, Resource, fields, Namespace, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix

from app.search_engines.base import BaseSearchEngine
from app.search_engines import SearchEngineManager

from app.utils.headers_manager import QueueHeaders
headers_manager = QueueHeaders()

class Header(BaseSearchEngine):
    headers_manager = QueueHeaders()

    def __init__(self):
        super().__init__()
        self.headers_manager.put('1', {'id': '1'})

    async def _get_headers(self):
        token_id,header = self.headers_manager.get(timeout=5)

        return token_id, header
    
    async def search(self, query: str, limit: int = 10, timeout: int = 5, **kwargs) -> list:
        token_id, header = await self._get_headers()
        print(token_id, header)
        await asyncio.sleep(2)
        self.headers_manager.release(token_id)
        return [token_id]
    

engines = [
    Header(),
]
searchEngineManager = SearchEngineManager(engines=engines)

api = Namespace('api', description='Search operations')

@api.route('/header')
class Search(Resource):
    '''search'''
    @api.doc(description='search data from social network')
    def get(self):
        '''query '''

        res = searchEngineManager.search('', limit=10)
        return res
    
import time
@api.route('/test')
class Test(Resource):
    '''test'''
    async def test(self):
        await asyncio.sleep(2)
    @api.doc(description='test')
    def get(self):
        '''test'''
        time.sleep(2)
        # asyncio.run(self.test())

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(self.test())
        # loop.close()
        return {'test': 'test'}