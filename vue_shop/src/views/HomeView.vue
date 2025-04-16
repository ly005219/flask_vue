<template>
    <div class="common-layout container">
        <el-container class="container">
            <el-header class="header">
                <div class="logo">
                    <img src="../assets/login1.png" alt="">
                    <span>电商后台管理系统</span>
                </div>

                <div class="user">
                    <div class="user-info">
                        <!-- 不使用el-image的预览功能，改用自定义 -->
                        <img 
                            :src="userInfo.avatar" 
                            alt="头像" 
                            class="avatar clickable"
                            @click="showAvatarPreview = true">
                        
                        <div class="user-text">
                            <span class="username">{{ userInfo.username || '未登录' }}</span>
                            <span class="role-badge">{{ userInfo.role_desc || '游客' }}</span>
                        </div>
                        
                        <!-- 更换头像按钮 -->
                        <el-button 
                            type="primary" 
                            size="small" 
                            class="change-avatar-btn">
                            <el-dropdown @command="handleCommand">
                                <span class="el-dropdown-link">
                                    个人设置<el-icon class="el-icon--right"><arrow-down /></el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item command="changeAvatar">更换头像</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                        </el-button>
                    </div>
                    <el-button @click="logout" type="danger" plain>退出登录</el-button>
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
        
        <!-- 自定义头像预览对话框 -->
        <div v-if="showAvatarPreview" class="avatar-preview-overlay" @click="showAvatarPreview = false">
            <div class="avatar-preview-container" @click.stop>
                <div class="avatar-preview-wrapper">
                    <img :src="userInfo.avatar" alt="头像预览" class="avatar-preview-img">
                </div>
                <div class="avatar-preview-close" @click="showAvatarPreview = false">关闭</div>
            </div>
        </div>
        
        <!-- 更换头像对话框 -->
        <el-dialog
            v-model="showAvatarDialog"
            title="更换头像"
            width="400px"
            align-center>
            <div class="avatar-upload-container">
                <div class="preview-avatar" v-if="previewUrl">
                    <img :src="previewUrl" alt="预览" class="preview-img">
                </div>
                <div v-else class="upload-placeholder">
                    <el-icon><upload-filled /></el-icon>
                    <div>预览区域</div>
                </div>
                <el-upload
                    class="avatar-uploader"
                    action="#"
                    :auto-upload="false"
                    :show-file-list="false"
                    :on-change="handleAvatarChange"
                    :drag="true">
                    <template #default>
                        <div class="upload-area">
                            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                            <div class="upload-text">
                                <span>拖拽图片到此处或</span>
                                <span class="upload-link">点击上传</span>
                            </div>
                            <div class="upload-tip">支持JPG、PNG、GIF等格式图片，大小不超过2MB</div>
                        </div>
                    </template>
                </el-upload>
                <div class="avatar-actions" v-if="avatarFile">
                    <el-button @click="uploadAvatar" type="success">确认使用</el-button>
                    <el-button @click="cancelUpload">取消</el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index'
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowDown, UploadFilled } from '@element-plus/icons-vue'

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

// 头像上传相关变量
const avatarFile = ref(null)
const previewUrl = ref('')
const showAvatarDialog = ref(false)
const showAvatarPreview = ref(false)

// 用户信息对象
const userInfo = reactive({
    id: null,
    username: '',
    nick_name: '',
    role_name: '',
    role_desc: '游客',
    avatar: 'http://localhost:5000/static/avatar/init.png'
})

// 监听页面刷新,DOM渲染完成后执行
onMounted(() => {
    getMenuList()
    getUserInfo()
})

const router = useRouter()

const logout = () => {
    sessionStorage.removeItem('token')
    router.push('/login/')
}

// 处理下拉菜单命令
const handleCommand = (command) => {
    if (command === 'changeAvatar') {
        showAvatarDialog.value = true
    }
}

// 选择头像文件
const handleAvatarChange = (file) => {
    const isImage = file.raw.type.startsWith('image/')
    const isLt2M = file.raw.size / 1024 / 1024 < 2
    
    if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return
    }
    if (!isLt2M) {
        ElMessage.error('图片大小不能超过2MB!')
        return
    }
    
    avatarFile.value = file.raw
    // 创建临时URL用于预览
    previewUrl.value = URL.createObjectURL(file.raw)
}

// 取消头像上传
const cancelUpload = () => {
    avatarFile.value = null
    previewUrl.value = ''
}

// 上传头像
const uploadAvatar = async () => {
    if (!avatarFile.value) {
        ElMessage.warning('请先选择头像图片')
        return
    }
    
    try {
        const response = await api.upload_avatar(avatarFile.value)
        if (response.data.status === 200) {
            ElMessage.success('头像上传成功')
            // 更新头像显示
            const avatarUrl = response.data.data.avatar
            userInfo.avatar = 'http://localhost:5000' + avatarUrl
            // 清理临时文件
            cancelUpload()
            // 关闭对话框
            showAvatarDialog.value = false
        } else {
            ElMessage.error(response.data.msg || '上传失败')
        }
    } catch (error) {
        console.error('上传头像错误:', error)
        ElMessage.error('上传头像失败，请稍后再试')
    }
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

// 获取用户信息
const getUserInfo = () => {
    api.get_user_info().then(res => {
        console.log('用户信息响应:', res)
        if (res?.data?.status === 200) {
            // 更新用户信息
            const data = res.data.data
            userInfo.id = data.id
            userInfo.username = data.username || '未登录'
            userInfo.nick_name = data.nick_name || data.username || '未登录'
            userInfo.role_name = data.role_name || ''
            userInfo.role_desc = data.role_desc || '游客'  // 使用role_desc替代role_name
            
            // 确保头像路径正确
            if (data.avatar) {
                // 判断头像路径是否已经包含完整URL
                if (data.avatar.startsWith('http')) {
                    userInfo.avatar = data.avatar
                } else {
                    userInfo.avatar = 'http://localhost:5000' + data.avatar
                }
            } else {
                userInfo.avatar = 'http://localhost:5000/static/avatar/init.png'
            }
            
            console.log('用户信息已更新:', userInfo)
        } else {
            console.error('获取用户信息失败:', res?.data?.msg)
        }
    }).catch(err => {
        console.error('获取用户信息错误:', err)
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

/* 用户信息样式 */
.user-info {
    display: flex;
    align-items: center;
    margin-right: 15px;
}

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    margin-right: 10px;
    object-fit: cover;
    border: 2px solid #409EFF;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.clickable {
    cursor: pointer;
}

.avatar:hover {
    transform: scale(1.05);
    border-color: #67C23A;
    box-shadow: 0 0 8px rgba(103, 194, 58, 0.5);
}

/* 自定义头像预览样式 */
.avatar-preview-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.avatar-preview-container {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.avatar-preview-wrapper {
    width: 200px; /* 固定大小，屏幕的约1/5 */
    height: 200px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid white;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
    background-color: white;
}

.avatar-preview-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-preview-close {
    margin-top: 20px;
    background-color: white;
    color: #333;
    padding: 8px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.2s;
}

.avatar-preview-close:hover {
    background-color: #f2f2f2;
    transform: translateY(-2px);
}

.user-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    line-height: 1.2;
    margin-right: 15px;
}

.username {
    font-size: 15px;
    color: #333;
    font-weight: 500;
    margin-bottom: 4px;
}

.role-badge {
    display: inline-block;
    font-size: 12px;
    background-color: #409EFF;
    color: white;
    padding: 2px 8px;
    border-radius: 10px;
    white-space: nowrap;
    box-shadow: 0 2px 4px rgba(64, 158, 255, 0.2);
}

.change-avatar-btn {
    background-color: #67C23A;
    border-color: #67C23A;
    transition: all 0.3s;
    height: 32px;
    font-weight: 500;
    padding: 0 12px;
}

.change-avatar-btn:hover {
    background-color: #85ce61;
    border-color: #85ce61;
    transform: translateY(-2px);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.el-dropdown-link {
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
}

/* 头像上传样式 */
.avatar-upload-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.preview-avatar {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    overflow: hidden;
    margin-bottom: 20px;
    border: 3px solid #409EFF;
    box-shadow: 0 0 10px rgba(64, 158, 255, 0.3);
}

.preview-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.upload-placeholder {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
    border: 3px dashed #c0c4cc;
    color: #c0c4cc;
    font-size: 14px;
}

.upload-placeholder .el-icon {
    font-size: 40px;
    margin-bottom: 10px;
}

.avatar-actions {
    margin-top: 20px;
    display: flex;
    justify-content: space-around;
    width: 100%;
}

.avatar-uploader {
    margin: 15px 0;
    width: 100%;
}

.avatar-uploader :deep(.el-upload) {
    width: 100%;
}

.avatar-uploader :deep(.el-upload-dragger) {
    width: 100%;
    height: auto;
    padding: 20px;
    border-color: #409EFF;
    border-style: dashed;
}

.avatar-uploader :deep(.el-upload-dragger:hover) {
    border-color: #67C23A;
}

.upload-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #606266;
}

.el-icon--upload {
    font-size: 32px;
    color: #409EFF;
    margin-bottom: 8px;
}

.upload-text {
    margin: 10px 0;
    font-size: 14px;
}

.upload-link {
    color: #409EFF;
    font-weight: bold;
}

.upload-tip {
    color: #909399;
    font-size: 12px;
    margin-top: 8px;
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
