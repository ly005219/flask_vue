## 1：建立menu和role的表多对多关系

```python
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
 
    parent_id=db.Column(db.Integer, db.ForeignKey('t_menus.id'))# 父级菜单id，子菜单与其父级关联不用每个都创建一个表，自关联
    children=db.relationship('Menu')#把子菜单子节点也获取处理

    #建立菜单和角色之间的关系,一个菜单对应多个角色,通过secondary指定第三张关联表,backref指定反向引用,lazy='dynamic'表示延迟加载,避免查询时加载所有角色信息,提高性能
    roles = db.relationship('Role', secondary=trm)
    # roles = db.relationship('Role', secondary=trm, backref=db.backref('menus', lazy='dynamic'))

class Role(db.Model):
    __tablename__ = 't_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    desc=db.Column(db.String(128))

    #建立角色和用户之间的关系,一个角色对应多个用户,前面建立了外键这里我们也建立一个反向引用,用于查找里面的信息
    users = db.relationship('User', backref='role')#backref='role'表示在user模型中添加一个role属性，通过这个属性可以获取到角色信息

    #)#建立角色和菜单之间的关系,一个角色对应多个菜单,通过secondary指定第三张关联表,backref指定反向引用,lazy='dynamic'表示延迟加载,避免查询时加载所有菜单信息,提高性能
    # menus = db.relationship('Menu', secondary=trm, backref=db.backref('roles', lazy='dynamic'))
    menus = db.relationship('Menu', secondary=trm)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
        }
 #创建同步数据库对象,$env:FLASK_APP = "manager"
 #传递app和数据库对象,创建完数据库后就进行三步命令：flask db init
 #    flask db migrate -m ''
 #    flask db upgrade
```

## 2:在t_roles_menus表中添加数据

```sql
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 1);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 2);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 3);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 4);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 5);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 21);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 31);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 32);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 22);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (1, 11);
#例如第一个用户拥有查看所有的权限，id为1，2，3...的用户管理，权限管理等等

INSERT INTO t_roles_menus (role_id, menu_id) VALUES (2, 1);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (2, 2);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (2, 3);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (2, 4);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (2, 5);
INSERT INTO t_roles_menus (role_id, menu_id) VALUES (2, 21);
```

## 3：在role表里面返回对应menu的所有数据，用relationship就行，为了两边同时都可以访问对方表里面的数据我们只要在一个里面加上一个backref就行，  menus = db.relationship('Menu', secondary=trm,backref=('roles'))，menus访问Menu，roles访问role表

```python
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
            'menus': [menu.to_dict_tree() for menu in self.menus if menu.level == 1] #获取一级菜单信息，转化为字典
        }
 #创建同步数据库对象,$env:FLASK_APP = "manager"
 #传递app和数据库对象,创建完数据库后就进行三步命令：flask db init
 #    flask db migrate -m ''
 #    flask db upgrade

```

## 4：把meus的数据加到role的页面的下拉框下面

```vue
 <el-table-column type="expand">
       <!-- 在这里可以放置展开的内容 --> 
       <template #default="scope">
                       
         <el-row v-for = " (m,i) in scope.row.menus" key="m.id" :class="['padding-left-100 bottom',i===0?'top':'']">
                 <el-col :span="2"><el-tag type="success" class="margin-10">{{ m.name }}</el-tag></el-col><!--可以查看的一级菜单权限-->
                  <el-col :span="1"><el-icon class="margin-top-10"><CaretRight/></el-icon></el-col>
                  <el-col :span="21"><el-tag type="primary" v-for="cm in m.children" :key="cm.id" class="margin-10">{{ cm.name }} </el-tag></el-col><!--可以查看的二级菜单权限-->

       </el-row>



       </template>
                      
    <style scoped>
.box-card {
    margin-top: 20px;
}
.padding-left-100{
    padding-left: 100px;
}
.top{
    border-top: 1px solid #eee;
}
.bottom{
    border-bottom: 1px solid #eee;
}
.margin-top-10{
    margin-top: 15px;
}
.margin-10{
    margin: 10px;
}


</style>
```

