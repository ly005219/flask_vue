from flask import request, current_app, send_from_directory, url_for, render_template, redirect
from flask_shop.user import user_bp,user_api
from flask_shop import models,db
from flask_restful import Resource,reqparse
import re
import os
import time
import hashlib
import uuid
import io
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
from werkzeug.utils import secure_filename

from flask_shop.utils.jwt_token import generate_token,login_required

import json

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

# 用于生成唯一且安全的文件名
def generate_unique_filename(user_id, original_filename):
    """
    生成唯一的文件名，格式为：md5(时间戳 + 用户ID + 随机字符串) + 原始扩展名
    
    参数:
        user_id: 用户ID
        original_filename: 原始文件名，用于获取扩展名
    
    返回:
        唯一的文件名
    """
    # 获取文件扩展名
    if '.' in original_filename:
        file_ext = original_filename.rsplit('.', 1)[1].lower()
    else:
        file_ext = 'jpg'  # 默认扩展名
    
    # 生成唯一标识
    timestamp = str(int(time.time()))
    random_str = str(uuid.uuid4().hex)
    
    # 组合源字符串
    source = f"{timestamp}_{user_id}_{random_str}"
    
    # 计算MD5哈希
    md5 = hashlib.md5(source.encode()).hexdigest()
    
    # 返回最终文件名
    return f"{md5}.{file_ext}"

# 图像增强和过滤器函数
def apply_filter(img, filter_type, intensity=0.5):
    """
    应用各种图像过滤器
    
    参数:
        img: PIL图像对象
        filter_type: 过滤器类型 ('sepia', 'blur', 'sharpen', 'bw', 'brightness', 'contrast')
        intensity: 过滤器强度 (0.0-1.0)
    
    返回:
        处理后的PIL图像对象
    """
    if filter_type == 'sepia':
        # 棕褐色滤镜
        img = img.convert('RGB')
        data = np.array(img)
        data = data.astype(np.float64)
        data = np.clip(data * np.array([1 - intensity * 0.5 + intensity * 0.6, 
                                        1 - intensity * 0.1, 
                                        1 - intensity * 0.5]), 0, 255).astype(np.uint8)
        return Image.fromarray(data)
    
    elif filter_type == 'blur':
        # 模糊效果
        radius = int(intensity * 5)  # 最大模糊半径5
        return img.filter(ImageFilter.GaussianBlur(radius=radius))
    
    elif filter_type == 'sharpen':
        # 锐化效果
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(1 + intensity * 2)  # 1-3范围
    
    elif filter_type == 'bw':
        # 黑白效果
        img = img.convert('RGB')
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(1 - intensity)  # 逐渐降低颜色饱和度
    
    elif filter_type == 'brightness':
        # 亮度调整
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(0.5 + intensity)  # 0.5-1.5范围
    
    elif filter_type == 'contrast':
        # 对比度调整
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(0.5 + intensity)  # 0.5-1.5范围
    
    return img  # 如果没有匹配的过滤器，返回原始图像

# 人脸检测与智能裁剪
def smart_crop(img, target_size, face_detection=True):
    """
    智能裁剪，如果启用人脸检测且识别到人脸，则将人脸居中
    否则使用内容感知裁剪或标准居中裁剪
    
    参数:
        img: PIL图像对象
        target_size: (宽, 高) - 目标尺寸
        face_detection: 是否启用人脸检测
        
    返回:
        裁剪后的PIL图像对象
    """
    # 获取原始尺寸
    width, height = img.size
    target_width, target_height = target_size
    
    # 计算裁剪比例
    width_ratio = target_width / width
    height_ratio = target_height / height
    
    # 如果图像比例已经匹配，只需调整大小
    if abs(width_ratio - height_ratio) < 0.1:
        return img.resize(target_size, Image.LANCZOS)
    
    # 如果启用人脸检测且OpenCV可用，尝试检测人脸
    if face_detection and CV2_AVAILABLE:
        try:
            # 转换PIL图像为OpenCV格式
            cv_img = np.array(img.convert('RGB'))
            cv_img = cv_img[:, :, ::-1].copy()  # RGB到BGR
            
            # 加载人脸检测器 (使用预训练的Haar级联分类器)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # 检测人脸
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # 如果检测到人脸
            if len(faces) > 0:
                # 使用最大的人脸（假设是主体）
                face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = face
                
                # 确定裁剪区域，以人脸为中心
                face_center_x = x + w // 2
                face_center_y = y + h // 2
                
                # 计算新的裁剪区域
                if width_ratio > height_ratio:
                    # 保持高度，裁剪宽度
                    new_width = int(height * target_width / target_height)
                    left = max(0, min(face_center_x - new_width // 2, width - new_width))
                    img = img.crop((left, 0, left + new_width, height))
                else:
                    # 保持宽度，裁剪高度
                    new_height = int(width * target_height / target_width)
                    top = max(0, min(face_center_y - new_height // 2, height - new_height))
                    img = img.crop((0, top, width, top + new_height))
                
                # 调整大小
                return img.resize(target_size, Image.LANCZOS)
        except Exception as e:
            print(f"Face detection error: {e}")
            # 如果人脸检测失败，返回标准裁剪
    
    # 默认居中裁剪
    if width_ratio > height_ratio:
        # 保持高度，裁剪宽度
        new_width = int(height * target_width / target_height)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        # 保持宽度，裁剪高度
        new_height = int(width * target_height / target_width)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))
    
    # 调整大小
    return img.resize(target_size, Image.LANCZOS)

# 分析图像复杂度
def analyze_image_complexity(img):
    """
    分析图像复杂度并返回0到1之间的值
    较复杂的图像(细节多、边缘多)应使用更高的质量，简单图像可以使用更低的质量
    
    参数:
        img: PIL图像对象
    
    返回:
        复杂度评分(0-1)，1表示最复杂
    """
    # 转换为灰度图以便处理
    if img.mode != 'L':
        gray_img = img.convert('L')
    else:
        gray_img = img
        
    # 转换为numpy数组
    img_array = np.array(gray_img)
    
    # 1. 计算图像梯度 - 使用Sobel算子
    if CV2_AVAILABLE:
        # OpenCV梯度检测
        sobelx = cv2.Sobel(img_array, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img_array, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    else:
        # 使用简单的差分代替Sobel
        gradient_x = np.diff(img_array, axis=1)
        gradient_y = np.diff(img_array, axis=0)
        # 补齐形状
        gradient_x = np.pad(gradient_x, ((0, 0), (0, 1)), mode='constant')
        gradient_y = np.pad(gradient_y, ((0, 1), (0, 0)), mode='constant')
        gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # 2. 计算图像的熵(信息量)
    histogram = np.histogram(img_array, bins=256, range=(0, 256))[0]
    histogram = histogram / np.sum(histogram)
    non_zero_hist = histogram[histogram > 0]
    entropy = -np.sum(non_zero_hist * np.log2(non_zero_hist))
    max_entropy = np.log2(256)  # 理论最大熵
    normalized_entropy = entropy / max_entropy
    
    # 3. 计算边缘密度
    edge_density = np.sum(gradient_magnitude > 30) / gradient_magnitude.size
    
    # 4. 计算标准差(对比度指标)
    std_dev = np.std(img_array) / 128  # 归一化
    
    # 5. 人脸检测 - 如果检测到人脸，增加复杂度权重
    face_weight = 0
    if CV2_AVAILABLE:
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(img_array, 1.1, 4)
            if len(faces) > 0:
                # 人脸占图像比例
                face_area = sum([w * h for (x, y, w, h) in faces])
                total_area = img_array.shape[0] * img_array.shape[1]
                face_ratio = face_area / total_area
                face_weight = min(0.3, face_ratio * 2)  # 最多增加0.3的权重
        except Exception as e:
            print(f"Face detection error in complexity analysis: {e}")
    
    # 组合以上指标得到最终复杂度评分
    # 边缘密度、熵和标准差共同影响图像的复杂度
    complexity = (
        0.4 * normalized_entropy +  # 熵权重
        0.3 * edge_density +        # 边缘密度权重
        0.2 * std_dev +             # 标准差权重
        0.1 + face_weight           # 基础值和人脸权重
    )
    
    # 确保值在0-1范围内
    complexity = max(0, min(1, complexity))
    
    # 记录日志便于调试
    print(f"Image complexity: {complexity:.4f} (entropy: {normalized_entropy:.4f}, "
          f"edge: {edge_density:.4f}, std: {std_dev:.4f}, face: {face_weight:.4f})")
    
    return complexity

# 自适应质量压缩
def adaptive_quality_compression(img, min_quality=60, max_quality=95, target_size_kb=None):
    """
    根据图像复杂度自适应调整压缩质量
    
    参数:
        img: PIL图像对象
        min_quality: 最低质量值
        max_quality: 最高质量值
        target_size_kb: 目标文件大小(KB)，如果指定会尝试达到此大小
        
    返回:
        (压缩后的图像字节数据, 使用的质量值)
    """
    # 分析图像复杂度
    complexity = analyze_image_complexity(img)
    
    # 根据复杂度计算初始质量值
    initial_quality = int(min_quality + complexity * (max_quality - min_quality))
    
    # 如果没有指定目标大小，直接使用计算出的质量值
    if target_size_kb is None:
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=initial_quality, optimize=True)
        output.seek(0)
        return output, initial_quality
    
    # 二分搜索找到接近目标大小的质量值
    target_bytes = target_size_kb * 1024
    low, high = min_quality, max_quality
    best_quality = initial_quality
    best_size = float('inf')
    best_output = None
    
    # 最多尝试8次二分搜索
    for _ in range(8):
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=best_quality, optimize=True)
        current_size = len(output.getvalue())
        
        # 更新最佳结果
        if abs(current_size - target_bytes) < abs(best_size - target_bytes):
            best_size = current_size
            best_output = output
            
        # 调整质量值
        if current_size > target_bytes * 1.1:  # 当前大小超过目标10%
            high = best_quality - 1
        elif current_size < target_bytes * 0.9:  # 当前大小低于目标10%
            low = best_quality + 1
        else:
            # 在目标范围内，接受这个结果
            break
            
        # 计算新的质量值
        best_quality = (low + high) // 2
        
        # 如果搜索范围变得很小，跳出循环
        if low > high:
            break
    
    best_output.seek(0)
    return best_output, best_quality

# 扩展的头像处理接口
@user_bp.route('/process_avatar/', methods=['POST'])
@login_required
def process_avatar():
    """
    高级头像处理API，支持自适应质量和多种图像处理操作
    支持的参数:
    - image: 要处理的图像文件
    - crop_data: JSON格式的裁剪数据，包含 {x, y, width, height}
    - rotate: 旋转角度
    - format: 输出格式(JPEG, PNG, WebP)
    - target_kb: 目标文件大小(KB)
    - filter: 滤镜类型
    - filter_intensity: 滤镜强度
    """
    user_id = request.current_user.get('id')
    if not user_id:
        return {'status': 401, 'msg': '未登录或token已过期'}
    
    try:
        # 验证文件
        if 'image' not in request.files:
            return {'status': 400, 'msg': '未上传文件'}
        
        file = request.files['image']
        if file.filename == '':
            return {'status': 400, 'msg': '未选择文件'}
        
        if not allowed_file(file.filename):
            return {'status': 400, 'msg': '不支持的文件类型'}
        
        # 打开图像
        img = Image.open(file)
        
        # 处理裁剪（前端传入的裁剪数据）
        crop_data = request.form.get('crop_data')
        if crop_data:
            try:
                crop = json.loads(crop_data)
                if all(k in crop for k in ['x', 'y', 'width', 'height']):
                    # 执行裁剪
                    img = img.crop((
                        int(crop['x']),
                        int(crop['y']),
                        int(crop['x'] + crop['width']),
                        int(crop['y'] + crop['height'])
                    ))
            except Exception as e:
                print(f"裁剪错误: {e}")
                return {'status': 400, 'msg': f'裁剪数据格式错误: {str(e)}'}
        
        # 处理旋转
        rotate = request.form.get('rotate')
        if rotate:
            try:
                angle = float(rotate)
                # 执行旋转(保留原始尺寸)
                img = img.rotate(angle, expand=False, resample=Image.BICUBIC)
            except Exception as e:
                print(f"旋转错误: {e}")
                return {'status': 400, 'msg': f'旋转处理错误: {str(e)}'}
        
        # 处理调整大小
        size = int(request.form.get('size', 400))  # 默认大小400px
        # 等比例调整到指定大小
        img.thumbnail((size, size), Image.LANCZOS)
        
        # 应用滤镜
        filter_type = request.form.get('filter')
        filter_intensity = float(request.form.get('filter_intensity', 0.5))
        if filter_type and filter_type != 'none':
            img = apply_filter(img, filter_type, filter_intensity)
        
        # 确定输出格式
        format_option = request.form.get('format', 'JPEG').upper()
        format_to_ext = {
            'JPEG': 'jpg',
            'PNG': 'png',
            'WEBP': 'webp'
        }
        output_format = format_option if format_option in format_to_ext else 'JPEG'
        ext = format_to_ext.get(output_format, 'jpg')
        
        # 处理模式转换
        if output_format == 'JPEG' and img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        elif output_format == 'WebP' and img.mode == 'RGBA' and 'transparency' not in img.info:
            img = img.convert('RGB')
        
        # 自适应质量压缩
        target_kb = request.form.get('target_kb')
        if target_kb:
            try:
                target_kb = int(target_kb)
                compressed_file, used_quality = adaptive_quality_compression(
                    img, 
                    min_quality=60, 
                    max_quality=95, 
                    target_size_kb=target_kb
                )
            except Exception as e:
                print(f"自适应压缩错误: {e}")
                # 使用默认质量
                compressed_file = io.BytesIO()
                used_quality = 85
                if output_format == 'JPEG':
                    img.save(compressed_file, format=output_format, quality=used_quality, optimize=True)
                elif output_format == 'PNG':
                    img.save(compressed_file, format=output_format, optimize=True)
                elif output_format == 'WEBP':
                    img.save(compressed_file, format=output_format, quality=used_quality, method=6)
                else:
                    img.save(compressed_file, format=output_format)
                compressed_file.seek(0)
        else:
            # 使用预设质量
            quality = int(request.form.get('quality', 85))
            compressed_file = io.BytesIO()
            used_quality = quality
            if output_format == 'JPEG':
                img.save(compressed_file, format=output_format, quality=quality, optimize=True)
            elif output_format == 'PNG':
                img.save(compressed_file, format=output_format, optimize=True)
            elif output_format == 'WEBP':
                img.save(compressed_file, format=output_format, quality=quality, method=6)
            else:
                img.save(compressed_file, format=output_format)
            compressed_file.seek(0)
        
        # 如果只需要预览，则返回base64数据
        preview_only = request.form.get('preview', 'false').lower() == 'true'
        if preview_only:
            import base64
            image_data = base64.b64encode(compressed_file.getvalue()).decode('utf-8')
            mime_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"
            
            # 计算原文件大小（用于显示压缩比）
            file.seek(0)
            original_size = len(file.read())
            file.seek(0)
            
            # 计算压缩后大小
            compressed_size = len(compressed_file.getvalue())
            
            # 计算压缩比
            if original_size > 0:
                size_reduction = round((1 - compressed_size / original_size) * 100)
            else:
                size_reduction = 0
                
            return {
                'status': 200,
                'msg': '图像预览生成成功',
                'data': {
                    'preview': f"data:{mime_type};base64,{image_data}",
                    'original_size': original_size,
                    'compressed_size': compressed_size,
                    'size_reduction': f"{size_reduction}%",
                    'dimensions': f"{img.width}x{img.height}",
                    'quality_used': used_quality,
                    'format': output_format
                }
            }
        
        # 生成唯一文件名
        filename = generate_unique_filename(user_id, f"avatar.{ext}")
        
        # 确保头像目录存在
        avatar_dir = os.path.join(current_app.static_folder, 'avatar')
        if not os.path.exists(avatar_dir):
            os.makedirs(avatar_dir)
        
        # 保存处理后的文件
        file_path = os.path.join(avatar_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(compressed_file.getvalue())
        
        # 保存原始图像供将来使用
        original_dir = os.path.join(current_app.static_folder, 'avatar/originals')
        if not os.path.exists(original_dir):
            os.makedirs(original_dir)
            
        original_filename = f"orig_{filename}"
        original_path = os.path.join(original_dir, original_filename)
        file.seek(0)
        with open(original_path, 'wb') as f:
            f.write(file.read())
        
        # 如果需要，生成多种分辨率版本
        # generate_multiple_sizes = request.form.get('generate_multiple_sizes', 'false').lower() == 'true'
        # 默认生成多个分辨率版本
        sizes = [(200, 200), (400, 400)]
        resized_versions = {}
        
        for size_tuple in sizes:
            size_str = f"{size_tuple[0]}x{size_tuple[1]}"
            size_filename = f"{size_tuple[0]}_{filename}"
            size_path = os.path.join(avatar_dir, size_filename)
            
            # 调整大小并保存
            sized_img = img.copy()
            sized_img.thumbnail(size_tuple, Image.LANCZOS)
            
            if output_format == 'JPEG':
                sized_img.save(size_path, format=output_format, quality=used_quality, optimize=True)
            elif output_format == 'PNG':
                sized_img.save(size_path, format=output_format, optimize=True)
            elif output_format == 'WEBP':
                sized_img.save(size_path, format=output_format, quality=used_quality, method=6)
            else:
                sized_img.save(size_path, format=output_format)
                
            resized_versions[size_str] = f'/static/avatar/{size_filename}'
        
        # 更新用户头像路径
        user = models.User.query.get(user_id)
        
        # 删除用户之前的头像文件（如果存在且不是默认头像）
        if user.avatar and not user.avatar.startswith('data:'):
            old_avatar_path = os.path.join(current_app.root_path, 'static', user.avatar.lstrip('/static/'))
            if os.path.exists(old_avatar_path):
                try:
                    os.remove(old_avatar_path)
                except:
                    pass  # 忽略删除失败
        
        # 更新用户记录
        avatar_url = f'/static/avatar/{filename}'
        user.avatar = avatar_url
        db.session.commit()
        
        # 计算原文件大小
        file.seek(0)
        original_size = len(file.read())
        
        # 计算压缩后大小
        compressed_size = len(compressed_file.getvalue())
        
        # 计算压缩比
        if original_size > 0:
            size_reduction = round((1 - compressed_size / original_size) * 100)
        else:
            size_reduction = 0
            
        return {
            'status': 200,
            'msg': '头像处理成功',
            'data': {
                'avatar': avatar_url,
                'resized_versions': resized_versions,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'size_reduction': f"{size_reduction}%",
                'dimensions': f"{img.width}x{img.height}",
                'quality_used': used_quality,
                'format': output_format
            }
        }
    except Exception as e:
        print(f"处理头像错误: {str(e)}")
        return {'status': 500, 'msg': f'服务器内部错误: {str(e)}'}

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

# 用户资料页面路由
@user_bp.route('/profile/')
@login_required
def user_profile():
    """渲染用户资料页面"""
    user_id = request.current_user.get('id')
    if not user_id:
        return redirect(url_for('user.login'))
    
    try:
        # 查询用户数据
        user = models.User.query.get(user_id)
        if not user:
            return redirect(url_for('user.login'))
            
        # 将用户数据传递给模板
        user_data = user.to_dict()
        
        # 如果用户有角色，添加角色名称
        if user.role_id:
            role = models.Role.query.get(user.role_id)
            if role:
                user_data['role_name'] = role.name
        
        return render_template('user/profile.html', user=user_data)
        
    except Exception as e:
        print(f"渲染用户资料页面错误: {str(e)}")
        return redirect(url_for('user.login'))

# 用户头像编辑器页面
@user_bp.route('/profile/avatar-editor')
@login_required
def avatar_editor():
    """渲染头像编辑页面"""
    user_id = request.current_user.get('id')
    if not user_id:
        return redirect(url_for('user.login'))
    
    try:
        # 查询用户数据
        user = models.User.query.get(user_id)
        if not user:
            return redirect(url_for('user.login'))
            
        # 将用户数据传递给模板
        user_data = user.to_dict()
        
        # 渲染头像编辑器页面
        return render_template('user/avatar-editor.html', user=user_data)
        
    except Exception as e:
        print(f"渲染头像编辑器页面错误: {str(e)}")
        return redirect(url_for('user.login'))

# 基本头像上传接口
@user_bp.route('/upload_avatar/', methods=['POST'])
@login_required
def upload_avatar():
    """基本头像上传功能"""
    user_id = request.current_user.get('id')
    if not user_id:
        return {'status': 401, 'msg': '未登录或token已过期'}
    
    try:
        # 验证文件
        if 'avatar' not in request.files:
            return {'status': 400, 'msg': '未上传文件'}
        
        file = request.files['avatar']
        if file.filename == '':
            return {'status': 400, 'msg': '未选择文件'}
        
        if not allowed_file(file.filename):
            return {'status': 400, 'msg': '不支持的文件类型'}
        
        # 打开图像
        img = Image.open(file)
        
        # 调整图像大小
        img = smart_crop(img, (400, 400), face_detection=True)
        
        # 生成唯一文件名
        filename = generate_unique_filename(user_id, file.filename)
        
        # 确保头像目录存在
        avatar_dir = os.path.join(current_app.static_folder, 'avatar')
        if not os.path.exists(avatar_dir):
            os.makedirs(avatar_dir)
        
        # 保存处理后的文件
        file_path = os.path.join(avatar_dir, filename)
        img.save(file_path, quality=85, optimize=True)
        
        # 更新用户头像路径
        user = models.User.query.get(user_id)
        
        # 删除用户之前的头像文件（如果存在且不是默认头像）
        if user.avatar and not user.avatar.startswith('data:') and 'init.png' not in user.avatar:
            old_avatar_path = os.path.join(current_app.root_path, 'static', user.avatar.lstrip('/static/'))
            if os.path.exists(old_avatar_path):
                try:
                    os.remove(old_avatar_path)
                except:
                    pass  # 忽略删除失败
        
        # 更新用户记录
        avatar_url = f'/static/avatar/{filename}'
        user.avatar = avatar_url
        db.session.commit()
        
        return {
            'status': 200,
            'msg': '头像上传成功',
            'data': {
                'avatar': avatar_url
            }
        }
    except Exception as e:
        print(f"上传头像错误: {str(e)}")
        return {'status': 500, 'msg': f'服务器内部错误: {str(e)}'}