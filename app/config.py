# flask app config
class DevelopmentConfig:
    DEBUG = True    
    SECRET_KEY = 'secret'
    # TEMPLATES_AUTO_RELOAD = True
    # TEMPLATE_FOLDER = 'templates'
    # STATIC_FOLDER = 'static'
    # STATIC_URL = ''
    # UPLOAD_FOLDER = 'uploads'
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  
    # SERVER_NAME = 'localhost:5000'
    # HOST = '0.0.0.0'
    # PORT = 5000
    # LOG_LEVEL = 'DEBUG'
    # LOG_FILE = 'logs/app.log'
    # LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    # LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'

class ProductionConfig:
    DEBUG = False
    SECRET_KEY = 'secrdsaasdf615rtw4y9835dsf1g>?<.[sfget'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}