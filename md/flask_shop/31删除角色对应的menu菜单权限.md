## 1：删除角色对应的menu菜单权限，若删除一级菜单，子菜单也删除

```python
@role_bp.route('/role/<int:role_id>/<int:menu_id>/')
#删除指定的menu的权限
def delete_menu_permission(role_id,menu_id):

    #查找当前的角色信息
    role=models.Role.query.get(role_id)
    #查找当前的菜单信息
    memu=models.Menu.query.get(menu_id)

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
```

## 2:修复一下在获取角色列表的时候，不按角色与权限是否对应，而是全部返回子菜单权限的bug

```py
   '''
    如何获取子菜单的值
当您访问一个 Menu 实例的 children 属性时，SQLAlchemy 会查询与该实例关联的所有子菜单。这是通过以下步骤实现的：

当您创建菜单时，通过将子菜单的 parent_id 设置为对应父菜单的 id，建立了父子关系。
在访问 children 属性时，SQLAlchemy 根据 parent_id 来查询所有与该菜单相关联的子菜单。例如，如果有一个菜单的 id 是 1，那么任何 parent_id 为 1 的菜单都会被加载为其子菜单。
    '''
   
   
   def to_dict_tree(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'parent_id': self.parent_id,
            'children': [child.to_dict_tree() for child in self.children]#获取自己的子节点所以是一个列表，是一个meun的对象然后遍历转化为字典
            
            
        }
        
            def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            #'menus': [menu.to_dict_list() for menu in self.menus]#获取菜单信息，转化为字典
            # 'menus': [menu.to_dict_tree() for menu in self.menus if menu.level == 1] #获取一级菜单信息，转化为字典
            'menus':self.get_menus_dict()
        }
 #创建同步数据库对象,$env:FLASK_APP = "manager"
 #传递app和数据库对象,创建完数据库后就进行三步命令：flask db init
 #    flask db migrate -m ''
 #    flask db upgrade
    


  def get_menus_dict(self):
        menus_dict = []
        #用id于排序，拿到的一级显示顺序是根据id来排序
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




        
        
```



## 3:编写前端页面调用后端删除接口

```
### 角色删除特定的菜单权限
GET http://127.0.0.1:5000/role/1/2/

base.js
  del_role_menu:"/role/" //删除角色对应的权限
index.js
 del_role_menu(role_id, menu_id) {
     return axios.get(base.baseUrl + base.del_role_menu + role_id + "/" + menu_id + "/")
   },
   
```



```vue
  <template>
  <!--加个closable属性可以有个×的图像 -->
  <el-row v-for = " (m,i) in scope.row.menus" key="m.id" :class="['padding-left-100 bottom',i===0?'top':'']">
      <el-col :span="2"><el-tag @click="removeMenu(scope.row,m.id)" type="success" class="margin-10" closable>{{ m.name }}</el-tag></el-col><!--可以查看的一级菜单权限-->
        <el-col :span="1"><el-icon class="margin-top-10"><CaretRight/></el-icon></el-col>
         <el-col :span="21"><el-tag @click="removeMenu(scope.row,cm.id)" type="primary" v-for="cm in m.children" :key="cm.id" class="margin-10" closable>{{ cm.name }} </el-tag></el-col><!--可以查看的二级菜单权限-->

         </el-row>
  </template>

<script setup>
import { ArrowRight , CirclePlus } from '@element-plus/icons-vue'
import { reactive ,onMounted } from 'vue';
import api from '@/api/index'//导入api接口


const tableData = reactive({
    rolelist: []

})

onMounted(() => {
    get_roles_list()
    
})
const get_roles_list = () => {
    api.get_roles_list().then(res => {
        console.log(res)
        tableData.rolelist = res.data.roles_data
        
    })
}

//删除角色权限
const removeMenu = (row,menu_id) => {
  ElMessageBox.confirm(
    '确认要删除该角色的权限吗?',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
    
  )
    .then(() => {
      ElMessage({
        type: 'success',
        message: '权限删除成功',
      })
      api.del_role_menu(row.id,menu_id).then(res => {
        console.log(res)
        //删除之后，刷新页面，就不再显示删除之后的数据了
        get_roles_list()
      })


    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '已取消删除',
      })
    })
}




</script>

```

