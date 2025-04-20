// import router from "@/router";
import axios from "axios"
import router from "@/router/index.js";

const errorHandle = (status,info) =>{
  switch(status){
    case 400:
      // console.log("语义错误");
      break;
    case 401:
      // console.log("服务器认证失败");
      break;
    case 403:
      // console.log("服务器请求拒绝执行");
      break;
    case 404:
      // console.log("请检查网路请求地址");
      break;
    case 500:
      // console.log("服务器发生意外");
      break;
    case 502:
      // console.log("服务器无响应");
      break;
    default:
      // console.log(info);
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
      // console.log("网络请求被中断了");
     }
   }
)
export default instance


