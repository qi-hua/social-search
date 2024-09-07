from flask import Flask, request, g, jsonify
from flask_cors import CORS
from flask_restx import Api

from .config import config

def before_request():
    if request.path.startswith('/static') or request.path.startswith('/docs') or request.path.startswith('//swaggerui'):
        return
    authorization = request.headers.get('Authorization')
    if authorization:
        if not authorization.startswith('Bearer '):
            authorization = 'Bearer ' + authorization
        # 将Authorization信息注入到上下文中
        g.authorization = authorization
    else:
        return jsonify({
            'status': 'error',
            'message': 'Authorization is required'
        }, 401)

def create_app(config_name):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 开启跨域
    CORS(app,
        resources={r"/api/*": {"origins": "*"}},
    )
    # 添加中间件
    # app.before_request(before_request)

    api = Api(
            title='Search API',
            description='Search API',
            version='1.0',
            doc='/docs'
        )
    
    from app.services import api as search_api
    from app.services import header_api

    api.add_namespace(search_api)
    api.add_namespace(header_api)
    api.init_app(app)

    return app