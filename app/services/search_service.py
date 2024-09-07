import asyncio

from flask import Flask, g, request, jsonify
from flask_restx import Api, Resource, fields, Namespace, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix


from app.search_engines import SearchEngineManager
from app.search_engines import RedditSearch
from app.search_engines import XSearch

from app.search_engines import TestSearch

searchEngineManager = SearchEngineManager()
searchEngineManager.engines = [
    # RedditSearch(searchEngineManager._loop, proxy='http://127.0.0.1:7897'),
    # XSearch(proxy='http://127.0.0.1:7897'),
    TestSearch(),
    TestSearch(),
    TestSearch(),
]

api = Namespace('api', description='Search operations')


search_parser = reqparse.RequestParser()
search_parser.add_argument('query', type=str, required=True, help='query is required')
search_parser.add_argument('count', type=int, required=False, help='count is optional')
search_parser.add_argument('product_type', choices=('Latest','Top','People','Media','Lists'), required=False, help='product_type is optional')

@api.route('/search')
class Search(Resource):
    '''search'''
    @api.doc(description='search data from social network')
    @api.expect(search_parser)
    def get(self):
        '''query '''
        # authorization = g.authorization
        args = search_parser.parse_args()
        # print(args)
        res = searchEngineManager.search(timeout=10, limit=15, **args)
        # print(res)
        return jsonify(res)
    