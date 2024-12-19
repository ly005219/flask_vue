from flask import request
from flask_shop.role import role_api,role_bp
from flask_restful import Resource
from flask_shop import models
from flask_restful import reqparse


class Roles(Resource):
    """
    角色列表资源
    """

    def get(self):
        try:
            roles=models.Role.query.all()#这个roles里面就可以获取到Role模型的所有数据和方法to_dict()
            role_list=[role.to_dict() for role in roles]
            return {'status':200,'msg':'角色列表获取成功','roles_data':role_list}
        except Exception as e:
            return {'status':500,'msg':'角色列表获取失败','error':str(e)}
    
    #添加角色
    def post(self):
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
        #删除角色
    def delete(self,id):
        try:
            
            role=models.Role.query.get(id)
            # if role:
            models.db.session.delete(role)
            models.db.session.commit()
            return {'status':200,'msg':'角色删除成功'}
            # else:
            #     return {'status':400,'msg':'角色不存在'}
        except Exception as e:
            return {'status':500,'msg':'角色删除失败'}
        #修改角色
    def put(self,id):
        # try:
        #     role=models.Role.query.get(id)
        #     if role:
        #         name=request.get_json().get('name')
        #         desc=request.get_json().get('desc')
        #         if not all([name,desc]):
        #             return {'status':400,'msg':'角色列表参数不完整'}
        #         else:
        #             role.name=name
        #             role.desc=desc
        #             models.db.session.commit()
        #             return {'status':200,'msg':'角色修改成功'}
        #     else:
        #         return {'status':400,'msg':'角色不存在'}
        # except Exception as e:
        #     return {'status':500,'msg':'角色修改失败'}

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


@role_bp.route('/role/<int:role_id>/<int:menu_id>/')
#删除指定的menu的权限
def delete_menu_permission(role_id,menu_id):

    #查找当前的角色信息
    role=models.Role.query.get(role_id)
    #查找当前的菜单信息
    memu=models.Menu.query.get(menu_id)
    # menu_ids = [menu.id for menu in role.menus]
    # print(menu_ids)  # 打印出所有菜单的 ID 列表

    '''
    ：当您访问 role.menus 时,SQLAlchemy 会自动查询这个中间表trm,返回与当前角色相关联的所有菜单实例。
    
    '''

    #判断当前角色与 当前菜单是否存在关系
    if all ([role,memu]) :
        #判断当前菜单是否存在于当前角色的权限列表中
        if memu in role.menus:# menus = db.relationship('Menu', secondary=trm,backref=('roles'))
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

@role_bp.route('/role/<int:role_id>/',methods=['POST'])
def set_menu(role_id:int):
    #查找当前的角色信息
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
              #判断当前菜单是否存在
                # if menu:
                #     #判断当前菜单是否为父级菜单
                #     if menu.level==1:
                #         #查找当前菜单的所有子菜单
                #         children=menu.children
                #         #将当前菜单及其子菜单添加到当前角色的权限列表中
                #         role.menus.append(menu)
                #         for child in children:
                #             role.menus.append(child)
                #     else:
                #         #将当前菜单添加到当前角色的权限列表中
                #         role.menus.append(menu)
                # else:
                #     return {'status':400,'msg':'菜单不存在'}    
            
        #保存到数据库
        models.db.session.commit()
        return {'status':200,'msg':'角色分配菜单权限成功'}

    except Exception as e:
        return {'status':500,'msg':'角色分配菜单权限失败'}
