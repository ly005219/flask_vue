from flask import request, current_app, send_from_directory, url_for
from flask_shop.user import user_bp,user_api

from flask_shop import models,db
from flask_restful import Resource,reqparse
import re
import os
from werkzeug.utils import secure_filename

from flask_shop.utils.jwt_token import generate_token,login_required



# #db用于操作数据库
# from flask_shop import db
#创建视图
@user_bp.route('/')
def index():
    return 'user index'

class UserReigster(Resource):


    def get(self):
        #创建RequestParser对象，用于解析请求参数
        parser=reqparse.RequestParser()
        #添加参数
        parser.add_argument('page',type=int,default=1,location='args')
        parser.add_argument('page_size',type=int,default=2,location='args')
        parser.add_argument('username',type=str,location='args')
        #解析参数
        args=parser.parse_args()
        #获取数据
        page=args.get('page')
        page_size=args.get('page_size')
        username=args.get('username')

        if username:
            userlist=models.User.query.filter(models.User.username.like(f'%{username}%')).paginate(page=page,per_page=page_size)#后面两个参数是分页
        else:
            userlist=models.User.query.paginate(page=page,per_page=page_size)

        data={
            'total':userlist.total,
            'page':page,
            'page_size':page_size,
            'data':[u.to_dict() for u in userlist.items]
        


        }
        return {'status':200,'msg':'获取用户列表成功','data':data}

 
    def post(self):
        username=request.get_json().get('username')
        pwd=request.get_json().get('pwd')
        email=request.get_json().get('email')
        nick_name=request.get_json().get('nick_name')
        phone=request.get_json().get('phone')
        real_pwd=request.get_json().get('real_pwd')
        if not all([username,pwd,real_pwd]):
             return {'status':400,'msg':'参数不完整'}
        else:
            if len(pwd)<6 or len(pwd)>20:
                return {'status':400,'msg':'密码长度不能小于6,也不能大于20'}
            if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
                return {'status':400,'msg':'邮箱格式不正确'}
            if not re.match(r'^1[3-9]\d{9}$',phone):
                return {'status':400,'msg':'手机号格式不正确'}
        #接收角色id信息
        role_id=request.get_json().get('role_id')

        



        try:
            user=models.User.query.filter(models.User.username==username).first()
            if user:
                return {'status':400,'msg':'用户名已存在'}
          
            # 验证手机号是否存在
            check_phone_response = check_phone()
            if check_phone_response['status'] == 400:
                return check_phone_response
            # 验证邮箱是否存在
            check_email_response = check_email()
            if check_email_response['status'] == 400:
                return check_email_response
        except Exception as e:
            return f'status:500------->msg:{e}'
         
        if real_pwd==pwd:
            if not role_id:
                new_user=models.User(username=username,password=pwd,email=email,nick_name=nick_name,phone=phone)
            else:
                new_user=models.User(username=username,password=pwd,email=email,nick_name=nick_name,phone=phone,role_id=role_id)
                
            
            db.session.add(new_user)
            db.session.commit()
            return {'status':200,'msg':'注册成功'}
        else:
            return {'status':400,'msg':'两次密码不一致'}
       

       



user_api.add_resource(UserReigster, '/register/')
from datetime import datetime

#登录功能
@user_bp.route('/login/', methods=[ 'POST'])
def login():

    name=request.get_json().get('username')
    pwd=request.get_json().get('pwd')


    if not all([name, pwd]):

        return {'status':400,'msg':'参数不完整'}
    
    else:
        user=models.User.query.filter(models.User.username==name).first()
        if not user:
            return {'status':400,'msg':'用户不存在'}
        else:
            if user.check_password(pwd):
                            # 更新最后登录时间
                user.last_login = datetime.now()
                db.session.commit()
                #生产token
                token=generate_token({'id':user.id})
                

                return {'status':200,'msg':'登录成功','data':{'token':token}}


              
            else:
                return {'status':400,'msg':'密码错误'}

class User(Resource):

    def get(self,id):
        user=models.User.query.get(id)
        if user:
            return {'status':200,'msg':'获取成功','data':user.to_dict()}
        else:
            return {'status':400,'msg':'用户不存在'}

    def put(self, id):
        # 尝试获取用户
        user = models.User.query.get(id)
        if not user:

            return {'status': 404, 'msg': '用户未找到修改失败'}

        # 创建RequestParser对象，用于解析请求参数
        parser = reqparse.RequestParser()
        # 添加参数
        parser.add_argument('nick_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('role_id', type=int)
        
        # 解析参数
        args = parser.parse_args()
        
        # 获取数据
        if args.get('nick_name'):
            user.nick_name = args.get('nick_name')
        if args.get('email'):
            user.email = args.get('email')
        if args.get('phone'):
            user.phone = args.get('phone')
        if args.get('role_id'):
            user.role_id = args.get('role_id')

        # 提交更改
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'status': 500, 'msg': '更新失败'}

        return {'status': 200, 'msg': '修改成功', 'data': user.to_dict()}

    def delete(self,id):
            # 尝试获取用户
        try:
            user = models.User.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
            return {'status': 200, 'msg': '删除成功'}#不管有没有找到用户，都返回200，这样就让别人不知道我们是真的删除了还是假的，可以保证安全
        except Exception as e:
            return {'status': 500, 'msg': '删除失败', 'error': str(e)}
           

user_api.add_resource(User, '/user/<int:id>/')


@user_bp.route('/reset_pwd/<int:id>/')
def reset_pwd(id):
    try:
        user = models.User.query.get(id)
        if user:
            user.password = '123456'
            db.session.commit()
            return {'status': 200, 'msg': '重置密码成功,密码为123456', 'data': user.to_dict(),'pwd':user.password}
        else:
            return {'status': 404, 'msg': '用户未找到'}
    except Exception as e:
        return {'status': 500, 'msg': '重置密码失败', 'error': str(e)}




@user_bp.route('/test_login/')
@login_required
def test_login():
    return {'status':200,'msg':'token验证成功'}



#验证邮箱是否存在
@user_bp.route('/check_email/',methods=['POST'])
def check_email():

    email=request.get_json().get('email')
    check_email=models.User.query.filter(models.User.email==email).first()
    if check_email:
        return {'status':400,'msg':'邮箱已存在'}
    else:
        return {'status':200,'msg':'邮箱可用'}


#验证手机号是否存在
@user_bp.route('/check_phone/',methods=['POST'])
def check_phone():

    phone=request.get_json().get('phone')
    check_phone=models.User.query.filter(models.User.phone==phone).first()
    if check_phone:
        return {'status':400,'msg':'手机号已存在'}
    else:
        return {'status':200,'msg':'手机号可用'}

# 添加获取默认头像的路由
@user_bp.route('/default_avatar/')
def default_avatar():
    """返回一个默认的Base64编码头像数据"""
    # 这是一个简单的Base64编码的1x1像素透明PNG图片
    default_avatar_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    return {'status': 200, 'msg': 'success', 'data': {'avatar': default_avatar_data}}
    
@user_bp.route('/last_login/')
def user_last_login():
    # 获取查询参数中的用户名
    username = request.args.get('username')
    if not username:
        return {'status': 400, 'msg': '缺少用户名参数'}
    
    try:
        # 从数据库查询用户
        user = models.User.query.filter_by(username=username).first()
        if not user:
            return {'status': 404, 'msg': '用户不存在'}
            
        # 获取最后登录时间
        last_login = user.last_login
        if last_login:
            # 格式化时间为字符串
            last_login_str = last_login.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_login_str = None
            
        return {
            'status': 200,
            'msg': 'success',
            'data': {
                'last_login': last_login_str
            }
        }
        
    except Exception as e:
        print(f"获取登录时间错误: {str(e)}")
        return {'status': 500, 'msg': '服务器内部错误'}

# 用于检查上传文件是否为允许的图片类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 添加上传头像接口
@user_bp.route('/upload_avatar/', methods=['POST'])
@login_required
def upload_avatar():
    user_id = request.current_user.get('id')
    if not user_id:
        return {'status': 401, 'msg': '未登录或 token 已过期'}
    
    try:
        # 从数据库查询用户
        user = models.User.query.get(user_id)
        if not user:
            return {'status': 404, 'msg': '用户不存在'}
        
        # 检查请求中是否有文件
        if 'avatar' not in request.files:
            return {'status': 400, 'msg': '未上传文件'}
        
        file = request.files['avatar']
        if file.filename == '':
            return {'status': 400, 'msg': '未选择文件'}
        
        if file and allowed_file(file.filename):
            # 安全处理文件名
            filename = secure_filename(f"avatar_{user_id}_{file.filename}")
            # 确保头像目录存在
            avatar_dir = os.path.join(current_app.static_folder, 'avatar')
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)
            
            # 保存文件
            file_path = os.path.join(avatar_dir, filename)
            file.save(file_path)
            
            # 更新用户头像路径
            avatar_url = f'/static/avatar/{filename}'
            user.avatar = avatar_url
            db.session.commit()
            
            return {'status': 200, 'msg': '头像上传成功', 'data': {'avatar': avatar_url}}
        
        return {'status': 400, 'msg': '不支持的文件类型'}
        
    except Exception as e:
        print(f"上传头像错误: {str(e)}")
        return {'status': 500, 'msg': '服务器内部错误'}

@user_bp.route('/info/')
@login_required
def get_user_info():
    # 从 token 中获取用户 ID
    user_id = request.current_user.get('id')
    if not user_id:
        return {'status': 401, 'msg': '未登录或 token 已过期'}
    
    try:
        # 从数据库查询用户
        user = models.User.query.get(user_id)
        if not user:
            return {'status': 404, 'msg': '用户不存在'}
        
        # 获取用户信息，确保包括角色名称和其他信息
        user_data = user.to_dict()
        
        return {
            'status': 200,
            'msg': 'success',
            'data': user_data
        }
    except Exception as e:
        print(f"获取用户信息错误: {str(e)}")
        return {'status': 500, 'msg': '服务器内部错误'}