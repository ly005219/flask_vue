<template>

    <div class="main">
        <div class="login">
            <div class="logo">
                <img src="../assets/login1.png" alt="">
            </div>

            <el-form :model="user" class="user_form" :rules="userRules" ref="userFormRef">
                <!-- //用户名 -->
                <el-form-item prop="username">
                    <el-input v-model="user.username" placeholder="请输入用户名" :prefix-icon="User" />
                </el-form-item>
                <!-- //密码 -->
                <el-form-item prop="pwd">
                    <el-input show-password v-model="user.pwd" placeholder="请输入密码" :prefix-icon="Lock" />
                </el-form-item>
                <!-- //登录按钮 -->
                <el-form-item class="login_btn">
                    <el-button type="primary" @click="submitForm(userFormRef)">登录</el-button>
                    <el-button type="success" @click="resetForm(userFormRef)">重置密码</el-button>
                </el-form-item>


            </el-form>
        </div>

    </div>

</template>

<script setup>
import { reactive, ref } from 'vue'
import { Lock, User } from '@element-plus/icons-vue'
import api from '@/api/index'//导入api接口
import { useRouter } from 'vue-router';
//导入路由对象
import { ElMessage } from 'element-plus'

//创建路由对象
const router = useRouter()

// 添加加载状态
const loading = ref(false)

//定义表单数据
const user = reactive({
    username: 'root',
    pwd: '123456'

})

//定义表单规则
const userRules = reactive({
    username: [
        { required: true, message: '用户名不能为空', trigger: 'blur' },
        { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
    ],
    pwd: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
    ]
})

//定义表单ref,为了让ref可以传递到resetForm方法中
const userFormRef = ref(null)


//定义重置表单方法
const resetForm = (formRef) => {
    formRef.resetFields()
}

//定义登录功能
const submitForm = (formRef) => {
    formRef.validate((valid) => {
        if (valid) {
            console.log('表单验证成功，开始登录请求')
            
            // 显示登录加载状态
            loading.value = true
            
            api.getLogin(user).then(res => {
                loading.value = false
                console.log('登录响应:', res)
                
                //根据响应的状态码进行不同的操作
                if (res.data.status === 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    //记录登录的token值和用户名，会话存储
                    sessionStorage.setItem('token', res.data.data.token)
                    sessionStorage.setItem('username', user.username)

                    //登录成功后跳转主页
                    router.push('/')
                } else {
                    ElMessage.warning({
                        showClose: true,
                        message: res.data.msg || '登录失败，请重试'
                    })
                }
            }).catch(err => {
                loading.value = false
                console.error('登录失败:', err)
                
                let errorMsg = '网络连接错误，请检查网络或稍后重试'
                if (err.response && err.response.data) {
                    errorMsg = err.response.data.msg || '服务器返回错误，请联系管理员'
                }
                
                ElMessage.error({
                    showClose: true,
                    message: errorMsg,
                    duration: 5000
                })
            })
        } else {
            console.log('表单验证失败')
            return false
        }
    })
}


</script>


<style scoped>
.main {
    width: 100%;
    height: 100%;
    background-color: rgb(223, 209, 26);
    /* 混合色示例 */

    display: flex;
    justify-content: center;
    align-items: center;

}

.login {
    width: 450px;
    height: 300px;
    background-color: snow;
    border-radius: 15px;

}

.logo {
    width: 200px;
    border: 1px solid #eee;
    box-shadow: 0 0 10px #ddd;
    padding: 5px;
    margin: 0 auto;
    margin-top: -67.5px;
    display: flex;
    border-radius: 10px;

}

img {
    width: 100%;
    height: 100%;


}

.logo p {
    font-size: 20px;
    text-align: center;


}

.user_form {

    padding: 50px;

}

.login_btn {
    display: flex;
    justify-content: space-between;
    /* ：在水平方向上，将子元素均匀地分布在容器的两端。 */

}

.login_btn button {
    flex: 1
}
</style>