## 1：修复新增添加角色



```
base.js
   add_rose:"/roses/", //添加角色
index.js
  add_rose(params) {
     return axios.post(base.baseUrl + base.add_rose, params)
     
   },
```



```vue
        <el-row>
            <el-button type="primary" @click="addRose" :icon="CirclePlus">新增角色</el-button>
        </el-row>   

<!-- 一个新增角色对话框 -->
     <el-dialog v-model="addRoleDialogVisible" title="新增角色" width="40%" @close="addCancel">

        <el-form :model="addRoleForm" label-width="120px">
            <el-form-item label="角色名称">
                <el-input v-model="addRoleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="addRoleForm.desc"></el-input>
            </el-form-item>

        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addCancel">取消</el-button>
                <el-button type="primary" @click="addRoleSubmit">
                    确定
                </el-button>
            </div>
        </template>


     </el-dialog>



<script>
const addRose=() => {
    //打开对话框
    addRoleDialogVisible.value = true
  
    



}
//取消新增对话框
const addCancel = () => {
    addRoleDialogVisible.value = false
    //清空表单
    addRoleForm.name = ''
    addRoleForm.desc = ''
}

//新增角色
const addRoleSubmit = () => {

    let params={
        name:addRoleForm.name,
        desc:addRoleForm.desc
    }
    console.log(params)
    api.add_role(params).then(res => {
        console.log(res)
        console.log(res.data.status)
        if(res.data.status==200){
            ElMessage({
                type: 'success',
                message: res.data.msg,
            })
            //刷新页面
            get_roles_list()
            //关闭对话框
            addRoleDialogVisible.value = false
            //清空表单
            addRoleForm.name = ''
            addRoleForm.desc = ''
        }else{
            ElMessage({
                type: 'error',
                message: res.data.msg,
            })

        }

    })
    
}

</script>
```



## 2:删除角色



```vue
                <el-table-column label="操作">
                    <template #default="scope">

                        <el-button type="warning" @click="handleEdit(scope.$index)">编辑</el-button>
                        <el-button type="success"
                            @click="handlePermission(scope.row)">分配权限</el-button><!--这个scope.row就是当前行的数据用于可以数据回显-->
                        <el-button type="danger" @click="handleDelete(scope.$index)">删除</el-button>
                    </template>
                </el-table-column>
<script>
//删除角色
//这个index就是第几行的数据，如果是6，那么你可以用tableData.rolelist[6]获取到当前行的数据
const handleDelete = (index) => {
    //console.log(index)
    //console.log(tableData.rolelist[index])
    let id = tableData.rolelist[index].id
    const role_name = tableData.rolelist[index].name
    //console.log(id)
    ElMessageBox.confirm(
            '确认要删除'+ role_name +'角色吗?',
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
            message: '角色'+ role_name +'删除成功',
          })
          api.del_role(id).then(res => {
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



## 4:更新角色

```
base.js
    update_role:"/role/", //更新角色
index.js
   update_role(id, params) {
     return axios.put(base.baseUrl + base.update_role + id + "/", params)
   },
```



```vue
    <!-- 一个编辑角色对话框 -->
    <el-dialog v-model="editRoleDialogVisible" title="编辑角色" width="40%" @close="editCancel">

        <el-form :model="editRoleForm" label-width="120px">
            <el-form-item label="角色名称">
                <el-input v-model="editRoleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="editRoleForm.desc"></el-input>
            </el-form-item>

        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="editCancel">取消</el-button>
                <el-button type="primary" @click="editRoleSubmit">
                    确定
                </el-button>
            </div>
        </template>


    </el-dialog>
    
<script>
    
//角色编辑框
let editRoleDialogVisible = ref(false);
//
const editRoleForm = reactive({
    name: '',
    desc: ''
})

const selectedRoleId = ref(null); // 用于存储角色的 id


//编辑框打开和获取id
const handleEdit =(index) => {
    editRoleDialogVisible.value = true;
    selectedRoleId.value = tableData.rolelist[index].id; // 记录角色 id

};


//编辑角色
const editRoleSubmit = (index) => {
    //拿到编辑框handleEdit传过来的id和params
    // 使用 selectedRoleId 和 selectedRoleParams 进行角色编辑
    const id = selectedRoleId.value;
    const params = {
        //拿到输入框的内容
        name: editRoleForm.name,
        desc: editRoleForm.desc
    };



    console.log(params)
    api.update_role(id,params).then(res => {
        console.log(res)
        //console.log(res.data.status)
        if(res.data.status==200){
            ElMessage({
                type: 'success',
                message: res.data.msg,
            })
            //刷新页面
            get_roles_list()
            //关闭对话框
            editRoleDialogVisible.value = false
            //清空表单
            editRoleForm.name = ''
            editRoleForm.desc = ''
        }else{
            ElMessage({
                type: 'error',
                message: res.data.msg,
            })

        }


    })

}
//取消编辑对话框
const editCancel = () => {
    editRoleDialogVisible.value = false
    //清空表单
    editRoleForm.name = ''
    editRoleForm.desc = ''
}



</script>
```



## 5:商品列表的删除

把Picture表的外键关联商品id设置为级联

t_product_attrs同理



## 6：商品分类的删除



```python
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

#DELETE http://127.0.0.1:5000/category/157/

```



```vue
const handleDelete = (index,row) => {
   
    //console.log(row)
    let name=row.name
    let id=row.id
    //console.log(index)页面的索引
    //删除角色分类

  ElMessageBox.confirm(
    '确认要删除' + name + '的权限吗?',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
    
  )
    .then(() => {
      
      api.del_category(id).then(res => {
        if (res.data.status == 200) {
            ElMessage({
                type: 'success',
                message: '删除' + name + '的成功',
            })
            console.log(res)
        //删除之后，刷新页面，就不再显示删除之后的数据了
        get_category()

        } else {
            {
                ElMessage.warning({
                    showClose: true,
                    message: res.data.msg
                });
                // console.log(res.data.msg)
            }
        }

      })


    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '已取消删除',
      })
    })
}
```

