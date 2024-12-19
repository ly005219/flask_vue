<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>权限管理</el-breadcrumb-item>
        <el-breadcrumb-item>角色列表</el-breadcrumb-item>

    </el-breadcrumb>

    <el-card class="box-card">

        <el-row>
            <el-button type="primary" @click="addRose" :icon="CirclePlus">新增角色</el-button>
        </el-row>

        <el-row>
            <el-table :data="tableData.rolelist" stripe style="width: 100%" class="table">
                <el-table-column type="expand">
                    <!-- 在这里可以放置展开的内容 -->
                    <template #default="scope">

                        <el-row v-for=" (m,i) in scope.row.menus" key="m.id"
                            :class="['padding-left-100 bottom',i===0?'top':'']">
                            <el-col :span="2"><el-tag @click="removeMenu(scope.row,m.id)" type="success"
                                    class="margin-10" closable>{{ m.name }}</el-tag></el-col><!--可以查看的一级菜单权限-->
                            <el-col :span="1"><el-icon class="margin-top-10">
                                    <CaretRight />
                                </el-icon></el-col>
                            <el-col :span="21"><el-tag @click="removeMenu(scope.row,cm.id)" type="primary"
                                    v-for="cm in m.children" :key="cm.id" class="margin-10" closable>{{ cm.name }}
                                </el-tag></el-col><!--可以查看的二级菜单权限-->

                        </el-row>

                    </template>
                </el-table-column>
                <el-table-column prop="id" label="id" width="120"></el-table-column>
                <el-table-column prop="name" label="名称" width="200"></el-table-column>
                <el-table-column prop="desc" label="描述"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">

                        <el-button type="warning" @click="handleEdit(scope.$index)">编辑</el-button>
                        <el-button type="success"
                            @click="handlePermission(scope.row)">分配权限</el-button><!--这个scope.row就是当前行的数据用于可以数据回显-->
                        <el-button type="danger" @click="handleDelete(scope.$index)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>

    <el-dialog v-model="menuDialogVisible" title="分配权限" width="40%">
        <!-- 用el-tree渲染菜单树,这个menuList就是渲染的菜单树数据，menuProps是渲染的属性，包括label、children、disabled-->
        <el-tree show-checkbox style="max-width: 600px" :data="menuList" :props="menuProps"
            @node-click="handleNodeClick" node-key="id" ref="treeRef" default-expand-all="true" />
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="menuDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitPermission">
                    确定
                </el-button>
            </div>
        </template>
    </el-dialog>

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
</template>


<script setup>
import { ArrowRight , CirclePlus } from '@element-plus/icons-vue'
import { reactive ,onMounted , ref, nextTick } from 'vue';
import api from '@/api/index'//导入api接口


const tableData = reactive({
    rolelist: []

})

let menuDialogVisible = ref(false);
let menuList = reactive([]);

let rid=ref(null)
//这个里面的数据lable对应的属性名要和你menuList里面的对应，也就是接口的json数据要对，这个树chilren的也是要对应上
const menuProps = {
    label: 'name',
    children: 'children',
 
}

onMounted(() => {
    get_roles_list()
    getMenuList()
    
})
const get_roles_list = () => {
    api.get_roles_list().then(res => {
        console.log(res)
        tableData.rolelist = res.data.roles_data
        
    })
}
//用于存储选中的菜单节点
let KeyList =reactive([])
const treeRef = ref(null)

//新增角色对话框
let addRoleDialogVisible = ref(false);
//
const addRoleForm = reactive({
    name: '',
    desc: ''
})

//角色编辑框
let editRoleDialogVisible = ref(false);
//
const editRoleForm = reactive({
    name: '',
    desc: ''
})



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

//treeRef 是一个引用，用于访问 el-tree 组件的实例，以便可以调用组件的方法，如 setCheckedKeys。
// 具体来说：
// KeyList 是一个数组，用于存储需要默认选中的菜单节点的唯一标识（例如菜单项的 ID）。
// treeRef 通过 ref 创建，用于获取 el-tree 组件的实例。
// 当调用 treeRef.value.setCheckedKeys(KeyList) 时，您实际上是在告诉 el-tree 组件，根据 KeyList 中的值来设置哪些节点应该被选中。



//新增角色menu权限,点击这个handlePermission分配权限后触发这个dialog，menuDialogVisible.value = true;
const handlePermission = (row) => {
    menuDialogVisible.value = true;
    console.log(row)
    //初始化KeyList数组，不然每次都是接着上一次的KeyList，一次次的加载所有的选项都会被选中
    KeyList = []
    
    //获取二级菜单的id
    row.menus.forEach(m => {
        m.children.forEach(cm => {
            //将选中的菜单节点id存入KeyList数组中
            KeyList.push(cm.id)
        })
        })
        console.log(KeyList)
        //让dom更新后，让树加载数据后，设置默认选中的菜单节点
        nextTick(() => {
            //设置默认选中
            treeRef.value.setCheckedKeys(KeyList)
        })
        //给角色id赋值
        rid.value = row.id

}


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
        console.log('下面是新增角色的返回数据')
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








//
const getMenuList = () => {
    //调用以树型返回的menu数据
    api.get_menu().then(res => {
        console.log(res)
        menuList = res.data.menus
    })
}
//确定之后提交权限
const submitPermission = () => {
    //获取选中的菜单节点id
    let menu_ids = [
        //获取选中的菜单节点id
        treeRef.value.getCheckedKeys(),
        //获取半选菜单节点id
        treeRef.value.getHalfCheckedKeys()


    ]

    //将数组转换成字符串，用逗号分隔
    menu_ids = menu_ids.join(',')
    console.log(menu_ids)
  

    //获取角色id
    //console.log(rid.value)

    //调用接口提交权限
    api.set_menu(rid.value,{'menu_id':menu_ids}).then(res => {
        console.log(res)
        if(res.data.status==200){
            ElMessage({
                type: 'success',
                message: res.data.msg,
            })
        }else{
            ElMessage({
                type: 'error',
                message: res.data.msg,
            })

        }


        //关闭对话框
        menuDialogVisible.value = false
        //刷新页面
        get_roles_list()
    })

}



</script>


        <style scoped>
            .box-card {
                margin-top: 20px;
            }

            .padding-left-100 {
                padding-left: 100px;
            }

            .top {
                border-top: 1px solid #eee;
            }

            .bottom {
                border-bottom: 1px solid #eee;
            }

            .margin-top-10 {
                margin-top: 15px;
            }

            .margin-10 {
                margin: 10px;
            }
        </style>