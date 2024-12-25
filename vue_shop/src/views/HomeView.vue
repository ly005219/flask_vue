<template>
    <div class="common-layout container">
        <el-container class="container">
            <el-header class="header">
                <div class="logo">
                    <img src="../assets/login1.png" alt="">
                    <span>电商后台管理系统</span>
                </div>

                <div class="user">
                    <el-button @click="logout" type="success" plain>退出登录</el-button>
                </div>
            </el-header>
            
            <el-container class="main-container">
                <el-aside width="200px" class="aside">
                    <el-menu active-text-color="#ffd04b" 
                            background-color="#0d6496" 
                            class="el-menu-vertical-demo"
                            default-active="2" 
                            text-color="#fff" 
                            :unique-opened="true" 
                            router>
                        <el-sub-menu :index="index+' '" v-for="(item, index) in menulist.menus">
                            <template #title>
                                <el-icon>
                                    <component :is="menulist.icons[item.id]"></component>
                                </el-icon>
                                <span>{{ item.name}}</span>
                            </template>
                            <el-menu-item :index="childItem.path" 
                                        v-for="childItem in item.children">
                                {{ childItem.name }}
                            </el-menu-item>
                        </el-sub-menu>
                    </el-menu>
                </el-aside>

                <el-main class="main-content">
                    <router-view/>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index'
import { onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'

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
    getMenuList()
})

const router = useRouter()

const logout = () => {
    sessionStorage.removeItem('token')
    router.push('/login/')
}

const getMenuList = () => {
    api.get_menu({type_: 'tree'}).then(res => {
        console.log('菜单响应:', res)
        if (res?.data?.status === 200) {
            // 直接使用返回的数据
            menulist.menus = res.data.data || []
        } else {
            ElMessage.error(res?.data?.msg || '获取菜单失败')
        }
    }).catch(err => {
        console.error('获取菜单错误:', err)
        ElMessage.error('获取菜单失败')
    })
}
</script>

<style scoped>
/* 容器样式 */
.container {
    height: 100%;
    min-height: 100vh;
}

/* 头部样式 */
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    font-size: 20px;
    color: #999;
    height: 50px;
    width: 100%;
}

/* logo样式 */
.logo {
    float: left;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo img {
    width: 80px;
    height: 40px;
    margin-right: 10px;
}

/* 用户区域样式 */
.user {
    float: right;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
}

/* 主容器样式 */
.main-container {
    margin-top: 50px; /* 为固定头部留出空间 */
    height: calc(100vh - 50px); /* 减去头部高度 */
}

/* 侧边栏样式 */
.aside {
    position: fixed;
    left: 0;
    top: 50px; /* 头部高度 */
    bottom: 0;
    width: 200px !important;
    background-color: #0d6496;
    overflow-y: auto; /* 内容过多时显示滚动条 */
    z-index: 999;
}

/* 主内容区域样式 */
.main-content {
    margin-left: 200px; /* 为固定侧边栏留出空间 */
    min-height: calc(100vh - 50px); /* 确保内容区域至少占满剩余高度 */
    background-color: #f0f2f5;
    padding: 20px;
}

/* 滚动条样式优化 */
.aside::-webkit-scrollbar {
    width: 6px;
}

.aside::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
}

.aside::-webkit-scrollbar-track {
    background-color: transparent;
}

/* 菜单样式优化 */
.el-menu {
    border-right: none;
}

/* 确保内容区域不会被覆盖 */
.el-main {
    padding: 20px;
    box-sizing: border-box;
}
</style>
