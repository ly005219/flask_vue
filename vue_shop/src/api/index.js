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

   },
   get_menu(params) {
    return axios.get(base.baseUrl + base.get_menu, params)

   },
   get_user(params) {
    //  if(params.username){
    //    return axios.get(base.baseUrl + base.get_users +'?username=' + params.username ,params)
    //  }else{
    //    return axios.get(base.baseUrl + base.get_users, params)
    //  }
    return axios.get(base.baseUrl + base.get_users, params)
    

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
   get_menu_list(params) {
     return axios.get(base.baseUrl + base.get_menu_list, params)
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
     return axios.get(base.baseUrl + base.get_roles_list, params)
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
   }
   

}


export default api