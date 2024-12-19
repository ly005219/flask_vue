
# from flask_shop import db
# from datetime import datetime

# from werkzeug.security import generate_password_hash,check_password_hash


# class BaseModel(object):
#     create_time=db.Column(db.DateTime, default=datetime.now)    
#     update_time=db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
        

# class User(db.Model,BaseModel):
#     __tablename__ = 't_users'
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     username = db.Column(db.String(50), nullable=False, unique=True)
#     pwd= db.Column(db.String(800))
#     nick_name= db.Column(db.String(50))
#     phone= db.Column(db.String(11), unique=True)
#     email= db.Column(db.String(50), unique=True)



#     @property
#     def password(self):
#         return self.pwd

#     @password.setter
#     def password(self, pwd):
#         self.pwd = generate_password_hash(pwd)

#     def check_password(self, pwd):
#         return check_password_hash(self.pwd, pwd)
from flask_shop import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)    
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class User(db.Model, BaseModel):
    __tablename__ = 't_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    pwd = db.Column(db.String(800))
    nick_name = db.Column(db.String(50))
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(50), unique=True)

    #建立用户和角色之间的关系,多个用户对应一个角色
    role_id = db.Column(db.Integer, db.ForeignKey('t_roles.id'))



    @property
    def password(self):
        return self.pwd

    @password.setter
    def password(self, pwd):
        # 使用默认的 PBKDF2 算法进行密码哈希
        self.pwd = generate_password_hash(pwd, method='pbkdf2:sha256')

    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nick_name': self.nick_name,
            'phone': self.phone,
            'email': self.email,
            'role_name':  self.role.name if self.role else None ,#backref='role'表示在user模型中添加一个role属性，通过这个属性可以获取到角色信息
            'role_desc':  self.role.desc if self.role else None,
            'role_id': self.role.id if self.role else None,

        }
 

#多对多role和menu的关系表
trm=db.Table('t_roles_menus',
    db.Column('role_id', db.Integer, db.ForeignKey('t_roles.id'), primary_key=True),
    db.Column('menu_id', db.Integer, db.ForeignKey('t_menus.id'), primary_key=True)
)




class Menu(db.Model):
    __tablename__ = 't_menus'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    level = db.Column(db.Integer, default=1)# 1 一级菜单 2 二级菜单 3 三级菜单
    path=db.Column(db.String(100))# 路由地址

    '''
    如何获取子菜单的值
当您访问一个 Menu 实例的 children 属性时，SQLAlchemy 会查询与该实例关联的所有子菜单。这是通过以下步骤实现的：

当您创建菜单时，通过将子菜单的 parent_id 设置为对应父菜单的 id，建立了父子关系。
在访问 children 属性时，SQLAlchemy 根据 parent_id 来查询所有与该菜单相关联的子菜单。例如，如果有一个菜单的 id 是 1，那么任何 parent_id 为 1 的菜单都会被加载为其子菜单。
    '''

 
    parent_id=db.Column(db.Integer, db.ForeignKey('t_menus.id'))# 父级菜单id，子菜单与其父级关联不用每个都创建一个表，自关联
    children=db.relationship('Menu')#把子菜单子节点也获取处理

    #建立菜单和角色之间的关系,一个菜单对应多个角色,通过secondary指定第三张关联表,backref指定反向引用,lazy='dynamic'表示延迟加载,避免查询时加载所有角色信息,提高性能
    #roles = db.relationship('Role', secondary=trm)
    #roles = db.relationship('Role', secondary=trm, backref=('menus'))

    #把模型转化为json
    def to_dict_tree(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'parent_id': self.parent_id,
            'children': [child.to_dict_tree() for child in self.children]#获取自己的子节点所以是一个列表，是一个meun的对象然后遍历转化为字典
        }


    def to_dict_list(self):
              return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'parent_id': self.parent_id,
          
        }

class Role(db.Model):
    __tablename__ = 't_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    desc=db.Column(db.String(128))

    #建立角色和用户之间的关系,一个角色对应多个用户,前面建立了外键这里我们也建立一个反向引用,用于查找里面的信息
    users = db.relationship('User', backref='role')#backref='role'表示在user模型中添加一个role属性，通过这个属性可以获取到角色信息

    #)#建立角色和菜单之间的关系,一个角色对应多个菜单,通过secondary指定第三张关联表,backref指定反向引用,lazy='dynamic'表示延迟加载,避免查询时加载所有菜单信息,提高性能
    # menus = db.relationship('Menu', secondary=trm, backref=db.backref('roles', lazy='dynamic'))
    menus = db.relationship('Menu', secondary=trm,backref=('roles'))


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            #'menus': [menu.to_dict_list() for menu in self.menus]#获取菜单信息，转化为字典
            #'menus': [menu.to_dict_tree() for menu in self.menus if menu.level == 1] #获取一级菜单信息，转化为字典
            'menus':self.get_menus_dict()
        }

    



    def get_menus_dict(self):
        menus_dict = []
        #用id于排序
        menus =sorted(self.menus, key=lambda x: x.id)

        for menu1 in menus:
             if menu1.level == 1:
                first_menu = menu1.to_dict_list()
                first_menu['children'] = []

                for menu2 in self.menus:
                       if menu2.parent_id == menu1.id and menu2.level == 2:
                            #将二级菜单添加到一级菜单的children列表中
                            first_menu['children'].append(menu2.to_dict_list())

                menus_dict.append(first_menu)
        return menus_dict

class Category(db.Model):
    __tablename__ = 't_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)#可以重名只是不同的分类
    level=db.Column(db.Integer, default=1)
    parent_id = db.Column(db.Integer, db.ForeignKey('t_categories.id'))# 父级菜单id，子菜单与其父级关联不用每个都创建一个表，自关联

    children = db.relationship('Category')#把子菜单子节点也获取处理,查看子节点
    attrs=db.relationship('Attribute', backref='category')#属性与分类关联

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'parent_id': self.parent_id,
        }
    


class Attribute(db.Model):
    __tablename__ = 't_attributes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    value=db.Column(db.String(255))
    _type=db.Column(db.Enum('static', 'dynamic'))#静态属性和动态属性

    category_id = db.Column(db.Integer, db.ForeignKey('t_categories.id'))# 所属分类id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            '_type': self._type,
            'category_id': self.category_id,
        }


class Product(db.Model):
    __tablename__ = 't_products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(512), nullable=False)
    price = db.Column(db.Float, default=0)
    number = db.Column(db.Integer, default=0)
    introduce = db.Column(db.Text)#商品介绍
    big_image = db.Column(db.String(255))#大图
    small_image = db.Column(db.String(255))#小图
    state=db.Column(db.Integer)#商品状态,0为未通过,1审核中,2审核通过
    is_promote=db.Column(db.Integer)#是否促销
    hot_number=db.Column(db.Integer)#热销数量
    weight=db.Column(db.Integer)#权重

    cid_one = db.Column(db.Integer, db.ForeignKey('t_categories.id'))# 一级分类id
    cid_two = db.Column(db.Integer, db.ForeignKey('t_categories.id'))# 二级分类id
    cid_three = db.Column(db.Integer, db.ForeignKey('t_categories.id'))# 三级分类id
 
    category = db.relationship('Category', foreign_keys=[cid_three])#关联第三级分类就都可以获取了,外键关联


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'number': self.number,
            'introduce': self.introduce,
            'big_image': self.big_image,
            'small_image': self.small_image,
            'state': self.state,
            'is_promote': self.is_promote,
            'hot_number': self.hot_number,
            'weight': self.weight,
            'cid_one': self.cid_one,
            'cid_two': self.cid_two,
            'cid_three': self.cid_three,
            'category':[ a.to_dict() for a in self.category.attrs]#拿出分类的属性信息
        }
    

class Picture(db.Model):
    __tablename__ = 't_pictures'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path=db.Column(db.String(255))#图片路径
    #一个商品多个图片，一对多关系，外键关联在多的
    product_id = db.Column(db.Integer, db.ForeignKey('t_products.id'))# 所属商品id


class ProductAttr(db.Model):
    #多对多的关系表
    __tablename__ = 't_product_attrs'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id= db.Column(db.Integer, db.ForeignKey('t_products.id'))# 所属商品id
    attr_id= db.Column(db.Integer, db.ForeignKey('t_attributes.id'))# 所属属性id
    value=db.Column(db.String(255))#属性值,当属性改变时不在检索这个共有类似管理员里面的这个属性类里面的value，而是我直接创建的这个字段私有的属性值
    _type=db.Column(db.Enum('static', 'dynamic'))#静态属性和动态属性,可以简化查询方式，虽然上面可以通过外键查询，也会有数据冗余，但是可以减少查询次数，提高性能

    

class Order(db.Model,BaseModel):
    __tablename__ = 't_orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price=db.Column(db.Float, default=0)
    number=db.Column(db.Integer, default=0)
    address=db.Column(db.String(255))
    pay_status=db.Column(db.Integer, default=0)#支付状态,0未支付,1已支付
    deliver_status=db.Column(db.Integer, default=0)#发货状态,0未发货,1已发货,2已收货
    confirm_status=db.Column(db.Integer, default=0)#确认收货状态,0未确认,1已确认收货
    confirm_content=db.Column(db.String(255))#确认收货内容
    user_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))# 所属用户id

    order_details=db.relationship('OrderDetail',backref='order')#一对多关系，外键关联在多的
    express=db.relationship('Express',backref='order')#一对多关系，外键关联在多的
    user=db.relationship('User', foreign_keys=[user_id])#用于多个外键的时候我们要具体指定
   
    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'number': self.number,
            'address': self.address,
            'pay_status': self.pay_status,
            'deliver_status': self.deliver_status,
            'confirm_status': self.confirm_status,
            'confirm_content': self.confirm_content,
            'user_id': self.user_id,
            'user': self.user.nick_name,
            'order_details': [a.to_dict() for a in self.order_details],
            'express': [a.to_dict() for a in self.express]
        }


#在创建一个外键表,订单详情表
class OrderDetail(db.Model):
    __tablename__ = 't_order_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('t_orders.id'))# 所属订单id
    product_id = db.Column(db.Integer, db.ForeignKey('t_products.id'))# 所属商品id
    number = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    total_price = db.Column(db.Float, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'number': self.number,
            'price': self.price,
            'total_price': self.total_price
        }

#物流快递表
class Express(db.Model):
    __tablename__ = 't_express'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('t_orders.id'))# 所属订单id
    content=db.Column(db.String(255))#快递信息
    update_time=db.Column(db.String(255))#更新时间

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'content': self.content,
            'update_time': self.update_time
        }

 #创建同步数据库对象,$env:FLASK_APP = "manager"
 #传递app和数据库对象,创建完数据库后就进行三步命令：flask db init
 #    flask db migrate -m ''
 #    flask db upgrade