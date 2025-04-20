import axios from "axios"
import base from "./base.js"

// 配置axios默认值
axios.defaults.withCredentials = true
axios.defaults.headers.common['Content-Type'] = 'application/json'

// 添加请求拦截器
axios.interceptors.request.use(
  config => {
    // 添加token
    const token = sessionStorage.getItem('token')
    if (token) {
      config.headers.token = token
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

const api = {
  /**
   * 登录
   */
  getLogin(params) {
    // console.log('开始登录请求:', params.username);
    return axios({
      method: 'post',
      url: base.baseUrl + base.login,
      data: params,
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true
    }).catch(error => {
      console.error('登录请求错误:', error);
      if (error.response) {
        console.error('错误响应数据:', error.response.data);
        console.error('错误状态码:', error.response.status);
      } else if (error.request) {
        console.error('没有收到响应:', error.request);
      } else {
        console.error('请求配置错误:', error.message);
      }
      throw error; // 重新抛出错误，让调用者可以处理
    });
  },
  test_response(params) {
    return axios.get(base.baseUrl + base.test_response, params)

   },
   get_menu(params) {
    return axios({
      method: 'get',
      url: base.baseUrl + base.get_menu,
      params: params,
      headers: {
        'Content-Type': 'application/json',
        'token': sessionStorage.getItem('token')
      }
    })
   },
   get_user(params) {
    //  if(params.username){
    //    return axios.get(base.baseUrl + base.get_users +'?username=' + params.username ,params)
    //  }else{
    //    return axios.get(base.baseUrl + base.get_users, params)
    //  }
    return axios({
      method: 'get',
      url: base.baseUrl + base.get_users,
      params: params.params, // 正确提取params中的params对象
      headers: {
        'Content-Type': 'application/json',
        'token': sessionStorage.getItem('token')
      }
    })
   },
   register_user(params) {
     return axios.post(base.baseUrl + base.get_users, params)

   },
   get_user_by_id(id) {
     return axios.get(base.baseUrl + base.get_user_by_id + id + "/")//### 测试根据ID获取单个用户,GET http://127.0.0.1:5000/user/user/1/
     
   },
   edit_user(id, params) {
     return axios.put(base.baseUrl + base.edit_user + id + "/", params)
   },
   delete_user(id) {
     return axios.delete(base.baseUrl + base.delete_user + id + "/")
   },
   reset_pwd(id){
     return axios.get(base.baseUrl + base.reset_pwd + id + "/")

   },
   get_menu_list() {
     return axios.get(base.baseUrl + base.get_menu_list)
   },
   
   add_role(params) {
     return axios.post(base.baseUrl + base.add_role, params)
     
   },
   del_role(id) {
     return axios.delete(base.baseUrl + base.del_role + id + "/")
   },
   update_role(id, params) {
     return axios.put(base.baseUrl + base.update_role + id + "/", params)
   },

   get_roles_list(params) {
     return axios({
        method: 'get',
        url: base.baseUrl + base.get_roles_list,
        headers: {
            'Content-Type': 'application/json',
            'token': sessionStorage.getItem('token')
        }
    })
   },
   del_role_menu(role_id, menu_id) {
     return axios.get(base.baseUrl + base.del_role_menu + role_id + "/" + menu_id + "/")
   },
   set_menu(role_id,params){
     return axios.post(base.baseUrl + base.set_menu + role_id + "/", params)
   },
   get_category_list(level) {
     return axios.get(base.baseUrl + base.get_category_list +'?level='+ level)
   },
   add_category(params) {
     return axios.post(base.baseUrl + base.add_category, params)
   },
   del_category(id) {
     return axios.delete(base.baseUrl + base.del_category + id + "/")
   },
   get_attr_by_category(category_id,_type) {
     return axios.get(base.baseUrl + base.get_attr_by_category +"?category_id="+category_id + "&_type=" + _type )
   },
   add_attr(params) {
     return axios.post(base.baseUrl + base.add_attr, params)
   },
   updata_attr_value(id,params) {
     return axios.put(base.baseUrl + base.add_attr_value + "/" + id + "/", params)
   },
   del_attr(id) {
     return axios.delete(base.baseUrl + base.del_attr + id + "/")
   },
   update_attr(id,params){
     return axios.put(base.baseUrl + base.update_attr + id + "/", params)
   },
   update_static_attr(id,params){
     return axios.put(base.baseUrl + base.update_static_attr + id + "/", params)
   },
   get_product_list(params) {
  //    if(name){
  //      return axios.get(base.baseUrl + base.get_product_list + "?name=" + name)
  //    }else{
  //      return axios.get(base.baseUrl + base.get_product_list)
  //    }
   
  //  },
    return axios.get(base.baseUrl + base.get_product_list, params)

   },
   get_all_products() {
     return axios.get(base.baseUrl + base.get_all_products)
   },
   del_product(id) {
     return axios.delete(base.baseUrl + base.del_product + id + "/")
   },
   update_product(id, params) {
     return axios.put(base.baseUrl + base.update_product + id + "/", params)
   },
   add_product(params) {
     return axios.post(base.baseUrl + base.add_product, params)
   },
   get_order_list(params) {
     return axios.get(base.baseUrl + base.get_order_list, params)
   },
   get_express_list(order_id) {
     return axios.get(base.baseUrl + base.get_express_list + order_id + "/")
   },
   get_category_statistics(){
     return axios.get(base.baseUrl + base.get_category_statistics)
   },
   // 获取用户信息
   get_user_info() {
     return axios.get(base.baseUrl + base.get_user_info)
   },
   getLastLogin(username) {
     return axios.get(base.baseUrl + base.get_last_login + `?username=${username}`)
   },
   get_sku_list(params) {
     return axios.get(base.baseUrl + base.get_sku_list, {
       params: params,
       headers: {
         'Content-Type': 'application/json',
         'token': sessionStorage.getItem('token')
       }
     })
   },
   add_sku(params) {
     return axios({
        method: 'post',
        url: base.baseUrl + base.add_sku,
        data: params,
        headers: {
            'Content-Type': 'application/json',
            'token': sessionStorage.getItem('token')
        }
    })
   },
   update_sku(id, params) {
     return axios.put(base.baseUrl + base.update_sku + id + "/", params)
   },
   delete_sku(id) {
     return axios({
       method: 'delete',
       url: base.baseUrl + base.delete_sku + id + "/",
       headers: {
         'Content-Type': 'application/json',
         'token': sessionStorage.getItem('token')
       }
     })
   },
   
   // 上传用户头像
   upload_avatar(file) {
     // 创建FormData对象
     const formData = new FormData()
     formData.append('avatar', file)
     
     return axios({
       method: 'post',
       url: base.baseUrl + base.upload_avatar,
       data: formData,
       headers: {
         'Content-Type': 'multipart/form-data',
         'token': sessionStorage.getItem('token')
       }
     })
   },
   
   // 获取头像编辑器页面URL
   get_avatar_editor_url() {
     return base.baseUrl + base.avatar_editor
   },
   
   // 高级头像处理API
   process_avatar(imageData, options = {}) {
     // 创建FormData对象
     const formData = new FormData()
     
     // 如果传入的是File对象
     if (imageData instanceof File) {
       formData.append('image', imageData)
     } 
     // 如果传入的是Blob对象（如Canvas导出的数据）
     else if (imageData instanceof Blob) {
       formData.append('image', imageData, 'cropped-image.jpg')
     }
     // 如果是Base64图像数据
     else if (typeof imageData === 'string' && imageData.startsWith('data:image')) {
       // 将Base64转换为Blob
       const byteString = atob(imageData.split(',')[1])
       const mimeString = imageData.split(',')[0].split(':')[1].split(';')[0]
       const ab = new ArrayBuffer(byteString.length)
       const ia = new Uint8Array(ab)
       for (let i = 0; i < byteString.length; i++) {
         ia[i] = byteString.charCodeAt(i)
       }
       const blob = new Blob([ab], { type: mimeString })
       formData.append('image', blob, 'cropped-image.jpg')
     } else {
       throw new Error('无效的图像数据格式')
     }
     
     // 添加裁剪数据
     if (options.cropData) {
       formData.append('crop_data', JSON.stringify(options.cropData))
     }
     
     // 添加其他选项
     if (options.rotate) formData.append('rotate', options.rotate)
     if (options.quality) formData.append('quality', options.quality)
     if (options.format) formData.append('format', options.format)
     if (options.size) formData.append('size', options.size)
     if (options.filter) formData.append('filter', options.filter)
     if (options.filterIntensity) formData.append('filter_intensity', options.filterIntensity)
     if (options.targetKb) formData.append('target_kb', options.targetKb)
     
     // 是否为预览请求
     if (options.preview) formData.append('preview', 'true')
     
     // 发送请求
     return axios({
       method: 'post',
       url: base.baseUrl + base.process_avatar,
       data: formData,
       headers: {
         'Content-Type': 'multipart/form-data',
         'token': sessionStorage.getItem('token')
       }
     })
   },
   delete_menu(id) {
     return axios.delete(base.baseUrl + base.del_menu + id + '/')
   },
   // 获取当前用户的菜单权限
   getUserPermissions() {
     return axios({
       method: 'get',
       url: base.baseUrl + base.user_permissions,
       headers: {
         'Content-Type': 'application/json',
         'token': sessionStorage.getItem('token')
       }
     })
   }
}


export default api
