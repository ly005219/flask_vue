from flask import request, jsonify, make_response
from flask_shop.role import role_api,role_bp
from flask_restful import Resource
from flask_shop import models
from flask_restful import reqparse
from flask_shop.utils.redis_cache import (
    cache_with_key, clear_cache_by_prefix, 
    cache_update_with_delay_double_deletion
)


class Roles(Resource):
    """
    角色列表资源
    """

    @cache_with_key("roles_list", ttl=86400)  # 缓存24小时
    def get(self):
        """获取角色列表"""
        try:
            roles = models.Role.query.all()
            role_list = [role.to_dict() for role in roles]
            return {
                'status': 200,
                'msg': '角色列表获取成功',
                'roles_data': role_list
            }
        except Exception as e:
            print(f"获取角色列表错误: {str(e)}")
            return {'status': 500, 'msg': '角色列表获取失败', 'error': str(e)}
    
    # 使用延迟双删策略处理缓存
    @cache_update_with_delay_double_deletion(['roles_list'], delay=1.0)
    def post(self):
        """添加角色"""
        try:
            role=models.Role.query.filter_by(name=request.get_json().get('name')).first()
            if role:
                return {'status':400,'msg':'角色已存在'}
            else:
                name=request.get_json().get('name')
                desc=request.get_json().get('desc')
                if not all([name,desc]):
                    return {'status':400,'msg':'角色列表参数不完整'}
                else:
                    role=models.Role(name=name,desc=desc)
                    models.db.session.add(role)
                    models.db.session.commit()
                    
                    return {'status':200,'msg':'角色添加成功'}
        except Exception as e:
            return {'status':500,'msg':'角色添加失败'}
        

role_api.add_resource(Roles, '/roles/')


class Role(Resource):
    # 使用延迟双删策略处理缓存
    @cache_update_with_delay_double_deletion(['roles_list'], delay=1.0)
    def delete(self,id):
        """删除角色"""
        try:
            role=models.Role.query.get(id)
            models.db.session.delete(role)
            models.db.session.commit()
            
            return {'status':200,'msg':'角色删除成功'}
        except Exception as e:
            return {'status':500,'msg':'角色删除失败'}
        
    # 使用延迟双删策略处理缓存
    @cache_update_with_delay_double_deletion(['roles_list'], delay=1.0)
    def put(self,id):
        """修改角色"""
        try:
            role=models.Role.query.get(id)
            #创建RequestParser对象，用来解析请求参数
            parser=reqparse.RequestParser()
            #添加参数
            parser.add_argument('name',type=str,required=True,help='角色名称不能为空')
            parser.add_argument('desc',type=str,required=True,help='角色描述不能为空')
            #解析参数
            args=parser.parse_args()
            #更新角色信息
            if not all([args.get('name'),args.get('desc')]):
                return {'status':400,'msg':'角色列表参数不完整'}
            else:
                role.name=args.get('name')
                role.desc=args.get('desc')
                models.db.session.commit()
                
                return {'status':200,'msg':'角色修改成功'}
        except Exception as e:
            return {'status':500,'msg':'角色修改失败'}

role_api.add_resource(Role, '/role/<int:id>/')


# 使用延迟双删策略处理缓存
@role_bp.route('/role/<int:role_id>/<int:menu_id>/')
@cache_update_with_delay_double_deletion(['roles_list', 'role_menus'], delay=1.0)
def delete_menu_permission(role_id,menu_id):
    """删除指定的menu的权限"""
    #查找当前的角色信息
    role=models.Role.query.get(role_id)
    #查找当前的菜单信息
    memu=models.Menu.query.get(menu_id)

    #判断当前角色与当前菜单是否存在关系
    if all([role,memu]):
        #判断当前菜单是否存在于当前角色的权限列表中
        if memu in role.menus:
            #删除当前角色的菜单权限
            role.menus.remove(memu)
            #判断当前菜单是不是父级菜单
            if memu.level==1:
                #删除当前菜单的子菜单权限
                for child in memu.children:
                    if child in role.menus:
                        role.menus.remove(child)
                  
            models.db.session.commit()
            
            return {'status':200,'msg':'角色删除菜单权限成功'}
        else:
            return {'status':400,'msg':'当前菜单不存在于当前角色的权限列表中'}
    else:
        return {'status':400,'msg':'角色或菜单不存在'}


# 添加缓存获取角色菜单列表的函数
@cache_with_key("role_menus", ttl=86400)  # 缓存24小时
def get_role_menus(role_id):
    """获取指定角色的菜单列表，支持缓存"""
    role = models.Role.query.get(role_id)
    if not role:
        return {'status': 404, 'msg': '角色不存在'}
    
    return {
        'status': 200,
        'msg': '获取角色菜单成功',
        'data': role.get_menus_dict()
    }


@role_bp.route('/role/menus/<int:role_id>/')
def get_role_menu_list(role_id):
    """获取指定角色的菜单列表API，通过缓存函数获取"""
    return get_role_menus(role_id)


# 使用延迟双删策略处理缓存
@role_bp.route('/role/<int:role_id>/',methods=['POST'])
@cache_update_with_delay_double_deletion(['roles_list', 'role_menus'], delay=1.0)
def set_menu(role_id:int):
    """设置角色的菜单权限"""
    try:
        role=models.Role.query.get(role_id)
        #获取当前角色的菜单列表
        menus_id=request.get_json().get('menu_id')
        #清空当前角色的所有权限
        role.menus=[]
        #遍历菜单列表
        menus_id=menus_id.split(',')
        for mid in menus_id:
            if mid:
                #查找当前菜单信息
                menu=models.Menu.query.get(int(mid))
                role.menus.append(menu)
            
        #保存到数据库
        models.db.session.commit()
        
        return {'status':200,'msg':'角色分配菜单权限成功'}

    except Exception as e:
        return {'status':500,'msg':'角色分配菜单权限失败'}
