<template>
  
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>

    </el-breadcrumb>
    <el-card class="box-card">
        <!-- 一个搜索按钮 -->
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input v-model="user_data.queryName" placeholder="请输入要搜索的账号" class="input-with-select"
                    @keyup.enter="searchUser" clearable @clear="searchUser"  @input="handleInput" >

                    <template #append>
                        <el-button :icon="Search" @click="searchUser" />
                    </template>
                </el-input>
            </el-col>
            <el-row>
                <el-button type="primary" :icon="CirclePlus" round plain
                    @click="addDialogVisible = true">添加用户</el-button>
            </el-row>
        </el-row>




        <!-- 一个表格 -->
        <el-row>
            <el-table :data="user_data.tableData" stripe style="width: 100%" class="table">
                <el-table-column prop="id" label="id" width="50" />
                <el-table-column prop="username" label="账号" width="100" />
                <el-table-column prop="nick_name" label="昵称" />
                <el-table-column prop="phone" label="电话" />
                <el-table-column prop="email" label="邮箱" />
                <!-- <el-table-column prop="role_name" label="角色" /> -->
                <el-table-column prop="role_desc" label="角色" />

                <!--这里的prop数据就是调用api.get_user接口函数来获取数据库的数据!-->
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
                            编辑
                        </el-button>
                        <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                            删除
                        </el-button>
                        <el-button size="small" type="success" @click="handleReset(scope.$index, scope.row)">
                            重置
                        </el-button>

                      

                    </template>
                </el-table-column>

            </el-table>
        </el-row>


        <!-- 一个分页器 -->
        <el-pagination v-model:current-page="user_data.pageNum" v-model:page-size="user_data.pageSize"
            :page-sizes="pageSizes" :size="size" :disabled="disabled" :background="background"
            layout="total, sizes, prev, pager, next, jumper" :total="user_data.total" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" class="table" />
    </el-card>


    <!-- 一个增加用户弹窗 -->
    <el-dialog v-model="addDialogVisible" title="增加用户" width="500" :before-close="addFormRest">
        <el-form :model="user_form" :rules="user_rules" ref="addFormRef">

            <el-form-item label="用户名" :label-width="formLabelWidth" prop="username">
                <el-input v-model="user_form.username" autocomplete="off" />
            </el-form-item>

            <el-form-item label="密码" :label-width="formLabelWidth" prop="pwd">
                <el-input v-model="user_form.pwd" autocomplete="off" />
            </el-form-item>

            <el-form-item label="确认密码" :label-width="formLabelWidth" prop="real_pwd">
                <el-input v-model="user_form.real_pwd" autocomplete="off" />
            </el-form-item>

            <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="user_form.nick_name" autocomplete="off" />
            </el-form-item>

            <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="user_form.phone" autocomplete="off" />
            </el-form-item>

            <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="user_form.email" autocomplete="off" />
            </el-form-item>

            <el-form-item label="角色" :label-width="formLabelWidth" prop="role_id">
                <el-select v-model="user_form.role_id" placeholder="请选择角色">
                    <el-option :label="r.desc" :value="r.id" v-for="r in roles" :key="r.id"></el-option>                 
                </el-select>
            </el-form-item>

        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addFormRest">取消</el-button>
                <el-button type="primary" @click="addUser(addFormRef)">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>

   <!-- 一个编辑用户弹窗 -->
   <el-dialog v-model="editDialogVisible" title="编辑用户" width="500" >
        <el-form :model="edit_form"  ref="editFormRef">

            <el-form-item label="用户名" :label-width="formLabelWidth" prop="username">
                <el-input v-model="edit_form.username" autocomplete="off" disabled/>
            </el-form-item>


            <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="edit_form.nick_name" autocomplete="off" />
            </el-form-item>

            <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="edit_form.phone" autocomplete="off" />
            </el-form-item>

            <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="edit_form.email" autocomplete="off" />
            </el-form-item>

            <el-form-item label="角色" :label-width="formLabelWidth" prop="role_id">
                <el-select v-model="edit_form.role_id" placeholder="请选择角色">

                    <el-option :label="r.desc" :value="r.id" v-for="r in roles" :key="r.id"></el-option>
                 
                </el-select>
            </el-form-item>

        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="editDialogVisible=false">取消</el-button>
                <el-button type="primary" @click="editUser(editFormRef)">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
  




</template>


<script setup>
//面包屑的图标,搜索按钮的图标
import { ArrowRight, Search , CirclePlus } from '@element-plus/icons-vue'
import api from '@/api/index'//导入api接口
import { onMounted , reactive, ref} from 'vue'



const user_data=reactive({
    
    tableData: [],
    total: 10,
    pageSize:4,//默认每页显示条数
    pageNum:1,//默认当前页
    queryName:''//搜索的账号

})

const user_form = reactive({
    username: null,
    pwd: null,
    real_pwd: null,
    nick_name: null,
    phone: null,
    email: null,
    role_id: null,


})

let edit_form = reactive({
    id: null,
    username: null,
    nick_name: null,
    phone: null,
    email: null,
    role_name: null,
    role_desc: null,
    role_id: null



})


// const tableData = reactive({
//     rolelist: []

// })


//定义验证确认密码的规则
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请确认密码'))
  } else if (value !== user_form.pwd) {
    callback(new Error("两次密码输入不一致"))
  } else {
    callback()
  }
}


//定义验证手机号的规则
const validatePhone = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入手机号'))
  } else if (!/^1[34578]\d{9}$/.test(value)) {
    callback(new Error('手机号格式不正确'))
  } else {
    callback()
  }
}

//定义验证邮箱的规则
const validateEmail = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入邮箱'))
  } else if (!/\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/.test(value)) {
    callback(new Error('邮箱格式不正确'))
  } else {
    callback()
  }
}

const user_rules = reactive({
  username:[
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 1, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],

  pwd: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],

  real_pwd: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ],

  nick_name: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 1, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],

  phone: [

    { validator: validatePhone, trigger: 'blur' }
  ],

  email: [

    { validator: validateEmail, trigger: 'blur' }
]

})



let pageSizes =ref([1,2,5,10])

const background = ref(false)
const disabled = ref(false)
const size = ref('small')

const addDialogVisible = ref(false)//增加用户弹窗的显示状态
const formLabelWidth = '80px'//表单项的label宽度
const addFormRef = ref(null)//增加用户弹窗的表单ref

const editDialogVisible = ref(false)//编辑用户弹窗的显示状态
const editFormRef = ref(null)//编辑用户弹窗的表单ref

let userID=ref(0)//当前编辑用户的id
const RDialogVisible = ref(false)//重置密码弹窗的显示状态
let roles=ref([])//角色列表

//定义一个onMounted钩子函数
onMounted(() => {

    get_user_list(),
    get_roles_list()
})

// const get_user_list = () => {
//     let params = {
//         'page': user_data.pageNum,//当前页
//         'page_size': user_data.pageSize,//页数
//         'username': user_data.queryName//搜索的账号

//     }
//     console.log(params)

//     api.get_user({ params }).then(res => {
//         console.log('下面是用户列表数据')
//         console.log(res)
//         user_data.tableData = res.data.data.data
//         user_data.total = res.data.data.total
//         // user_data.pagesize = res.data.data.page_size
//         // user_data.pagenum = res.data.data.pnum
//     })

// }

const get_user_list = () => {
    let params = {
        'page': user_data.pageNum,
        'page_size': user_data.pageSize,
        'username': user_data.queryName
    };

    console.log(params);

    api.get_user({ params })
        .then(res => {
            console.log('下面是用户列表数据')
            console.log(res);
            if (res && res.data && res.data.data) {
                user_data.tableData = res.data.data.data;
                user_data.total = res.data.data.total;
            } else {
                console.error('响应数据格式不正确：', res);
            }
        })
        .catch(error => {
            console.error('请求失败，错误信息：', error);
        });
}






//分页器相关数据




const handleSizeChange = (val) => { //这个是改变每页显示条数的函数
//   console.log(val)
    user_data.pageSize = val//修改每页显示条数
    get_user_list()//重新获取数据

}
const handleCurrentChange = (val) => { //这个是改变当前页的函数
//   console.log(val)
    user_data.pageNum = val//修改当前页
    get_user_list()//重新获取数据
}

//获取用户列表
const searchUser = () => {
    console.log(user_data.queryName)
   
    //初始化页码
    user_data.pageNum = 1

    get_user_list()//重新获取数据

}

//重置表单
const addFormRest = () => {
    addFormRef.value.resetFields()
    addDialogVisible.value=false
}




//增加用户弹窗相关数据,注册
const addUser = (formRef) => {
    formRef.validate((valid) => {
        if (valid) {
            console.log('验证成功')
            api.register_user(user_form).then(res => {
                //根据响应的状态码进行不同的操作
                if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    console.log(res)
                    //重置表单
                    addFormRest()
                    //刷新页面，添加数据后自动刷新不用点击搜索之后在触发这个刷新的get_user_list()函数
                    get_user_list()
              

                }else{
                    //如果res.data.status ! == 200，说明验证失败，弹出错误信息res.data.msg
                    ElMessage.error({
                        showClose: true,
                        message: res.data.msg});
                   
                    
                    
                    console.log(res.data.msg)
                }
             
            })

        } else {
            console.log('验证失败')
            
          
            return false
        }


    })

}

//编辑用户弹窗相关数据,编辑
const handleEdit = (index, row) => {
    console.log(index, row)
    //打开编辑弹窗
    editDialogVisible.value = true


    //数据回显
    // edit_form.username = row.username
    // edit_form.nick_name = row.nick_name
    // edit_form.phone = row.phone
    // edit_form.email = row.email

    // edit_form=row//直接将数据赋值给edit_form，这样就不需要再次请求接口获取数据了，但是不安全

    //数据库获取数据
    api.get_user_by_id(row.id).then(res => {
        //edit_form = res.data.data//这个网络请求是异步的，所以有的时候打开了还没有显示
        edit_form.username = res.data.data.username
        edit_form.nick_name = res.data.data.nick_name
        edit_form.phone = res.data.data.phone
        edit_form.email = res.data.data.email
        edit_form.role_desc = res.data.data.role_desc
        edit_form.role_id = res.data.data.role_id

        // console.log(edit_form)
    })
        //每次打开页面给他动态修改
        userID.value = row.id

}

//编辑用户弹窗相关数据,提交编辑
const editUser =() => {
    api.edit_user(userID.value,edit_form).then(res => {
        if (res.data.status == 200) {
            //弹出框
            ElMessage({
                showClose: true,
                message: res.data.msg,
                type: 'success',
            })

            console.log(res)
           //关闭编辑弹窗
            editDialogVisible.value = false
            //刷新页面，添加数据后自动刷新不用点击搜索之后在触发这个刷新的get_user_list()函数
            get_user_list()

        } else {
            ElMessage.warning({
                showClose: true,
                message: res.data.msg});
            // console.log(res.data.msg)
        }
    })
       

    }

//删除用户
const handleDelete = (index, row) => {
    console.log(index, row)
    //弹出框
    ElMessageBox.confirm('确认删除'+row.username+'用户吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        }).then(() => {
            api.delete_user(row.id).then(res => {
                if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    console.log(res)
                    //刷新页面，添加数据后自动刷新不用点击搜索之后在触发这个刷新的get_user_list()函数
                    get_user_list()

                    } else {
                        ElMessage.warning({
                            showClose: true,
                            message: res.data.msg});
                        // console.log(res.data.msg)
                    }
            })
        }).catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消删除'
            })
        })
}

//重置用户密码
const handleReset = (index, row) => {
    console.log(index, row)
    //弹出框
    ElMessageBox.confirm('确认重置'+row.username+'用户密码吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        }).then(() => {
            api.reset_pwd(row.id).then(res => {
                if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    console.log(res)
                    //刷新页面，添加数据后自动刷新不用点击搜索之后在触发这个刷新的get_user_list()函数
                    get_user_list()

                    } else {
                        ElMessage.warning({
                            showClose: true,
                            message: res.data.msg});
                        // console.log(res.data.msg)
                    }
            })
        }).catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消重置'
            })
        })
}

//获取角色desc列表
const get_roles_list = () => {

    api.get_roles_list().then(res => {
        console.log(res)
        // tableData.rolelist = res.data.roles_data
        roles.value= res.data.roles_data
       
    })
}

//不断的搜索
const handleInput=()=>{
    if(user_data.queryName !==''){
        get_user_list()
    }else{
        get_user_list()
    }

}




</script>

<style scoped>
.box-card {
    margin-top: 20px;
}
.table{
    margin-top: 15px;


}


</style>
