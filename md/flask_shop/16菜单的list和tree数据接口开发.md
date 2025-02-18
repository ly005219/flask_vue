## 1:models定义一个列表的json数据返回方法

```python
    #把模型转化为json
    def to_dict_tree(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'parent_id': self.parent_id,
            'children': [child.to_dict_tree() for child in self.children]#获取自己的子节点所以是一个列表，是一个meun的对象然后遍历转化为字典
        }


    def to_dict_list(self):#全部获取出来，不用调用chilrent的子节点
              return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'parent_id': self.parent_id,
          
        }

```

## 2:菜单的menu的视图Views里面遍历获取和返回是否成功

```python
from flask_shop.menu import menu_api
from flask_restful import Resource
from flask_shop import models
from flask import request


class Menus(Resource):
    def get(self):
        #获取前端页面要求二点数据类型,list,type
        type_=request.args.get('type_')
        if type_=='tree':
            #通过模型获取菜单数据
            menu_list=models.Menu.query.filter(models.Menu.level==1).all()
            #将菜单数据转换为字典列表
            menu_dict_list=[]
            for menu in menu_list:
                menu_dict_list.append(menu.to_dict_tree())
            return {'status':200,'msg':'获取tree菜单成功','menus':menu_dict_list}   
        else:
            #通过模型获取菜单数据
            menu_list=models.Menu.query.filter(models.Menu.level != 0).all()

            #将菜单数据转换为字典列表
            menu_dict_list=[]
            for menu in menu_list:
                menu_dict_list.append(menu.to_dict_list())
            return {'status':200,'msg':'获取list菜单成功','menus':menu_dict_list}   


menu_api.add_resource(Menus, '/menus/')

#这个demo默认就是list
```

## 3：接口发送请求测试

```python
### 测试获取菜单，不加参数默认就是list
GET http://127.0.0.1:5000/menu/menus/?type_=tree
```

## 4：可以获取之后，我们要在前端进行同样的测试，显示到浏览器上

在base.js定义路由，这个路由和刚刚后端的发送的一样的

```http
/**
 * 存放所有网络请求地址
 */
const base = {
    baseUrl:"http://localhost:5000",     // 公共地址
    login:"/user/login/",           // 登录地址 
    test_response:"/user/test_login/", // 测试token是否有效地址
    get_menu:"/menu/menus/?type_=tree",     // 获取菜单地址

  }
export default base
  
```

在这个同级下的index.js来定义方法来返回刚刚的路由

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

   },
   get_menu(params) {
    return axios.get(base.baseUrl + base.get_menu, params)

   }



}


export default api

```

最后在你所写的HomeView.vue进行调用方法即可,这里还有element-plus的菜单添加

```vue
<template>
    <div class="common-layout contariner">
        <el-container class="contariner">
            <el-header class="header">
                <div class="logo">
                    <img src="../assets/login1.png" alt="">
                    <span>电商后台管理系统</span>


                </div>

                <div class="user">
                    <el-button @click="logout" type="success" plain>退出登录</el-button>
                    <!-- <el-button @click="test" >测试</el-button> -->


                </div>


            </el-header>
            <el-container>
                <el-aside width="200px" class="aside">

                    <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo"
                        default-active="2" text-color="#fff" @open="handleOpen" @close="handleClose">
                        <el-sub-menu index="1">
                            <template #title>
                                <el-icon>
                                    <location />
                                </el-icon>
                                <span>用户管理</span>
                            </template>
                            <el-menu-item index="1-1">item one</el-menu-item>
                            <el-menu-item index="1-2">item two</el-menu-item>
                           
                        </el-sub-menu>
                        
                    
                        

                        
                    </el-menu>


                </el-aside>
                <el-main>Main</el-main>
            </el-container>
        </el-container>
    </div>
</template>


<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index'//导入api接口
import { onMounted } from 'vue'

// 监听页面刷新,DOM渲染完成后执行，刷新后就调用这个方法获取数据
onMounted(() => {
    get_menu()

})
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
const get_menu = () => {
    //获取菜单数据
    api.get_menu().then(res => {
        console.log(res)

        })
}

```

