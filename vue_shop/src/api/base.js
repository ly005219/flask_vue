/**
 * 存放所有网络请求地址
 */
const base = {
    baseUrl:"http://localhost:5000",     // 公共地址
    login:"/user/login/",           // 登录地址 
    test_response:"/user/test_login/", // 测试token是否有效地址
    get_menu:"/menu/menus/?type_=tree",     // 获取菜单地址,树的形式
    get_menu_list:"/menu/menus/",     // 获取菜单列表地址
    get_users:"/user/register/",     // 获取用户列表地址
    get_user_by_id:"/user/user/", //获取单个用户
    edit_user:"/user/user/",  //编辑用户
    delete_user:"/user/user/", //删除用户
    reset_pwd:"/user/reset_pwd/", //重置密码
    add_role:"/roles/", //添加角色
    del_role:"/role/", //删除角色
    update_role:"/role/", //更新角色
    get_roles_list:"/roles/",//获取角色列表
    del_role_menu:"/role/", //删除角色对应的权限
    set_menu:"/role/",//设置角色对应的权限
    get_category_list:"/categories/", //获取商品分类列表
    add_category:"/categories/", //添加商品分类
    del_category:"/category/", //删除商品分类
    get_attr_by_category:"/attributes/", //获取某个分类下的属性列表
    add_attr:"/attributes/", //添加属性
    add_attr_value:"/attribute",//添加属性值
    del_attr:"/attribute/", //删除属性
    update_attr:"/attribute/", //更新属性
    update_static_attr:"/static_attr/", //更新静态属性
    get_product_list:"/products/", //获取商品列表
    del_product:"/product/", //删除商品
    update_product:"/product/", //更新商品
    upload_img:"/upload_img/", //上传图片地址
    add_product:"/products/", //添加商品
    get_order_list:"/orders/", //获取订单列表
    get_express_list:"/expresses/", //获取快递列表
    get_category_statistics:"/statistics/", //获取商品分类统计数据
    get_user_info: "/user/info/",  // 获取用户信息的接口
    get_last_login: "/user/last_login/",  // 获取上次登录时间的接口
    get_sku_list: "/skus/",
    add_sku: "/skus/",
    update_sku: "/sku/",
    delete_sku: "/sku/",
    export_sku_pdf: "/skus/export/pdf/",
    export_sku_excel: "/skus/export/excel/",  // 修改导出接口
  }
export default base
  