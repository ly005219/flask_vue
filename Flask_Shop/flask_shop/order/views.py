from flask_restful import Resource,reqparse
from flask_shop.order import order_api
from flask_shop import db,models

class OrderList(Resource):
    '''
    获取订单列表
    '''
    def get(self):
        #定义一个解析器
        parser = reqparse.RequestParser()
        #添加参数
        parser.add_argument('name',type=str,location='args')#这个是get请求，然后要设置在url里面，所以要加location='args'
        #location='args'表示这个参数是从url中获取
        #解析参数
        args = parser.parse_args()
        #获取参数
        name = args.get('name')
        #根据参数查询列表
        if name:
            #orders = models.Order.query.filter(models.User.nick_name.like('%'+name+'%')).all()
            orders = models.Order.query.join(models.User).filter(models.User.nick_name.like('%' + name + '%')).all()

        else:
            orders = models.Order.query.all()
        #返回列表
        return {
            'status':200,
            'msg':'订单列表获取成功',
            'orders':[order.to_dict() for order in orders]
            }
    

order_api.add_resource(OrderList,'/orders/')


#获取单个信息
class Order(Resource):
    def get(self,id):
        order = models.Order.query.get(id)
        return {
           'status':200,
           'msg':'订单详情获取成功',
           'order':order.to_dict()
        }
    
order_api.add_resource(Order,'/orders/<int:id>/')



class Expresses(Resource):
    def get(self,order_id):
        expresses = models.Express.query.filter(models.Express.order_id==order_id).order_by(models.Express.update_time.desc()).all()
        return {
           'status':200,
           'msg':'订单物流信息获取成功',
            'expresses':[express.to_dict() for express in expresses]
        }

order_api.add_resource(Expresses,'/expresses/<int:order_id>/')



