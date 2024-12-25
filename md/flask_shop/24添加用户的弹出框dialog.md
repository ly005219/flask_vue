## 1：增加一个添加用户的弹出框dialog

```vue
   <!-- 一个增加用户弹窗 -->
    <el-dialog v-model="addDialogVisible" title="增加用户" width="500">
      <el-form :model="user_form">

      <el-form-item label="用户名" :label-width="formLabelWidth">
        <el-input v-model="user_form.name" autocomplete="off" />
      </el-form-item>

      <el-form-item label="密码" :label-width="formLabelWidth">
        <el-input v-model="user_form.pwd" autocomplete="off" />
      </el-form-item>

      <el-form-item label="确认密码" :label-width="formLabelWidth">
        <el-input v-model="user_form.real_pwd" autocomplete="off" />
      </el-form-item>

      <el-form-item label="昵称" :label-width="formLabelWidth">
        <el-input v-model="user_form.nick_name" autocomplete="off" />
      </el-form-item>

      <el-form-item label="手机号" :label-width="formLabelWidth">
        <el-input v-model="user_form.phone" autocomplete="off" />
      </el-form-item>

      <el-form-item label="邮箱" :label-width="formLabelWidth">
        <el-input v-model="user_form.email" autocomplete="off" />
      </el-form-item>

    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addDialogVisible = false">
          确认
        </el-button>
      </div>
    </template> 
  </el-dialog>

```



```
const user_form = reactive({
    username: null,
    pwd: null,
    real_pwd: null,
    nick_name: null,
    phone: null,
    email: null


})

const addDialogVisible = ref(false)//增加用户弹窗的显示状态
const formLabelWidth = '80px'//表单项的label宽度
```



## 2：按钮取消重置一下信息

```
//首先
const addFormRef = ref(null)//增加用户弹窗的表单ref，名字要和下面的ref一样还有click里面一样

//其次
  <el-dialog v-model="addDialogVisible" title="增加用户" width="500">
      <el-form :model="user_form" :rules="user_rules" ref="addFormRef">
      
//然后注入到这个按钮上面
       <el-button @click="addFormRest(addFormRef)">取消</el-button>
       
//最后写这个函数重置
//重置表单

//重置表单
const addFormRest = (formRef) => {
    formRef.resetFields()
    addDialogVisible.value=false
}


 
```

## 3：按×也取消信息

```
 <el-dialog v-model="addDialogVisible" title="增加用户" width="500" :before-close="addFormRest">//这个before-close就是会调用这个重置表单的函数即可
 
 
  const addFormRef = ref(null)//增加用户弹窗的表单ref
 //这下面就不能括号去传参数了，用ref定义的addFormRef.value去获取 
  <el-button @click="addFormRest">取消</el-button>
 
 //重置表单
const addFormRest = () => {
    addFormRef.value.resetFields()
    addDialogVisible.value=false
}


```



## 4：下面是完整代码

```vue
<template>
    <h1>这是用户列表</h1>
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
                <el-input v-model="user_data.queryName" placeholder="请输入要搜索的账号" class="input-with-select"  @keyup.enter="searchUser">

                    <template #append>
                        <el-button :icon="Search" @click="searchUser"/>
                    </template>
                </el-input>
            </el-col>
            <el-row>
          <el-button type="primary" :icon="CirclePlus" round plain @click="addDialogVisible = true">添加用户</el-button>
        </el-row>
        </el-row>




        <!-- 一个表格 -->
        <el-row>
        <el-table :data="user_data.tableData" stripe style="width: 100%" class="table">
            <el-table-column prop="id" label="id" width="180" />
            <el-table-column prop="username" label="账号" width="180" />
            <el-table-column prop="nick_name" label="昵称" />
            <el-table-column prop="phone" label="电话" />
            <el-table-column prop="email" label="邮箱" />

        </el-table>
    </el-row>


        <!-- 一个分页器 -->
        <el-pagination v-model:current-page="user_data.pageNum" v-model:page-size="user_data.pageSize"
            :page-sizes="pageSizes" :size="size" :disabled="disabled" :background="background"
            layout="total, sizes, prev, pager, next, jumper" :total="user_data.total" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" class="table"/>
    </el-card>


    <!-- 一个增加用户弹窗 -->
    <el-dialog v-model="addDialogVisible" title="增加用户" width="500" :before-close="addFormRest">
      <el-form :model="user_form" :rules="user_rules" ref="addFormRef">
		<!--// prop="username"和rules="user_rules" 绑在一起，可以获取到
          const user_rules = reactive({
  username:[
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 1, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],!-->

          
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

    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="addFormRest">取消</el-button>
        <el-button type="primary" @click="addDialogVisible = false">
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
    pageSize:2,//默认每页显示条数
    pageNum:1,//默认当前页
    queryName:''//搜索的账号

})

const user_form = reactive({
    username: null,
    pwd: null,
    real_pwd: null,
    nick_name: null,
    phone: null,
    email: null


})

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

//定义一个onMounted钩子函数
onMounted(() => {

    get_user_list()
})

const get_user_list = () => {
    let params = {
        'page': user_data.pageNum,//当前页
        'page_size': user_data.pageSize,//页数
        'username': user_data.queryName//搜索的账号

    }

    api.get_user({ params }).then(res => {
        console.log(res)
        user_data.tableData = res.data.data.data
        user_data.total = res.data.data.total
        // user_data.pagesize = res.data.data.page_size
        // user_data.pagenum = res.data.data.pnum
    })

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

</script>

<style scoped>
.box-card {
    margin-top: 20px;
}
.table{
    margin-top: 15px;


}


</style>

```



## 5:注册添加用户



```
    
    1:base.js已经有了之前的注册用户的路由，直接触发调用在index写函数view调用接口函数即可
    
    get_users:"/user/register/",     // 获取用户列表地址
    
    2:定义函数index.js，发送post请求
      register_user(params) {
     return axios.post(base.baseUrl + base.get_users, params)

   }
    
    3:view调用注册的接口
    
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
                    ElMessage.warning({
                        showClose: true,
                        message: res.data.msg});
                   
                    
                    
                    // console.log(res.data.msg)
                }
             
            })

        } else {
            console.log('验证失败')
            return false
        }


    })

}

4：在确认按钮上定义这个按钮点击事件
    <el-button type="primary"  @click="addUser(addFormRef)">
          确认
        </el-button>
```

