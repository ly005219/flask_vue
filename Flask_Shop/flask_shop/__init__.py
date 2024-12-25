from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    
    # 简化CORS配置
    CORS(app, supports_credentials=True)
    
    # 初始化db
    db.init_app(app)

    # 注册蓝图
    from flask_shop.user import user_bp
    app.register_blueprint(user_bp)

    # 注册菜单蓝图
    from flask_shop.menu import menu_bp
    app.register_blueprint(menu_bp)

    # 注册角色蓝图
    from flask_shop.role import role_bp
    app.register_blueprint(role_bp)

    # 注册分类蓝图
    from flask_shop.category import category_bp
    app.register_blueprint(category_bp)

    # 注册属性蓝图
    from flask_shop.category import attribute_bp
    app.register_blueprint(attribute_bp)

    # 注册商品蓝图
    from flask_shop.product import product_bp
    app.register_blueprint(product_bp)

    # 注册订单蓝图
    from flask_shop.order import order_bp
    app.register_blueprint(order_bp)

    # 注册SKU蓝图
    from flask_shop.sku import sku_bp
    app.register_blueprint(sku_bp)

    @app.errorhandler(Exception)
    def handle_error(error):
        print(f"全局错误处理: {str(error)}")
        return {'status': 500, 'msg': str(error)}, 500

    return app    











