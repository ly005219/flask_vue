from flask import Blueprint
from flask_restful import Api


#创建蓝图对象
menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

#创建api对象
menu_api = Api(menu_bp)

#导入视图函数
from. import views



