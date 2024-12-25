## 1:在views里面创建HomeView.vue的主页页面

1.1:下面还有一个登出的按钮，可以删除token然后跳转到登录页面

```vue
<template>
    <div class="common-layout contariner">
      <el-container class="contariner">
        <el-header class="header">
            <div class="logo">
                <img src="../assets/login1.png" alt="" >
                <span>电商后台管理系统</span>


            </div>

            <div class="user"> 
                <el-button @click="logout" type="success" plain>退出登录</el-button>
                <!-- <el-button @click="test" >测试</el-button> -->


            </div>


        </el-header>
        <el-container>
          <el-aside width="200px" class="aside">Aside</el-aside>
          <el-main>Main</el-main>
        </el-container>
      </el-container>
    </div>
  </template>
  

<script setup>
    import { useRouter } from 'vue-router'
    import api from '@/api/index'//导入api接口


    const router = useRouter()

    const logout = () => {
        //去除token
        sessionStorage.removeItem('token')
        //跳转到登录页面
        router.push('/login/')

    }

    // const test = () => {
    //     api.test_response().then(res => {
    //         console.log(res)
    //     })

    // }

</script>


<style scoped>
.header{
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    font-size: 20px;
    color: #999;
    height: 50px;
    width: 100%;
}
.logo img{
    width: 80px;
    height: 40px;
    margin-right: 10px;


}

.logo{
    float: left;/* 左浮动让logo里面的div可以横着显示，而不是一行一行的显示 */
    height: 50px;
 
    display: flex;
    align-items: center;/* 垂直居中 */
    justify-content: center;/* 水平居中 */


}
.user{
    float: right;/* 右浮动让user里面的div可以横着显示，而不是一行一行的显示 */
    display: flex;
    align-items: center;/* 垂直居中 */
    justify-content: center;/* 水平居中 */
    height: 50px;
}
.aside{
    width: 200px;
    background-color: #0d6496;
 

    
}
.contariner{

    height: 100%;
  
}

</style>


```

## 2:测试token如果失效就直接跳到登录页面

2.1：先加一个测试的按钮，然后肯定是在这里用api调用index.js中的api的中的utils的requests.js网络axios的api中base.js定义的路由地址。

首先：/api/base.js     :用于定义写好的页面网络的地址

```javascript
/**
 * 存放所有网络请求地址
 */
const base = {
    baseUrl:"http://localhost:5000",     // 公共地址
    login:"/user/login/",           // 登录地址 
    test_response:"/user/test_login/", // 测试token是否有效地址

  }
export default base
  
```

其次： /utils/requests.js	:用于创建axios对象和网络的错误处理（包括400等的错误返回；token失效的删除跳转到login）

```javascript
// import router from "@/router";
import axios from "axios"
import router from "@/router/index.js";

const errorHandle = (status,info) =>{
  switch(status){
    case 400:
      console.log("语义错误");
      break;
    case 401:
      console.log("服务器认证失败");
      break;
    case 403:
      console.log("服务器请求拒绝执行");
      break;
    case 404:
      console.log("请检查网路请求地址");
      break;
    case 500:
      console.log("服务器发生意外");
      break;
    case 502:
      console.log("服务器无响应");
      break;
    default:
      console.log(info);
      break;
   }
}
/**
 * 创建Axios对象
 */
const instance = axios.create({
  timeout:5000,
})




instance.interceptors.request.use(
  config =>{
    //获取token值
    let token =sessionStorage.getItem("token")
    if(token){
      config.headers.token = token//这个headers.token是后端定义传过来的token=request.headers.get('token')
    }


    return config
   },
  error => Promise.reject(error)
)
instance.interceptors.response.use(
  // response => response.status === 200 ? Promise.resolve(response) : Promise.reject(response),
  response => {
    if (response.status === 200) {
      if (response.data.status === 401) {
        //删除无效的token
        sessionStorage.removeItem("token")
        //token失效
        router.push("/login/")
      }
      return Promise.resolve(response)
    } else {
      return Promise.reject(response)
    }


  },



  error =>{
    const { response } = error;
    if(response){
      errorHandle(response.status,response.info)
     }else{
      console.log("网络请求被中断了");
     }
   }
)
export default instance



```

然后：/api/index.js	:定义方法用刚刚base.js定义的路由和requests.js的axios来发起请求

```javascript
import axios from "../utils/requests.js"
import base from "./base.js"


const api = {
  /**
   * 登录
   */
  getLogin(params) {
    return axios.post(base.baseUrl + base.login, params)
   },
  test_response(params) {
    return axios.get(base.baseUrl + base.test_response, params)

   }


}


export default api

```

最后在HomeVIew.vue中调用index.js中的api的方法返回其中的res和操作

```vue
    <template>
    <div class="user"> 
                <el-button @click="logout" type="success" plain>退出登录</el-button>
                <!-- <el-button @click="test" >测试</el-button> -->


           </div>
       </template>
       
<script>
 import api from '@/api/index'//导入api接口
   const test = () => {
    api.test_response().then(res => {
           console.log(res)
       })

    }
    
 </script>
```



## 3:在发送请求base.js的路由之前，后端要有这个处理的请求和逻辑

首先就是在后端中发送请求

```http
### test_login测试token
GET http://127.0.0.1:5000/user/test_login/
token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNzMwNjUzNzA1Ljg1NzYyNzl9.SV3kNodQTrAsHbrlDMfOEo5rMvL-gaDjxN_8XZYNKo8
```





```python
@user_bp.route('/test_login/')
@login_required
def test_login():
    return {'status':200,'msg':'token验证成功'}


```



可以看到执行这个代码之前下面也有token的一个验证的装饰器，保证他是正确的

```python
def verify_token(data):
    try:
        data = jwt.decode(data, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except Exception as e:
        print(f"Token verification error: {e}")  # 打印错误信息
        return None
    return data


def login_required(view_func):
    @wraps(view_func)
    def verify_token_info(*agrs,**kwagrs):
        token=request.headers.get('token')
        if verify_token(token):#如果这个token为真(不为空并且为原来用户登录的token)
             return view_func(*agrs,**kwagrs)
        else:
            return {'status': 401, 'msg': 'token过期或者无效'}
    return verify_token_info
```

