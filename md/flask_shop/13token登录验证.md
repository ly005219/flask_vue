## 1:没有token不能访问主页面，得先登录

```
1：base.js定义url
2：router里面的index.js，创建router对象，用于router.push，router的路由守卫，并且里面设置跳转的验证有没有token，不然就next去登录页面
3：工具类的reuquest.js，创建axios对象，用于发送请求，这里搞个响应拦截器，每次请求都，处理错误和把token加到请求头，token验证后端没成功就删除无用token，router.push到登录页面，
4：index.js用于发送请求



```







在LoginView.vue里面把token加到浏览器里面

```javascript
//定义登录功能
const submitForm = (formRef) => {
    formRef.validate((valid) => {
        if (valid) {
            console.log('验证成功')
            api.getLogin(user).then(res => {
                //根据响应的状态码进行不同的操作
                if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    console.log(res)
                    //记录登录的token值，会话存储
                    sessionStorage.setItem('token', res.data.data.token)
                    //本地存储
                    // localStorage.setItem('token', res.data.data.token)




                    // console.log(res.data.msg)
                    //登录成功后跳转主页
                    router.push('/')


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

```



加完之后在index.js里面做路由的跳转验证

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [

  {
    path: '/login/',
    name: 'login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/',
    name: 'home',
    component: HomeView
  }
  



]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router


//做router跳转的login_required的验证
router.beforeEach((to, from, next) => {
  if (to.path === '/login/') {
    next()

  }else{
    //获取token值
    const token = sessionStorage.getItem('token') 
    if (!token ){
      next('/login/')
    }
    next()


  }


})
// 如果目标路径不是 /login/，则检查 sessionStorage 中是否存在 token。
// 如果 token 不存在，调用 next('/login/')，将用户重定向到登录页面。
// 如果 token 存在，再次调用 next()，允许导航继续进行。



```

## 2：在requests.js把token加到浏览器网络中

```javascript
import axios from "axios"


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
  response => response.status === 200 ? Promise.resolve(response) : Promise.reject(response),
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

## 3:在vue后端requests.js验证后端存储在浏览器的数据token值是否失效

```javascript
//import router from "@/router";
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
      if (response.data.status === 401) {//这个status和后端返回到浏览器的值一样
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

这就是后端在浏览器存储的token的值，返回的json

```python
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

