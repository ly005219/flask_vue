from flask_shop.menu import menu_api
from flask_restful import Resource
from flask_shop import models
from flask import request
from flask_shop.utils.redis_cache import (
    cache_with_key, clear_cache_by_prefix,
    cache_update_with_delay_double_deletion
)


class Menus(Resource):
    """菜单资源类"""
    
    @cache_with_key("menus", ttl=86400)  # 缓存24小时
    def get(self):
        """获取菜单列表"""
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
    
    @cache_update_with_delay_double_deletion(['menus', 'roles_list', 'role_menus'], delay=1.0)
    def post(self):
        """添加菜单"""
        try:
            data = request.get_json()
            name = data.get('name')
            path = data.get('path')
            level = data.get('level', 1)
            parent_id = data.get('parent_id')
            
            # 验证必填字段
            if not all([name, path]):
                return {'status': 400, 'msg': '菜单名称和路径不能为空'}
                
            # 检查菜单是否已存在
            if models.Menu.query.filter_by(name=name).first():
                return {'status': 400, 'msg': '菜单名称已存在'}
                
            # 创建菜单
            menu = models.Menu(
                name=name,
                path=path,
                level=level,
                parent_id=parent_id
            )
            
            models.db.session.add(menu)
            models.db.session.commit()
            
            return {'status': 200, 'msg': '添加菜单成功', 'data': menu.to_dict_list()}
            
        except Exception as e:
            models.db.session.rollback()
            print(f"添加菜单错误: {str(e)}")
            return {'status': 500, 'msg': f'添加菜单失败: {str(e)}'}


menu_api.add_resource(Menus, '/menus/')


# 单个菜单操作
class MenuResource(Resource):
    """单个菜单资源类"""
    
    @cache_with_key("menu_detail", ttl=86400)  # 缓存24小时
    def get(self, menu_id):
        """获取指定菜单"""
        try:
            menu = models.Menu.query.get(menu_id)
            if not menu:
                return {'status': 404, 'msg': '菜单不存在'}
                
            return {'status': 200, 'msg': '获取菜单成功', 'data': menu.to_dict_list()}
        except Exception as e:
            print(f"获取菜单错误: {str(e)}")
            return {'status': 500, 'msg': f'获取菜单失败: {str(e)}'}
    
    @cache_update_with_delay_double_deletion(['menus', 'menu_detail', 'roles_list', 'role_menus'], delay=1.0)
    def put(self, menu_id):
        """更新菜单"""
        try:
            menu = models.Menu.query.get(menu_id)
            if not menu:
                return {'status': 404, 'msg': '菜单不存在'}
                
            data = request.get_json()
            name = data.get('name')
            path = data.get('path')
            
            # 验证必填字段
            if not all([name, path]):
                return {'status': 400, 'msg': '菜单名称和路径不能为空'}
                
            # 检查名称是否已被其他菜单使用
            existing = models.Menu.query.filter_by(name=name).first()
            if existing and existing.id != menu_id:
                return {'status': 400, 'msg': '菜单名称已存在'}
                
            # 更新菜单
            menu.name = name
            menu.path = path
            
            # level和parent_id一般不建议修改，但如果提供了也可以更新
            if 'level' in data:
                menu.level = data['level']
            if 'parent_id' in data:
                menu.parent_id = data['parent_id']
                
            models.db.session.commit()
            
            return {'status': 200, 'msg': '更新菜单成功', 'data': menu.to_dict_list()}
            
        except Exception as e:
            models.db.session.rollback()
            print(f"更新菜单错误: {str(e)}")
            return {'status': 500, 'msg': f'更新菜单失败: {str(e)}'}
    
    @cache_update_with_delay_double_deletion(['menus', 'menu_detail', 'roles_list', 'role_menus'], delay=1.0)
    def delete(self, menu_id):
        """删除菜单"""
        try:
            menu = models.Menu.query.get(menu_id)
            if not menu:
                return {'status': 404, 'msg': '菜单不存在'}
                
            # 检查是否有子菜单
            children = models.Menu.query.filter_by(parent_id=menu_id).all()
            if children:
                return {'status': 400, 'msg': '该菜单下有子菜单，无法删除'}
                
            # 删除菜单
            models.db.session.delete(menu)
            models.db.session.commit()
            
            return {'status': 200, 'msg': '删除菜单成功'}
            
        except Exception as e:
            models.db.session.rollback()
            print(f"删除菜单错误: {str(e)}")
            return {'status': 500, 'msg': f'删除菜单失败: {str(e)}'}


menu_api.add_resource(MenuResource, '/menu/<int:menu_id>/')

