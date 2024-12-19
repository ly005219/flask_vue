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

                    <el-menu active-text-color="#ffd04b" background-color="#0d6496" class="el-menu-vertical-demo"
                        default-active="2" text-color="#fff" :unique-opened="true" router><!-- 这个router就是会将index作为路由跳转index="childItem.path" -->
                        <el-sub-menu :index="index+' '" v-for="(item, index) in menulist.menus">
                            <template #title>
                                <el-icon>
                                   <!-- <location /> 就是icon的图标 -->
                                    <component :is="menulist.icons[item.id]"></component>
                                </el-icon>
                                <span>{{ item.name}}</span>
                            </template>
                            <el-menu-item :index="childItem.path" v-for="childItem in item.children">{{ childItem.name }} </el-menu-item>
                          
                        </el-sub-menu>
                        
                    
                        

                        
                    </el-menu>


                </el-aside>
                <el-main>
                    <router-view/>



                </el-main>
            </el-container>
        </el-container>
    </div>
</template>


<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index'//导入api接口
import { onMounted, reactive} from 'vue'


const menulist = reactive({
    menus: [],
    icons:{
        '1':'User',
        '2':'Tools',
        '3':'Shop',
        '4':'ShoppingCart',
        '5':'PieChart',

    }


})


// 监听页面刷新,DOM渲染完成后执行
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
        // console.log(res)
        menulist.menus = res.data.menus

        })
}



</script>


<style scoped>
.header {
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    font-size: 20px;
    color: #999;
    height: 50px;
    width: 100%;
}

.logo img {
    width: 80px;
    height: 40px;
    margin-right: 10px;


}

.logo {
    float: left;
    /* 左浮动让logo里面的div可以横着显示，而不是一行一行的显示 */
    height: 50px;

    display: flex;
    align-items: center;
    /* 垂直居中 */
    justify-content: center;
    /* 水平居中 */


}

.user {
    float: right;
    /* 右浮动让user里面的div可以横着显示，而不是一行一行的显示 */
    display: flex;
    align-items: center;
    /* 垂直居中 */
    justify-content: center;
    /* 水平居中 */
    height: 50px;
}

.aside {
    width: 200px;
    background-color: #0d6496;



}

.contariner {

    height: 100%;

}
</style>
