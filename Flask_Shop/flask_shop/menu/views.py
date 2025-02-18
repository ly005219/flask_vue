from flask_shop.menu import menu_api
from flask_restful import Resource
from flask_shop import models
from flask import request


class Menus(Resource):
    def get(self):
        try:
            type_ = request.args.get('type_')
            if type_ == 'tree':
                # 获取所有一级菜单
                menus = models.Menu.query.filter_by(level=1).all()
                menu_list = [menu.to_dict_tree() for menu in menus]
                return {
                    'status': 200,
                    'msg': '获取菜单成功',
                    'data': menu_list
                }
            else:
                # 获取所有菜单列表
                menus = models.Menu.query.all()
                menu_list = [menu.to_dict_list() for menu in menus]
                return {
                    'status': 200,
                    'msg': '获取菜单成功',
                    'data': menu_list
                }
        except Exception as e:
            print(f"获取菜单错误: {str(e)}")
            return {'status': 500, 'msg': str(e)}


menu_api.add_resource(Menus, '/menus/')

