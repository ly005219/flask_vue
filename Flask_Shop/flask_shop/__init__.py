from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map




#创建一个SQLAlchemy实例
db = SQLAlchemy()#直接把下面的配置信息加载进来，因为app就是Config的实例
def create_app(config_name):
    app = Flask(__name__)
    #加载配置信息,然后后面我们可以通过crrent_app.config来获取配置信息
    app.config.from_object(config_map[config_name])

     #初始化db,让原来的db实例(db=SQLAlchemy(app))加载配置信息
    db.init_app(app)

        #注册蓝图
    from flask_shop.user import user_bp

    app.register_blueprint(user_bp)

    #获取menu的蓝图
    from flask_shop.menu import menu_bp

    app.register_blueprint(menu_bp)

    #获取role的蓝图
    from flask_shop.role import role_bp

    app.register_blueprint(role_bp)

    #获取category的蓝图
    from flask_shop.category import category_bp

    app.register_blueprint(category_bp)

    #获取attribute的蓝图
    from flask_shop.category import attribute_bp
    app.register_blueprint(attribute_bp)

    #获取product的蓝图
    from flask_shop.product import product_bp
    app.register_blueprint(product_bp)

    #获取order的蓝图
    from flask_shop.order import order_bp
    app.register_blueprint(order_bp)
    
    return app    











