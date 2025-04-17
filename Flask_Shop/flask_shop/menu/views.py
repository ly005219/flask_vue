from flask_shop.menu import menu_api,menu_bp
from flask_restful import Resource
from flask_shop import models
from flask import request, jsonify
from flask_shop.utils.redis_cache import (
    cache_with_key, clear_cache_by_prefix,
    cache_update_with_delay_double_deletion
)
from flask_shop.utils.jwt_token import login_required


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


@menu_bp.route('/api/menus/user_menus', methods=['GET'])
@login_required
def get_user_menus():
    """获取当前用户的菜单权限"""
    try:
        # 从session中获取用户ID
        user_id = request.user.id
        
        # 获取用户对象
        user = models.User.query.get(user_id)
        if not user:
            return jsonify({'status': 404, 'msg': '用户不存在'})
            
        # 获取用户的角色
        role = user.role
        if not role:
            return jsonify({'status': 403, 'msg': '用户没有分配角色'})
            
        # 获取角色的菜单权限
        menus = role.get_menus_dict()
        
        # 构建树形结构
        menu_tree = []
        menu_map = {}
        
        # 首先创建一个以id为键的字典
        for menu in menus:
            menu['hasChildren'] = False
            menu['children'] = []
            menu_map[menu['id']] = menu
            
        # 构建树形结构
        for menu in menus:
            if not menu['parent_id']:  # 如果是顶级菜单
                menu_tree.append(menu)
            else:
                # 这是一个子菜单，将其添加到父菜单的children列表中
                parent = menu_map.get(menu['parent_id'])
                if parent:
                    parent['hasChildren'] = True
                    parent['children'].append(menu)
        
        # 按照level和id排序
        menu_tree.sort(key=lambda x: (x['level'], x['id']))
        for menu in menu_tree:
            if menu['children']:
                menu['children'].sort(key=lambda x: (x['level'], x['id']))
        
        return jsonify({
            'status': 200,
            'msg': '获取成功',
            'data': menu_tree
        })
        
    except Exception as e:
        print(f"获取用户菜单失败: {str(e)}")
        return jsonify({'status': 500, 'msg': '获取用户菜单失败'})


@menu_bp.route('/api/user/permissions', methods=['GET'])
@login_required
def get_current_user_permissions():
    """获取当前登录用户的菜单权限"""
    try:
        # 从token中获取用户ID
        user_id = request.current_user.get('id')
        if not user_id:
            return jsonify({'status': 401, 'msg': '未登录或token已过期'})
            
        # 获取用户对象
        user = models.User.query.get(user_id)
        if not user:
            return jsonify({'status': 404, 'msg': '用户不存在'})
            
        # 获取用户的角色
        role = user.role
        if not role:
            return jsonify({'status': 403, 'msg': '用户没有分配角色'})
            
        # 获取角色信息和菜单权限
        role_info = {
            'id': role.id,
            'name': role.name,
            'desc': role.desc
        }
        
        # 获取角色的菜单权限
        menus = role.get_menus_dict()
        
        return {
            'status': 200,
            'msg': '获取权限成功',
            'data': {
                'role': role_info,
                'menus': menus
            }
        }
    
    except Exception as e:
        print(f"获取用户权限失败: {str(e)}")
        return {'status': 500, 'msg': f'获取用户权限失败: {str(e)}'}

