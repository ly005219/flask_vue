from flask_shop.menu import menu_api
from flask_restful import Resource
from flask_shop import models
from flask import request


class Menus(Resource):
    def get(self):
        #获取前端页面要求二点数据类型,list,type
        type_=request.args.get('type_')
        if type_=='tree':
            #通过模型获取菜单数据
            menu_list=models.Menu.query.filter(models.Menu.level==1).all()
            #将菜单数据转换为字典列表
            menu_dict_list=[]
            for menu in menu_list:
                menu_dict_list.append(menu.to_dict_tree())
            return {'status':200,'msg':'获取tree菜单成功','menus':menu_dict_list}   
        else:
            #通过模型获取菜单数据
            menu_list=models.Menu.query.filter(models.Menu.level != 0).all()

            #将菜单数据转换为字典列表
            menu_dict_list=[]
            for menu in menu_list:
                menu_dict_list.append(menu.to_dict_list())
            return {'status':200,'msg':'获取list菜单成功','menus':menu_dict_list}   


menu_api.add_resource(Menus, '/menus/')

