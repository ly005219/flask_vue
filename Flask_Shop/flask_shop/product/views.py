from flask_shop.product import product_api,product_bp
from flask_restful import Resource,reqparse
from flask_shop import models,db
from flask import request,current_app
import hashlib
from time import time

class Products(Resource):
    def post(self):
        '''
        添加商品    
        '''
        try:
            #创建一个参数解析器
            parser = reqparse.RequestParser()
            #添加参数
            parser.add_argument('name', type=str, required=True, help='商品名称不能为空')
            parser.add_argument('price', type=float, help='商品价格不能为空')
            parser.add_argument('number', type=str,)
            parser.add_argument('content', type=str)
            parser.add_argument('weight', type=int)
            parser.add_argument('cid_one', type=int)
            parser.add_argument('cid_two', type=int)
            parser.add_argument('cid_three', type=int)

            parser.add_argument('pics', type=list, location='json')
            parser.add_argument('attrs_dynamic', type=list, location='json')
            parser.add_argument('attrs_static', type=list, location='json')
    
            
            #解析参数
            args = parser.parse_args()
            #创建商品对象
            product = models.Product(
                name=args.get('name'),
                price=args.get('price'),
                number=args.get('number'),
                introduce=args.get('content'),
                weight=args.get('weight'),
                cid_one=args.get('cid_one'),
                cid_two=args.get('cid_two'),
                cid_three=args.get('cid_three'),

            )
            #添加商品属性
            db.session.add(product)
            db.session.commit()
            #添加商品图片，用直接专门创建的模型
            for pic in args.get('pics'):
                pic=models.Picture(path=pic,product_id=product.id)
                db.session.add(pic)
            #添加商品属性
            for attr_dynamic in args.get('attrs_dynamic'):
                attr_dynamic=models.ProductAttr(product_id=product.id,attr_id=attr_dynamic.get('id'),value=','.join(attr_dynamic.get('value')),_type='dynamic')
                db.session.add(attr_dynamic)
            for attr_static in args.get('attrs_static'):
                attr_static=models.ProductAttr(product_id=product.id,attr_id=attr_static.get('id'),value=attr_static.get('value'),_type='static')
                db.session.add(attr_static)
            #提交数据
            db.session.commit()
            #返回结果
            return {'status':200,'msg':'添加商品成功'}
        except Exception as e:
            print(e)
            return {'status':500,'msg':'添加商品失败'}

        



    def get(self):
        '''
        商品查询
        '''
        try:
            #创建一个参数解析器
            parser = reqparse.RequestParser()
            #添加参数
            parser.add_argument('name', type=str, location='args')  # 商品名称搜索
            parser.add_argument('sort_by', type=str, location='args')  # 排序字段
            parser.add_argument('order', type=str, location='args')  # 排序方式
            parser.add_argument('min_price', type=float, location='args')  # 最低价格
            parser.add_argument('max_price', type=float, location='args')  # 最高价格
            parser.add_argument('state', type=int, location='args')  # 商品状态
            parser.add_argument('page', type=int, location='args', default=1)  # 页码
            parser.add_argument('per_page', type=int, location='args', default=10)  # 每页数量
            
            #解析参数
            args = parser.parse_args()
            
            # 构建基础查询
            query = models.Product.query
            
            # 按名称搜索
            if args.get('name'):
                query = query.filter(models.Product.name.like(f'%{args.get("name")}%'))
            
            # 按价格范围筛选
            if args.get('min_price') is not None:
                query = query.filter(models.Product.price >= args.get('min_price'))
            if args.get('max_price') is not None:
                query = query.filter(models.Product.price <= args.get('max_price'))
            
            # 按商品状态筛选
            if args.get('state') is not None:
                query = query.filter(models.Product.state == args.get('state'))
            
            # 排序
            valid_sort_fields = {'price', 'number', 'id'}  # 允许排序的字段
            sort_by = args.get('sort_by')
            if sort_by and sort_by in valid_sort_fields:
                sort_field = getattr(models.Product, sort_by)
                if args.get('order') == 'desc':
                    sort_field = sort_field.desc()
                query = query.order_by(sort_field)
            else:
                # 默认按ID排序
                query = query.order_by(models.Product.id.desc())
            
            # 分页
            page = max(1, args.get('page', 1))  # 确保页码至少为1
            per_page = min(100, max(1, args.get('per_page', 10)))  # 限制每页数量在1-100之间
            
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            # 构建响应数据
            data = {
                'total': pagination.total,
                'current_page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'items': [p.to_dict() for p in pagination.items]
            }
            
            return {'status': 200, 'msg': '获取商品列表成功', 'data': data}
            
        except Exception as e:
            print(f"获取商品列表错误: {str(e)}")
            return {'status': 500, 'msg': f'获取商品列表失败: {str(e)}'}




product_api.add_resource(Products, '/products/')



class Product(Resource):


    def delete(self, id):
        '''
        删除商品
        '''
        try:
            # 开启事务
            with db.session.begin():
                # 先删除商品关联的图片记录
                models.Picture.query.filter_by(product_id=id).delete()
                
                # 删除商品属性记录
                models.ProductAttr.query.filter_by(product_id=id).delete()
                
                # 删除SKU记录
                models.SKU.query.filter_by(product_id=id).delete()
                
                # 最后删除商品记录
                product = models.Product.query.get(id)
                if not product:
                    return {'status': 404, 'msg': '商品不存在'}
                
                db.session.delete(product)
                
            return {'status': 200, 'msg': '删除商品成功'}
            
        except Exception as e:
            db.session.rollback()
            print(f"删除商品错误: {str(e)}")
            return {'status': 500, 'msg': f'删除商品失败: {str(e)}'}
        
    def put(self, id):
        '''
    修改商品
    '''
    # 获取参数
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('price', type=float, required=False)
        parser.add_argument('number', type=int, required=False)
        parser.add_argument('state', type=int, required=False)

        args = parser.parse_args()

        # 根据id查询商品
        try:
            product = models.Product.query.get(id)
            
            # 检查商品是否存在
            if product is None:
                return {'status': 404, 'msg': '商品未找到'}

            # 修改商品信息
            if args.get('name') is not None:  # 只有当字段显式提供时才修改
                product.name = args.get('name')
            if args.get('price') is not None:
                product.price = args.get('price')
            if args.get('number') is not None:
                product.number = args.get('number')
            if args.get('state') is not None:  # 注意这里允许state为0
                product.state = args.get('state')

            # 提交数据
            models.db.session.commit()
            # 返回结果
            return {'status': 200, 'msg': '修改商品成功'}
        except Exception as e:
            print(e)
            return {'status': 500, 'msg': '修改商品失败'}




    

product_api.add_resource(Product, '/product/<int:id>/')

@product_bp.route('/upload_img/',methods=['POST'])
def upload_img():
    '''
    上传图片
    '''
    #获取图片
    img = request.files.get('img')
    #判断图片是否为空
    if not img:
        return {'status': 500, 'msg': '图片不存在'}
    #判断图片是否是能上传的类型
    if allowed_file(img.filename):
        #保存图片,根据时间戳的md5加密文件名,不会有重复的
        filename = md5_file() + '.' + img.filename.rsplit('.', 1)[1].lower()
        img.save(current_app.config['UPLOAD_FOLDER'] +'/' + filename)
        #返回图片路径
        data={
            'path':'/static/uploads/' + filename,
             'url':f'http://127.0.0.1:5000/static/uploads/{filename}' 
        }
        return {'status': 200, 'msg': '上传图片成功', 'data': data}
    else:
        return {'status': 500, 'msg': '图片格式不支持'}


def allowed_file(filename):
    '''
    判断文件是否是能上传的类型
    '''
    # if  '.' in filename:
    #     #获取文件的后缀
    #     suffix = filename.split('.')[-1]
    #     #判断文件的后缀是否允许的文件类型中
    #     '''
    #     app.config.from_object(config_map[config_name])则是用来加载配置的。config_map是一个字典,其中存储了不同环境下的配置类，
    #     config_name是指当前需要使用的配置名。通过这行代码,应用会从config_map中取出对应的配置,并将其加载到Flask应用的配置中。

    # 关于current_app,它是Flask提供的一个上下文变量,用于在应用工厂模式下访问当前请求的应用实例。在请求处理过程中,
    # current_app可以用来获取当前活跃的Flask应用的配置、属性或方法。
    #     '''
    #     if suffix in current_app.config['ALLOWED_EXTENSIONS']:
    #         return True
    #     return False
    # return False#从右向左分割一次.获取第二个元素,即文件后缀，对于字符串'example.txt'，rsplit('.', 1)会返回['example', 'txt']，rsplit('.', 1)[1]会返回'txt'。
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def md5_file():
    '''
    将时间戳进行md5加密
    '''
    #获取当前时间戳
    # timestamp = str(time())
    # #将时间戳进行md5加密
    # md5_str = hashlib.md5(timestamp.encode('utf-8'))
    # #返回加密后的字符串
    # return md5_str.hexdigest()



    return hashlib.md5(str(time()).encode('utf-8')).hexdigest()

