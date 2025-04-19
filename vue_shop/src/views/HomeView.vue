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
                            <el-dropdown @command="handleCommand" :teleported="false">
                                <span class="el-dropdown-link">
                                    个人设置<el-icon class="el-icon--right"><arrow-down /></el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item command="changeAvatar">基本头像上传</el-dropdown-item>
                                        <el-dropdown-item command="advancedAvatar">高级头像编辑</el-dropdown-item>
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
                        <template v-for="(item, index) in menuList" :key="item.id || index">
                            <!-- 如果菜单有子项且为一级菜单，使用子菜单组件 -->
                            <el-sub-menu 
                                :index="String(index)"
                                v-if="item && item.level === 1 && item.children && item.children.length > 0">
                            <template #title>
                                <el-icon>
                                        <component :is="iconMapping[item.id] || 'Menu'"></component>
                                </el-icon>
                                    <span>{{ item.name }}</span>
                            </template>
                                
                                <!-- 遍历二级菜单 -->
                                <template v-for="subItem in item.children" :key="subItem.id">
                                    <!-- 如果二级菜单有子项，再创建子菜单 -->
                                    <el-sub-menu 
                                        v-if="subItem && subItem.children && subItem.children.length > 0" 
                                        :index="subItem.id.toString()">
                                        <template #title>
                                            <span>{{ subItem.name }}</span>
                                        </template>
                                        
                                        <!-- 遍历三级菜单项 -->
                                        <el-menu-item 
                                            v-for="childItem in subItem.children" 
                                            :key="childItem.id"
                                            :index="childItem.path">
                                {{ childItem.name }}
                            </el-menu-item>
                        </el-sub-menu>
                                    
                                    <!-- 如果二级菜单没有子项，则显示为菜单项 -->
                                    <el-menu-item 
                                        v-else
                                        :index="subItem.path"
                                        v-if="subItem">
                                        {{ subItem.name }}
                                    </el-menu-item>
                                </template>
                            </el-sub-menu>
                            
                            <!-- 无子菜单的一级菜单直接显示为菜单项 -->
                            <el-menu-item 
                                v-else-if="item && item.level === 1" 
                                :index="item.path || String(index)">
                                <el-icon>
                                    <component :is="iconMapping[item.id] || 'Menu'"></component>
                                </el-icon>
                                <span>{{ item.name }}</span>
                            </el-menu-item>
                        </template>
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
            title="上传头像"
            width="600px"
            destroy-on-close
            class="avatar-dialog"
        >
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

        <!-- 高级头像编辑对话框 -->
        <el-dialog
            v-model="showAdvancedAvatarDialog"
            title="高级头像编辑"
            width="800px"
            align-center
            :before-close="closeAdvancedAvatarEditor"
            @open="onDialogOpen">
            <div class="debug-panel">
                <div>对话框状态: {{ showAdvancedAvatarDialog ? '已打开' : '已关闭' }}</div>
                <div>文件选择状态: {{ advancedAvatarFile ? '已选择文件' : '未选择文件' }}</div>
                <div>图片URL: {{ advancedImageUrl ? '已设置' : '未设置' }}</div>
                <div v-if="imageSize">
                    <div>图像尺寸信息:</div>
                    <ul>
                        <li>自然宽度: {{ imageSize.naturalWidth }}px</li>
                        <li>自然高度: {{ imageSize.naturalHeight }}px</li>
                        <li>客户端宽度: {{ imageSize.clientWidth }}px</li>
                        <li>客户端高度: {{ imageSize.clientHeight }}px</li>
                        <li>偏移宽度: {{ imageSize.offsetWidth }}px</li>
                        <li>偏移高度: {{ imageSize.offsetHeight }}px</li>
                    </ul>
                </div>
                <div>
                    <el-tooltip
                        content="初始化图像处理，当图像未正确显示时使用"
                        placement="top"
                        effect="light"
                    >
                        <el-button size="small" @click="debugInitCropper">调试初始化</el-button>
                    </el-tooltip>
                    <el-tooltip
                        content="强制重新载入图像并重新渲染，解决图像不显示或处理错误问题"
                        placement="top"
                        effect="light"
                    >
                        <el-button size="small" @click="debugForceRerender" type="warning">强制重新渲染</el-button>
                    </el-tooltip>
                </div>
            </div>
            <div class="advanced-avatar-container">
                <!-- 图像裁剪区域 -->
                <div class="cropper-container-wrapper">
                    <div class="image-container">
                        <div v-if="!advancedAvatarFile" class="placeholder">
                            <el-upload
                                class="advanced-uploader"
                                action="#"
                                :auto-upload="false"
                                :show-file-list="false"
                                :on-change="handleAdvancedAvatarChange"
                                :drag="true">
                                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                                <div class="upload-text">拖拽或点击上传图片</div>
                            </el-upload>
                        </div>
                        <!-- 注意：这里更改了图片的包装方式以适应Cropper 2.0.0 -->
                        <div v-if="advancedAvatarFile" class="cropper-wrapper">
                            <img ref="cropperImage" :src="advancedImageUrl" alt="待裁剪图片" class="cropper-img" 
                                 :style="{ 'transform': `rotate(${currentRotation.value}deg)` }">
                            <div class="debug-info">图片元素是否存在: {{ cropperImage ? '是' : '否' }}</div>
                        </div>
                    </div>
                </div>
                
                <!-- 控制面板区域 -->
                <div class="controls-container" v-if="advancedAvatarFile">
                    <!-- 预览区域 -->
                    <div class="preview-container">
                        <h4>预览效果</h4>
                        <div class="avatar-preview">
                            <img v-if="croppedImageUrl" :src="croppedImageUrl" alt="预览">
                        </div>
                    </div>
                    
                    <!-- 工具按钮 -->
                    <div class="tool-buttons">
                        <el-button-group class="rotate-buttons">
                            <el-button @click="rotateLeft" size="small" type="success" style="flex: 1;">
                                <el-icon><refresh-left /></el-icon>
                                <span>向左旋转</span>
                            </el-button>
                            <el-button @click="rotateRight" size="small" type="success" style="flex: 1;">
                                <el-icon><refresh-right /></el-icon>
                                <span>向右旋转</span>
                            </el-button>
                        </el-button-group>
                    </div>
                    
                    <!-- 质量控制 -->
                    <div class="quality-control">
                        <span>质量:</span>
                        <el-slider 
                            v-model="imageQuality" 
                            :min="10" 
                            :max="100" 
                            :step="5"
                            @change="updateCropper"
                            show-stops>
                        </el-slider>
                        <span>{{ imageQuality }}%</span>
                    </div>
                    
                    <!-- 滤镜选择 -->
                    <div class="filter-selection">
                        <span>滤镜效果:</span>
                        <el-radio-group v-model="imageFilter" @change="updateCropper">
                            <el-radio value="none">无</el-radio>
                            <el-radio value="sepia">复古</el-radio>
                            <el-radio value="bw">黑白</el-radio>
                            <el-radio value="brightness">明亮</el-radio>
                            <el-radio value="contrast">对比度</el-radio>
                        </el-radio-group>
                    </div>
                    
                    <!-- 滤镜强度 -->
                    <div class="filter-intensity" v-if="imageFilter !== 'none'">
                        <span>滤镜强度:</span>
                        <el-slider 
                            v-model="filterIntensity" 
                            :min="0" 
                            :max="1" 
                            :step="0.1"
                            @change="updateCropper">
                        </el-slider>
                        <span>{{ Math.round(filterIntensity * 100) }}%</span>
                    </div>
                    
                    <!-- 图像信息 -->
                    <div class="image-info" v-if="imageMetadata">
                        <h4>图像信息</h4>
                        <p v-if="imageMetadata.original_size">原始大小: {{ (imageMetadata.original_size / 1024).toFixed(1) }} KB</p>
                        <p v-if="imageMetadata.compressed_size">压缩后: {{ (imageMetadata.compressed_size / 1024).toFixed(1) }} KB</p>
                        <p v-if="imageMetadata.size_reduction">压缩率: {{ imageMetadata.size_reduction }}</p>
                        <p v-if="imageMetadata.dimensions">尺寸: {{ imageMetadata.dimensions }}</p>
                    </div>
                    
                    <!-- 操作按钮 -->
                    <div class="action-buttons">
                        <el-button @click="uploadCroppedAvatar" type="primary">确认上传</el-button>
                        <el-button @click="resetCropper">重置</el-button>
                        <el-button @click="closeAdvancedAvatarEditor">取消</el-button>
                    </div>
                </div>
            </div>
        </el-dialog>

        <!-- 高级头像编辑区域 -->
        <div v-if="advancedMode" class="advanced-editor">
          <div class="cropper-wrapper">
            <img 
              v-if="advancedImageUrl" 
              :src="advancedImageUrl" 
              class="cropper-img" 
              ref="advancedImage"
              :style="{ transform: `rotate(${rotationAngle}deg)` }"
            />
            <div v-else class="upload-placeholder">
              <el-icon><upload-filled /></el-icon>
              <span>请选择图片</span>
            </div>
          </div>
          
          <div class="rotation-controls">
            <el-button-group style="width: 100%;">
              <el-button type="primary" @click="rotateLeft" style="flex: 1;">
                <el-icon><back /></el-icon>向左旋转
              </el-button>
              <el-button type="primary" @click="rotateRight" style="flex: 1;">
                <el-icon><right /></el-icon>向右旋转
              </el-button>
            </el-button-group>
          </div>
          
          <div class="tool-buttons">
            <el-button-group>
              <el-button type="primary" @click="handleAdvancedFileChange">
                <el-icon><picture-outline /></el-icon>选择图片
              </el-button>
              <el-button type="success" @click="cropImage" :disabled="!advancedImageUrl">
                <el-icon><crop /></el-icon>裁剪图片
              </el-button>
              <el-button type="danger" @click="uploadAdvancedAvatar" :disabled="!croppedImageUrl">
                <el-icon><upload /></el-icon>上传头像
              </el-button>
            </el-button-group>
          </div>
          
          <input 
            type="file" 
            ref="advancedFileInput" 
            style="display: none" 
            accept="image/*" 
            @change="handleAdvancedUpload"
          />
          
          <div v-if="croppedImageUrl" class="preview-area">
            <h4>预览</h4>
            <img :src="croppedImageUrl" class="preview-img" />
          </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index'
import { onMounted, reactive, ref, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowDown, UploadFilled, ZoomIn, ZoomOut, RefreshLeft, RefreshRight, Back, Right, PictureOutline, Crop, Upload, Menu } from '@element-plus/icons-vue'
// 确保导入所有需要的图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// 导入Cropper.js
import Cropper from 'cropperjs'
// 引入自定义的Cropper样式
import '@/assets/cropper.css'

// 菜单图标映射
const iconMapping = {
    '1': 'User',
    '2': 'Tools',
    '3': 'Shop',
    '4': 'ShoppingCart',
    '5': 'PieChart',
}

// 菜单列表 - 使用ref
const menuList = ref([])

// 头像上传相关变量
const avatarFile = ref(null)
const previewUrl = ref('')
const showAvatarDialog = ref(false)
const showAvatarPreview = ref(false)

// 高级头像编辑相关变量
const showAdvancedAvatarDialog = ref(false)
const advancedAvatarFile = ref(null)
const advancedImageUrl = ref('')
const croppedImageUrl = ref('')
const cropperImage = ref(null)
const cropper = ref(null)
const imageQuality = ref(85)
const imageFilter = ref('none')
const filterIntensity = ref(0.5)
const currentRotation = ref(0)
const imageMetadata = ref(null)
const imageSize = ref(null)
const advancedMode = ref(false)
const rotationAngle = ref(0)
const advancedFileInput = ref(null)
const advancedImage = ref(null)

// 权限相关变量
const hasAddPermission = ref(false)
const hasEditPermission = ref(false)
const hasDeletePermission = ref(false)

// 用户信息对象
const userInfo = reactive({
    id: null,
    username: '',
    nick_name: '',
    role_name: '',
    role_desc: '游客',
    avatar: 'http://localhost:5000/static/avatar/init.png'
})

// 在组件挂载时获取菜单和用户信息
onMounted(() => {
    loadUserMenu()
    getUserInfo()
    
    // 确保Cropper.js工具按钮显示正确
    if (showAdvancedAvatarDialog.value && advancedAvatarFile.value) {
        nextTick(() => {
            initCropper()
        })
    }
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
    } else if (command === 'advancedAvatar') {
        showAdvancedAvatarDialog.value = true
        // 初始化操作移至onDialogOpen函数
    }
}

// 对话框打开时的处理函数
const onDialogOpen = () => {
    console.log('高级头像编辑对话框已打开')
    
    // 如果已经有选择的图片，在对话框显示后重新初始化裁剪器
    if (advancedAvatarFile.value) {
        console.log('对话框打开时已有图片，即将初始化裁剪器')
        // 等待DOM完全渲染
        nextTick(() => {
            setTimeout(() => {
                console.log('延迟初始化裁剪器')
                initCropper()
            }, 300) // 增加延迟时间，确保DOM已完全渲染
        })
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

// 高级头像编辑处理函数
const handleAdvancedAvatarChange = (file) => {
    console.log('文件选择事件触发', file)
    
    const isImage = file.raw.type.startsWith('image/')
    const isLt5M = file.raw.size / 1024 / 1024 < 5
    
    if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return
    }
    if (!isLt5M) {
        ElMessage.error('图片大小不能超过5MB!')
        return
    }
    
    console.log('文件检查通过，准备设置头像文件')
    advancedAvatarFile.value = file.raw
    console.log('已设置advancedAvatarFile', advancedAvatarFile.value)
    
    // 创建URL
    advancedImageUrl.value = URL.createObjectURL(file.raw)
    console.log('已创建图片URL', advancedImageUrl.value)
    
    // 等待图像加载完成后初始化显示
    console.log('等待nextTick初始化图像显示')
    nextTick(() => {
        console.log('nextTick回调执行')
        setTimeout(() => {
            console.log('延迟300ms后初始化图像显示')
            // 使用正确的初始化函数
            initCropperInstance()
            
            // 立即生成预览图像
            updateCropper()
        }, 300) // 增加延迟时间，确保DOM完全渲染
    })
}

// 初始化Cropper
const initCropper = () => {
    console.log('开始初始化Cropper')
    console.log('cropperImage元素:', cropperImage.value)
    console.log('advancedAvatarFile:', advancedAvatarFile.value)
    console.log('advancedImageUrl:', advancedImageUrl.value)
    
    // 检查图像尺寸
    if (cropperImage.value) {
        const img = cropperImage.value;
        imageSize.value = {
            naturalWidth: img.naturalWidth || 0,
            naturalHeight: img.naturalHeight || 0,
            clientWidth: img.clientWidth || 0,
            clientHeight: img.clientHeight || 0,
            offsetWidth: img.offsetWidth || 0,
            offsetHeight: img.offsetHeight || 0
        }
        console.log('图像尺寸:', imageSize.value)
        
        // 检查图像是否已加载
        if (!img.complete) {
            console.log('图像尚未完全加载，添加加载事件监听器')
            img.onload = () => {
                console.log('图像已加载完成，重新获取尺寸')
                imageSize.value = {
                    naturalWidth: img.naturalWidth || 0,
                    naturalHeight: img.naturalHeight || 0,
                    clientWidth: img.clientWidth || 0,
                    clientHeight: img.clientHeight || 0,
                    offsetWidth: img.offsetWidth || 0,
                    offsetHeight: img.offsetHeight || 0
                }
                console.log('图像加载后尺寸:', imageSize.value)
                // 图像加载完成后再初始化Cropper
                initCropperInstance()
            }
            return
        }
    }
    
    initCropperInstance()
}

// 实际初始化Cropper实例的函数
const initCropperInstance = () => {
    // 简单显示图像，不初始化裁剪器
    console.log('初始化图像显示')
    if (cropperImage.value) {
        cropperImage.value.style.display = 'block';
        cropperImage.value.style.maxWidth = '100%';
        cropperImage.value.style.maxHeight = '100%';
    }
}

// 更新裁剪预览 - 简化为直接使用原图
const updateCropper = async () => {
    if (!advancedAvatarFile.value) return;
    
    try {
        // 使用简单的预览模式
        const response = await api.process_avatar(advancedAvatarFile.value, {
            cropData: null, // 不使用裁剪，使用整个图像
            rotate: currentRotation.value,
            quality: imageQuality.value,
            filter: imageFilter.value === 'none' ? null : imageFilter.value,
            filterIntensity: filterIntensity.value,
            preview: true,
            size: 400 // 预览尺寸
        });
        
        if (response.data.status === 200) {
            // 更新预览图像
            croppedImageUrl.value = response.data.data.preview
            
            // 更新图像元数据
            imageMetadata.value = {
                original_size: response.data.data.original_size,
                compressed_size: response.data.data.compressed_size,
                size_reduction: response.data.data.size_reduction,
                dimensions: response.data.data.dimensions
            }
        } else {
            ElMessage.error(response.data.msg || '预览生成失败')
        }
    } catch (error) {
        console.error('预览错误:', error)
        ElMessage.error('生成预览失败，请重试')
    }
}

// 旋转操作
const rotateLeft = () => {
    // 更新旋转角度
    currentRotation.value = (currentRotation.value - 90) % 360;
    
    // 直接设置图像旋转，不依赖Cropper API
    if (cropperImage.value) {
        // 应用旋转样式
        cropperImage.value.style.transform = `rotate(${currentRotation.value}deg)`;
        
        // 更新预览图像
        updateCropper();
    }
}

const rotateRight = () => {
    // 更新旋转角度
    currentRotation.value = (currentRotation.value + 90) % 360;
    
    // 直接设置图像旋转，不依赖Cropper API
    if (cropperImage.value) {
        // 应用旋转样式
        cropperImage.value.style.transform = `rotate(${currentRotation.value}deg)`;
        
        // 更新预览图像
        updateCropper();
    }
}

// 重置裁剪器
const resetCropper = () => {
    // 重置旋转和滤镜设置
    currentRotation.value = 0;
    imageQuality.value = 85;
    imageFilter.value = 'none';
    filterIntensity.value = 0.5;
    
    // 重置图像样式
    if (cropperImage.value) {
        cropperImage.value.style.transform = `rotate(0deg)`;
    }
    
    // 更新预览
    updateCropper();
}

// 上传裁剪后的头像
const uploadCroppedAvatar = async () => {
    if (!advancedAvatarFile.value) {
        ElMessage.warning('请先选择头像图片')
        return
    }
    
    try {
        // 使用简单的上传模式
        const response = await api.process_avatar(advancedAvatarFile.value, {
            cropData: null, // 不使用裁剪，使用整个图像
            rotate: currentRotation.value,
            quality: imageQuality.value,
            filter: imageFilter.value === 'none' ? null : imageFilter.value,
            filterIntensity: filterIntensity.value,
            size: 400 // 最终头像尺寸
        });
        
        if (response.data.status === 200) {
            ElMessage.success('头像上传成功')
            
            // 更新头像显示
            const avatarUrl = response.data.data.avatar
            userInfo.avatar = 'http://localhost:5000' + avatarUrl
            
            // 关闭对话框
            closeAdvancedAvatarEditor()
        } else {
            ElMessage.error(response.data.msg || '上传失败')
        }
    } catch (error) {
        console.error('上传头像错误:', error)
        ElMessage.error('上传头像失败，请稍后再试')
    }
}

// 关闭高级头像编辑器 - 移除对Cropper API的依赖
const closeAdvancedAvatarEditor = () => {
    showAdvancedAvatarDialog.value = false
    
    // 不再使用Cropper API
    cropper.value = null
    
    // 清理资源
    advancedAvatarFile.value = null
    if (advancedImageUrl.value && advancedImageUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(advancedImageUrl.value)
    }
    advancedImageUrl.value = ''
    croppedImageUrl.value = ''
    imageMetadata.value = null
    currentRotation.value = 0
    imageQuality.value = 85
    imageFilter.value = 'none'
    filterIntensity.value = 0.5
}

// 加载用户菜单
const loadUserMenu = async () => {
    try {
        // 先尝试获取用户权限菜单
        const permRes = await api.getUserPermissions()
        console.log('获取用户权限菜单响应:', permRes)
        
        if (permRes?.data?.status === 200 && permRes.data.data && permRes.data.data.menus && permRes.data.data.menus.length > 0) {
            // 如果成功获取用户权限菜单
            menuList.value = permRes.data.data.menus
            console.log('已加载用户权限菜单:', menuList.value)
            
            // 打印菜单结构，帮助调试多级菜单
            console.log('菜单结构详情:')
            menuList.value.forEach((item, index) => {
                console.log(`一级菜单${index+1}:`, item.name, '(ID:', item.id, ')')
                if (item.children && item.children.length > 0) {
                    item.children.forEach((subItem, subIndex) => {
                        console.log(`--二级菜单${subIndex+1}:`, subItem.name, '(ID:', subItem.id, ')')
                        if (subItem.children && subItem.children.length > 0) {
                            subItem.children.forEach((childItem, childIndex) => {
                                console.log(`----三级菜单${childIndex+1}:`, childItem.name, '(ID:', childItem.id, ')')
                            })
                        }
                    })
                }
            })
        } else {
            // 如果获取用户权限菜单失败，尝试获取所有菜单
            const menuRes = await api.get_menu_list()
            console.log('获取所有菜单响应:', menuRes)
            
            if (menuRes?.data?.status === 200) {
                menuList.value = menuRes.data.data || []
                console.log('已加载所有菜单:', menuList.value)
                
                // 打印菜单结构
                console.log('菜单结构详情:')
                menuList.value.forEach((item, index) => {
                    console.log(`一级菜单${index+1}:`, item.name, '(ID:', item.id, ')')
                    if (item.children && item.children.length > 0) {
                        item.children.forEach((subItem, subIndex) => {
                            console.log(`--二级菜单${subIndex+1}:`, subItem.name, '(ID:', subItem.id, ')')
                            if (subItem.children && subItem.children.length > 0) {
                                subItem.children.forEach((childItem, childIndex) => {
                                    console.log(`----三级菜单${childIndex+1}:`, childItem.name, '(ID:', childItem.id, ')')
                                })
                            }
                        })
                    }
                })
            } else {
                ElMessage.error('获取菜单失败')
            }
        }
    } catch (error) {
        console.error('加载菜单错误:', error)
        ElMessage.error('加载菜单失败，请检查网络连接')
    }
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
            userInfo.role_desc = data.role_desc || '游客'
            
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

// 组件卸载时清理资源
onUnmounted(() => {
    if (cropper.value) {
        cropper.value.destroy()
    }
    
    // 释放对象URL
    if (previewUrl.value && previewUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(previewUrl.value)
    }
    if (advancedImageUrl.value && advancedImageUrl.value.startsWith('blob:')) {
        URL.revokeObjectURL(advancedImageUrl.value)
    }
})

// 调试函数
const debugInitCropper = () => {
    console.log('开始调试初始化图像显示')
    
    // 显示图像并更新预览
    if (cropperImage.value && advancedImageUrl.value) {
        cropperImage.value.style.display = 'block';
        cropperImage.value.style.maxWidth = '100%';
        cropperImage.value.style.maxHeight = '100%';
        
        // 更新预览
        updateCropper();
    } else {
        console.warn('无法初始化图像，图像元素或URL不存在')
    }
}

// debugForceRerender 函数修复 - 移除Cropper API依赖
const debugForceRerender = () => {
    console.log('开始强制重新渲染')
    
    // 强制重新创建图像元素
    if (advancedAvatarFile.value) {
        // 先释放现有的URL
        if (advancedImageUrl.value && advancedImageUrl.value.startsWith('blob:')) {
            URL.revokeObjectURL(advancedImageUrl.value)
        }
        
        // 清除现有的Cropper实例
        cropper.value = null
        
        // 重新创建图像URL
        advancedImageUrl.value = URL.createObjectURL(advancedAvatarFile.value)
        console.log('重新创建的URL:', advancedImageUrl.value)
        
        // 等待下一个渲染周期
        nextTick(() => {
            // 设置一个更长的延迟，确保图像已加载
            setTimeout(() => {
                if (cropperImage.value) {
                    console.log('强制重新渲染后的图像元素:', cropperImage.value)
                    
                    // 检查图像尺寸
                    const img = cropperImage.value;
                    imageSize.value = {
                        naturalWidth: img.naturalWidth || 0,
                        naturalHeight: img.naturalHeight || 0,
                        clientWidth: img.clientWidth || 0,
                        clientHeight: img.clientHeight || 0,
                        offsetWidth: img.offsetWidth || 0,
                        offsetHeight: img.offsetHeight || 0
                    }
                    console.log('强制重新渲染后的图像尺寸:', imageSize.value)
                    
                    // 显示图像
                    initCropperInstance()
                } else {
                    console.error('强制重新渲染后仍找不到图像元素')
                }
            }, 500)
        })
    } else {
        console.warn('没有选择文件，无法强制重新渲染')
    }
}

// 高级头像编辑相关函数
const handleAdvancedFileChange = () => {
    if (advancedFileInput.value) {
        advancedFileInput.value.click()
    }
}

const handleAdvancedUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
        handleAdvancedAvatarChange({ raw: file })
    }
}

const cropImage = () => {
    if (cropper.value) {
        const canvas = cropper.value.getCroppedCanvas({
            width: 300,
            height: 300,
            minWidth: 100,
            minHeight: 100,
            maxWidth: 4096,
            maxHeight: 4096,
            fillColor: '#fff',
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high',
        })
        
        if (canvas) {
            // 转换为base64
            croppedImageUrl.value = canvas.toDataURL('image/jpeg', 0.9)
        }
    }
}

const uploadAdvancedAvatar = async () => {
    if (!croppedImageUrl.value) {
        ElMessage.warning('请先裁剪图片')
        return
    }
    
    try {
        // 创建FormData对象
        const formData = new FormData()
        // 从base64转换为Blob
        const blob = await fetch(croppedImageUrl.value).then(res => res.blob())
        formData.append('avatar', blob, 'avatar.jpg')
        
        // 上传
        const response = await fetch('/api/user/upload_avatar/', {
            method: 'POST',
            body: formData,
            credentials: 'include'
        }).then(res => res.json())
        
        if (response.status === 200) {
            ElMessage.success('头像上传成功')
            // 更新头像显示
            const avatarUrl = response.data.avatar
            userInfo.avatar = 'http://localhost:5000' + avatarUrl
            // 重置状态
            resetAdvancedEditor()
        } else {
            ElMessage.error(response.msg || '上传失败')
        }
    } catch (error) {
        console.error('上传头像错误:', error)
        ElMessage.error('上传头像失败，请稍后再试')
    }
}

const resetAdvancedEditor = () => {
    advancedImageUrl.value = ''
    croppedImageUrl.value = ''
    rotationAngle.value = 0
    
    // 不再使用Cropper API
    cropper.value = null
    
    advancedMode.value = false
}

const toggleAdvancedMode = () => {
    advancedMode.value = !advancedMode.value
    if (advancedMode.value) {
        nextTick(() => {
            if (advancedImageUrl.value) {
                // 调用正确的Cropper初始化函数
                initCropperInstance()
            }
        })
    } else {
        resetAdvancedEditor()
    }
}
</script>

<style lang="scss" scoped>
/* Cropperjs基本样式 */
.cropper-container {
  direction: ltr;
  font-size: 0;
  line-height: 0;
  position: relative;
  touch-action: none;
  user-select: none;
  max-width: 100%;
}

.cropper-container img {
  display: block;
  height: auto;
  image-orientation: 0deg;
  max-width: 100%;
  max-height: 100%;
}

.cropper-wrap-box,
.cropper-canvas,
.cropper-drag-box,
.cropper-crop-box,
.cropper-modal {
  bottom: 0;
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
}

.cropper-wrap-box,
.cropper-canvas {
  overflow: hidden;
}

.cropper-drag-box {
  background-color: #fff;
  opacity: 0;
}

.cropper-view-box {
  display: block;
  height: 100%;
  outline: 1px solid #39f;
  outline-color: rgba(51, 153, 255, 0.75);
  overflow: hidden;
  width: 100%;
}

.cropper-dashed {
  border: 0 dashed #eee;
  display: block;
  opacity: 0.5;
  position: absolute;
}

.cropper-dashed.dashed-h {
  border-bottom-width: 1px;
  border-top-width: 1px;
  height: calc(100% / 3);
  left: 0;
  top: calc(100% / 3);
  width: 100%;
}

.cropper-dashed.dashed-v {
  border-left-width: 1px;
  border-right-width: 1px;
  height: 100%;
  left: calc(100% / 3);
  top: 0;
  width: calc(100% / 3);
}

.cropper-center {
  display: block;
  height: 0;
  left: 50%;
  opacity: 0.75;
  position: absolute;
  top: 50%;
  width: 0;
}

.cropper-center::before,
.cropper-center::after {
  background-color: #eee;
  content: ' ';
  display: block;
  position: absolute;
}

.cropper-center::before {
  height: 1px;
  left: -3px;
  top: 0;
  width: 7px;
}

.cropper-center::after {
  height: 7px;
  left: 0;
  top: -3px;
  width: 1px;
}

.cropper-face,
.cropper-line,
.cropper-point {
  display: block;
  height: 100%;
  opacity: 0.1;
  position: absolute;
  width: 100%;
}

.cropper-face {
  background-color: #fff;
  left: 0;
  top: 0;
}

.cropper-line {
  background-color: #39f;
}

.cropper-line.line-e {
  cursor: ew-resize;
  right: -3px;
  top: 0;
  width: 5px;
}

.cropper-line.line-n {
  cursor: ns-resize;
  height: 5px;
  left: 0;
  top: -3px;
}

.cropper-line.line-w {
  cursor: ew-resize;
  left: -3px;
  top: 0;
  width: 5px;
}

.cropper-line.line-s {
  bottom: -3px;
  cursor: ns-resize;
  height: 5px;
  left: 0;
}

.cropper-point {
  background-color: #39f;
  height: 5px;
  opacity: 0.75;
  width: 5px;
}

.cropper-point.point-e {
  cursor: ew-resize;
  margin-top: -3px;
  right: -3px;
  top: 50%;
}

.cropper-point.point-n {
  cursor: ns-resize;
  left: 50%;
  margin-left: -3px;
  top: -3px;
}

.cropper-point.point-w {
  cursor: ew-resize;
  left: -3px;
  margin-top: -3px;
  top: 50%;
}

.cropper-point.point-s {
  bottom: -3px;
  cursor: s-resize;
  left: 50%;
  margin-left: -3px;
}

.cropper-point.point-ne {
  cursor: nesw-resize;
  right: -3px;
  top: -3px;
}

.cropper-point.point-nw {
  cursor: nwse-resize;
  left: -3px;
  top: -3px;
}

.cropper-point.point-sw {
  bottom: -3px;
  cursor: nesw-resize;
  left: -3px;
}

.cropper-point.point-se {
  bottom: -3px;
  cursor: nwse-resize;
  right: -3px;
}

.cropper-move {
  cursor: move;
}

.cropper-crop {
  cursor: crosshair;
}

.cropper-modal {
  background-color: #000;
  opacity: 0.5;
}

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

/* 添加高级头像编辑相关样式 */
.advanced-avatar-container {
  display: flex;
  flex-direction: row;
  gap: 20px;
  min-height: 450px; /* 确保有足够的高度 */
}

.cropper-container-wrapper {
  flex: 3;
  min-width: 300px; /* 确保有足够的宽度 */
}

.image-container {
  width: 100%;
  height: 400px;
  position: relative;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 20px; /* 添加底部边距 */
}

.placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.controls-container {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  max-width: 300px;
}

.preview-container {
  text-align: center;
  margin-bottom: 15px;
}

.avatar-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto;
  border: 2px solid #409eff;
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tool-buttons, .quality-control, .filter-selection, .image-info, .action-buttons {
  margin-bottom: 15px;
}

.tool-buttons {
  margin-bottom: 20px;
}

.rotate-buttons {
  display: flex;
  width: 100%;
  
  .el-button {
    flex: 1;
    transition: all 0.2s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
  }
}

.tool-buttons .el-icon {
  margin-right: 0;
  font-size: 16px;
}

.filter-intensity {
  margin-top: 10px;
}

.image-info {
  padding: 10px;
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.image-info h4, .preview-container h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #606266;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
}

.advanced-uploader {
  width: 100%;
  height: 100%;
}

.advanced-uploader .el-icon--upload {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 10px;
}

.upload-text {
  color: #606266;
  font-size: 14px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .advanced-avatar-container {
    flex-direction: column;
  }
  
  .image-container {
    height: 300px;
  }
  
  .avatar-preview {
    width: 150px;
    height: 150px;
  }
}

/* 图像容器和裁剪区 */
.cropper-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  border: 2px dashed #409eff;
  background-color: #f8f9fa;
  
  &:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: repeating-linear-gradient(
      45deg,
      rgba(0, 0, 0, 0.03),
      rgba(0, 0, 0, 0.03) 10px,
      rgba(0, 0, 0, 0.06) 10px,
      rgba(0, 0, 0, 0.06) 20px
    );
    z-index: 0;
  }
}

.cropper-img {
  max-width: 100%;
  max-height: 100%;
  display: block;
  transition: transform 0.3s ease;
  position: relative;
  z-index: 1;
}

/* 调试面板样式 */
.debug-panel {
  background-color: #f2f6fc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  font-size: 12px;
  color: #303133;
  border: 1px solid #dcdfe6;
}

.debug-panel div {
  margin-bottom: 5px;
}

.debug-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px;
  font-size: 12px;
  text-align: center;
}

.avatar-cropper-container {
  position: relative;
  width: 100%;
  height: 360px;
  overflow: hidden;
  background-color: #f0f0f0;
  margin-bottom: 20px;
  border-radius: 4px;
  
  // 确保在旋转时有足够空间
  max-width: 100%;
  max-height: 60vh;
}

.avatar-dialog {
  .el-dialog__body {
    padding: 10px 20px;
    max-height: 85vh;
    overflow-y: auto;
  }
  
  .el-dialog__header {
    padding: 15px 20px 10px;
  }
  
  // 使对话框响应式
  @media (max-width: 768px) {
    width: 95% !important;
    margin: 0 auto !important;
    
    .avatar-cropper-container {
      height: 280px;
    }
    
    .filter-selector {
      flex-wrap: wrap;
      
      .filter-item {
        width: calc(33.33% - 10px);
        margin-bottom: 10px;
      }
    }
  }
}

.rotation-controls {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
  gap: 10px;
  
  .el-button {
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    
    &:hover {
      transform: scale(1.05);
    }
    
    .el-icon {
      font-size: 16px;
      margin-right: 4px;
    }
  }
}

.slider-container {
  margin: 15px 0;
}

/* 高级头像编辑区域 */
.advanced-editor {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.preview-area {
  margin-top: 20px;
  text-align: center;
}

.preview-img {
  max-width: 150px;
  max-height: 150px;
  object-fit: cover;
}
</style>
