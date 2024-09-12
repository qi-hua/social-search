import time
import json
from typing import Union
from flask_restx import Resource, Namespace, reqparse

from app.search_engines import SearchEngineManager
from app.search_engines import RedditSearch
from app.search_engines import XSearch

from app.search_engines import TestSearch

searchEngineManager = SearchEngineManager()
searchEngineManager.engines = [
    RedditSearch(searchEngineManager._loop),
    XSearch(),
    # TestSearch(),
    # TestSearch(),
    # TestSearch(),
]

api = Namespace('api', description='Search operations')

def json_type(value):
    try:
        return json.loads(value)
    except ValueError as e:
        return value
    
def boolean(value: Union[bool|str]):
    if isinstance(value, bool):
        return value
    if value.lower() in ['true', '1', 'yes']:
        return True
    elif value.lower() in ['false', '0', 'no']:
        return False
    else:
        raise ValueError('Invalid boolean value')
    
search_parser = reqparse.RequestParser()
search_parser.add_argument('query', type=json_type, required=True, help='query is JSON encoded list or string')
search_parser.add_argument('justtext', type=boolean, required=False, default=True, help='justtext is optional, controls whether to return text or not')

@api.route('/search')
class Search(Resource):
    '''search'''
    @api.doc(description='search data from social network')
    @api.expect(search_parser)
    def get(self):
        '''query能够是列表或者字符串
        
        query:["query1","query2","query3"]
        query:query1'''
        start_time = time.time()
        # authorization = g.authorization
        args = search_parser.parse_args()
        if not args.get('query'):
            return {'message': 'query is required'}, 400
        if not args.get('limit'):
            if isinstance(args.get('query'), list):
                args['limit'] = 5 if len(args.get('query')) > 3 else 10
            else:
                args['limit'] = 10
        res = searchEngineManager.search(timeout=10, **args)
        end_time = time.time()
        if args.get('justtext'):
            result = '\n---\n\n'.join([self.format_data(index+1,item) for index, item in enumerate(res)])
        else:
            result = {
                'status': 'success',
                'data': res,
                'time': end_time - start_time,
            }
        return result
    

    def format_data(self,id,data):
        return f"""**{id}: {data['title']} - {data['createdAt']}**\n\n> {data['content']}\n"""
