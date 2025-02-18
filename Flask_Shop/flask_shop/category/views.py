from flask_shop.category import category_api,attribute_api,category_bp
from flask_restful import Resource,reqparse
from flask_shop import models,db
from flask import request

class Category(Resource):
    def get(self):

        level = request.args.get('level')
        pnum=request.args.get('pnum')
        psize=request.args.get('psize')

        if level:
            level = int(level)
        else:
            level = 3

        #获取所有分类信息
        base_query= models.Category.query.filter(models.Category.level == 1)

        if all([pnum,psize]):
            categories = base_query.paginate(page=int(pnum),per_page=int(psize))
        else:
            categories = base_query.all()

        #定义列表获取子节点level
        # categories_list = []
        #遍历一级分类
        # for c1 in categories:
        #     first_dict=c1.to_dict()
        #     #获取一级下的二级分类
        #     first_dict['children'] = []
        #     #遍历二级分类
        #     for c2 in c1.children:
        #         second_dict = c2.to_dict()
        #         #把二级分类的子节点添加到第一个分类的列表中
        #         first_dict['children'].append(second_dict)
        #         #获取二级下的三级分类
        #         second_dict['children'] = []
        #         for c3 in c2.children:
        #             third_dict = c3.to_dict()
        #             #把三级分类的子节点添加到第二个分类的列表中
        #             second_dict['children'].append(third_dict)
        #     #一级分类加到列表中
        #     categories_list.append(first_dict)
        categories_list = self.to_tree(categories,level)

        return {'status':200 ,'msg':'获取分类成功success','data':categories_list}

    #因为上面每次都是重复的给一个children的key，然后又遍历，下面是优化代码
    def to_tree(self,info:list,level):
        #定义一个空的列表来存储信息
        info_list = []
        #遍历信息
        for i in info:
            i_dict = i.to_dict()

            if i.level < level:

                #获取子节点
                children = self.to_tree(i.children,level)
                #把子节点添加到字典中
                i_dict['children'] = children
            #把字典添加到列表中
            info_list.append(i_dict)
        return info_list

    def post(self):
        try:
            #创建一个RequestParser对象，用于解析请求参数
            parser = reqparse.RequestParser()
            #添加参数规则
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('parent_id', type=int)
            parser.add_argument('level', type=int,required=True)
            #解析参数
            args = parser.parse_args()
            #获取参数
            if  args.get('parent_id'):
                category = models.Category(name=args.get('name'),parent_id=args.get('parent_id'),level=args.get('level'))
            
            else:
                category = models.Category(name=args.get('name'),level=args.get('level'))
            #保存到数据库
            db.session.add(category)
            db.session.commit()
            return {'status':200 ,'msg':'添加分类成功success'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'添加分类失败error'}
            



category_api.add_resource(Category, '/categories/')


#根据id删除单个分类
class CategoryDelete(Resource):
    def delete(self,id):
        try:
            #根据id获取分类信息
            category = models.Category.query.get(id)
            #删除分类信息
            db.session.delete(category)
            db.session.commit()
            return {'status':200 ,'msg':'删除分类成功success'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'删除分类失败error'}


category_api.add_resource(CategoryDelete, '/category/<int:id>/')



class Attributes(Resource):
    #根据category_id获取属性信息
    def get(self):
        #创建一个RequestParser对象，用于解析请求参数
        parser = reqparse.RequestParser()
        #添加参数规则
        parser.add_argument('category_id', type=int,required=True,location='args')
        parser.add_argument('_type', type=str,required=True,location='args')
        #解析参数
        args = parser.parse_args()
        #获取参数category_id
        category = models.Category.query.get(args.get('category_id'))
        #根据category_id获取属性信息
        attribute_list=[]
        if args.get('_type')=='static':
            attribute_list = [ a.to_dict() for a in category.attrs if a._type=='static']
        elif args.get('_type')=='dynamic':
            attribute_list = [ a.to_dict() for a in category.attrs if a._type=='dynamic']
        
        return {'status':200 ,'msg':'获取属性成功success','data':attribute_list}

    #添加属性信息
    def post(self):
        try:
            #创建一个RequestParser对象，用于解析请求参数
            parser = reqparse.RequestParser()
            #添加参数规则
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('value', type=str)
            parser.add_argument('category_id', type=int,required=True)
            parser.add_argument('_type', type=str,required=True)
            #解析参数
            args = parser.parse_args()
            #获取参数
            if  args.get('value'):
                attribute = models.Attribute(name=args.get('name'),value=args.get('value'),category_id=args.get('category_id'),_type=args.get('_type'))
            
            else:
                attribute = models.Attribute(name=args.get('name'),category_id=args.get('category_id'),_type=args.get('_type'))
            #保存到数据库
            db.session.add(attribute)
            db.session.commit()
            return {'status':200 ,'msg':'添加属性成功success'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'添加属性失败error'}
        
attribute_api.add_resource(Attributes, '/attributes/')

class Attribute(Resource):
    #根据属性id获取属性详情
    def get(self,id):
        try:
            #根据id获取属性信息
            attribute = models.Attribute.query.get(id)
            #返回属性信息
            return {'status':200 ,'msg':'获取属性成功success','data':attribute.to_dict()}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'获取属性失败error'}
    #根据属性id修改属性信息
    def put(self,id):
        try:
            #创建一个RequestParser对象，用于解析请求参数
            parser = reqparse.RequestParser()
            #添加参数规则
            parser.add_argument('name', type=str)
            parser.add_argument('value', type=str)
            parser.add_argument('category_id', type=int)
            parser.add_argument('_type', type=str)
            #解析参数
            args = parser.parse_args()
            #获取参数
            attribute = models.Attribute.query.get(id)
            if args.get('name'):
                attribute.name = args.get('name')
            if args.get('value'):
                attribute.value = args.get('value')
            if args.get('category_id'):
                attribute.category_id = args.get('category_id')
            if args.get('_type'):
                attribute._type = args.get('_type')
        
            #保存到数据库
            db.session.commit()
            return {'status':200 ,'msg':'修改属性成功success'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'修改属性失败error'}
    #根据属性id删除属性信息
    def delete(self,id):
        try:
            #根据id获取属性信息
            attribute = models.Attribute.query.get(id)
            #删除属性信息
            db.session.delete(attribute)
            db.session.commit()
            return {'status':200 ,'msg':'删除属性成功'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'删除属性失败'}
        


attribute_api.add_resource(Attribute, '/attribute/<int:id>/')

from sqlalchemy import func,text

#写一个数据统计函数
@category_bp.route('/statistics/')
def category_statistics():
    '''
    根据level获取分类分组信息

    '''
    #rs=db.session.query(models.Category.level,func.count(1)).group_by(models.Category.level).all()
    #一般企业复杂就用这种因为可能涉及很多什么联表查询等等，就用原生的sql这里的count(1)和count(*)区别就是count(1)是不包括null值的，而count(*)是包括null值的
    sql='select level,count(1) from t_categories group by level'
    rs=db.session.execute(text(sql)).all()
    data={
        'name':'分类统计',
        'xAxis':[f'{r[0]}级分类' for r in rs ]     ,
        'series':[r[1] for r in rs ]     ,
  

    }

    return {'status':200 ,'msg':'获取分类分组信息成功success','data':data}


class static_attr(Resource):
    def put(self,id):
        try:
            #创建一个RequestParser对象，用于解析请求参数
            parser = reqparse.RequestParser()
            #添加参数规则
            parser.add_argument('name', type=str)
            parser.add_argument('value', type=str)
            #解析参数
            args = parser.parse_args()
            #获取参数
            attribute = models.Attribute.query.get(id)
            if args.get('name'):
                attribute.name = args.get('name')
            if args.get('value'):
                attribute.value = args.get('value')
            #保存到数据库
            db.session.commit()
            return {'status':200 ,'msg':'修改属性成功success'}
        except Exception as e:
            print(e)
            return {'status':500 ,'msg':'修改属性失败error'}
        
attribute_api.add_resource(static_attr, '/static_attr/<int:id>/')