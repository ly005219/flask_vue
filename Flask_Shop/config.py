import os



class Config:
    
    
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'flask_shop'
    #更换自己的数据库名称
    #MYSQL_DB = 'connect_flask'
    MYSQL_PORT = 3306
    
    MYSQL_CHARSET = 'utf8mb4'
    # 在Docker环境中，使用服务名作为主机名
    # MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
    # SQLALCHEMY_DATABASE_URI =f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
   
    #不用docker就用localhost
    MYSQL_HOST = 'localhost'
    SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    DEBUG = True

    #设置JSON数据不使用ASCII编码
    RESTFUL_JSON = {'ensure_ascii': False}
    #设置JSON数据使用中文
    JSON_AS_ASCII = False
    #设置token过期时间
    JWT_EXPIRATION_DELTA = 3600 * 24 * 1 # 1 days
    #设置token加密密钥
    SECRET_KEY = os.urandom(16)
    #设置可以上传的图片类类型
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}
    #获取当前目前的根路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))#当前路径的上一级
    #设置上传图片的路径
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'flask_shop','static/uploads')

  
    


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}




