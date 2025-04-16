<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人资料</h1>
    </div>
    
    <el-card class="profile-card">
      <div class="avatar-container">
        <div class="avatar-wrapper">
          <!-- 使用懒加载处理头像 -->
          <img 
            ref="avatarImage"
            class="avatar lazy-image"
            :data-src="userInfo.avatar || defaultAvatar" 
            src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
            alt="用户头像"
          />
          <div class="avatar-loading" ref="loadingIndicator">
            <i class="el-icon-loading"></i>
          </div>
        </div>
        <div class="avatar-actions">
          <el-button type="primary" size="small" @click="showUploadDialog">更换头像</el-button>
        </div>
      </div>
      
      <div class="user-info">
        <div class="info-item">
          <span class="label">用户名:</span>
          <span class="value">{{ userInfo.username }}</span>
        </div>
        <div class="info-item">
          <span class="label">邮箱:</span>
          <span class="value">{{ userInfo.email }}</span>
        </div>
        <div class="info-item">
          <span class="label">手机:</span>
          <span class="value">{{ userInfo.mobile }}</span>
        </div>
        <div class="info-item">
          <span class="label">注册时间:</span>
          <span class="value">{{ formatDate(userInfo.reg_date) }}</span>
        </div>
        <div class="info-item">
          <span class="label">上次登录:</span>
          <span class="value">{{ formatDate(userInfo.last_login) }}</span>
        </div>
      </div>
      
      <div class="profile-actions">
        <el-button type="primary" @click="editProfile">编辑资料</el-button>
      </div>
    </el-card>
    
    <!-- 上传头像对话框 -->
    <el-dialog
      title="上传头像"
      :visible.sync="dialogVisible"
      width="500px"
    >
      <div class="avatar-upload">
        <el-upload
          class="upload-area"
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleFileChange"
        >
          <img v-if="imageUrl" :src="imageUrl" class="preview" />
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          <div class="upload-text" v-if="!imageUrl">点击上传头像</div>
        </el-upload>
        
        <div class="image-settings" v-if="imageUrl">
          <div class="setting">
            <span>图片大小:</span>
            <el-slider v-model="imageSize" :min="100" :max="800" :step="50"></el-slider>
            <span>{{ imageSize }}px</span>
          </div>
          <div class="setting">
            <span>图片质量:</span>
            <el-slider v-model="imageQuality" :min="40" :max="100" :step="5"></el-slider>
            <span>{{ imageQuality }}%</span>
          </div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="uploadAvatar" :disabled="!imageFile">上传</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { formatDate } from '@/utils/format'

export default {
  name: 'ProfileView',
  data() {
    return {
      userInfo: {
        username: '',
        email: '',
        mobile: '',
        avatar: '',
        reg_date: '',
        last_login: ''
      },
      defaultAvatar: '/static/images/default_avatar.png',
      dialogVisible: false,
      imageUrl: '',
      imageFile: null,
      imageSize: 300,
      imageQuality: 85,
      observer: null
    }
  },
  created() {
    this.getUserInfo()
  },
  mounted() {
    // 设置IntersectionObserver实现懒加载
    this.setupLazyLoading()
  },
  beforeDestroy() {
    // 清理observer
    if (this.observer) {
      this.observer.disconnect()
    }
  },
  methods: {
    formatDate,
    async getUserInfo() {
      try {
        const { data: res } = await axios.get('api/users/profile')
        if (res.meta.status === 200) {
          this.userInfo = res.data
        } else {
          this.$message.error('获取用户信息失败')
        }
      } catch (error) {
        console.error('获取用户信息出错:', error)
        this.$message.error('网络错误，请稍后重试')
      }
    },
    setupLazyLoading() {
      // 创建IntersectionObserver实例
      this.observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target
            const src = img.getAttribute('data-src')
            
            // 显示加载指示器
            if (this.$refs.loadingIndicator) {
              this.$refs.loadingIndicator.style.display = 'flex'
            }
            
            // 创建一个新的Image对象进行预加载
            const tempImg = new Image()
            tempImg.onload = () => {
              // 图片加载完成后，设置实际图片并隐藏loading
              img.src = src
              if (this.$refs.loadingIndicator) {
                this.$refs.loadingIndicator.style.display = 'none'
              }
            }
            tempImg.onerror = () => {
              // 加载失败时，使用默认头像
              img.src = this.defaultAvatar
              if (this.$refs.loadingIndicator) {
                this.$refs.loadingIndicator.style.display = 'none'
              }
              this.$message.error('头像加载失败')
            }
            tempImg.src = src
            
            // 图片开始加载后，取消观察
            this.observer.unobserve(img)
          }
        })
      }, {
        threshold: 0.1 // 当10%的图片进入可视区域时触发
      })
      
      // 开始观察头像元素
      if (this.$refs.avatarImage) {
        this.observer.observe(this.$refs.avatarImage)
      }
    },
    showUploadDialog() {
      this.dialogVisible = true
      this.imageUrl = ''
      this.imageFile = null
    },
    handleFileChange(file) {
      this.imageFile = file.raw
      
      if (this.imageFile) {
        // 检查文件类型
        if (!['image/jpeg', 'image/png', 'image/gif'].includes(this.imageFile.type)) {
          this.$message.error('请上传JPG/PNG/GIF格式的图片')
          this.imageFile = null
          return false
        }
        
        // 检查文件大小（小于2MB）
        if (this.imageFile.size / 1024 / 1024 > 2) {
          this.$message.error('图片大小不能超过2MB')
          this.imageFile = null
          return false
        }
        
        // 预览
        this.imageUrl = URL.createObjectURL(this.imageFile)
      }
    },
    async uploadAvatar() {
      if (!this.imageFile) {
        this.$message.error('请先选择图片')
        return
      }
      
      const formData = new FormData()
      formData.append('avatar', this.imageFile)
      formData.append('size', this.imageSize)
      formData.append('quality', this.imageQuality)
      
      try {
        const { data: res } = await axios.post('/api/user/upload_avatar/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (res.meta.status === 201) {
          this.$message.success('头像上传成功')
          this.dialogVisible = false
          
          // 更新头像
          this.userInfo.avatar = res.data.avatar_url + '?t=' + new Date().getTime() // 添加时间戳防止缓存
          
          // 重新设置懒加载
          if (this.$refs.avatarImage) {
            this.$refs.avatarImage.setAttribute('data-src', this.userInfo.avatar)
            this.setupLazyLoading()
          }
        } else {
          this.$message.error(res.meta.msg || '上传失败')
        }
      } catch (error) {
        console.error('上传头像出错:', error)
        this.$message.error('网络错误，请稍后重试')
      }
    },
    editProfile() {
      this.$message.info('编辑资料功能开发中...')
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 20px;
}

.profile-card {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.avatar-wrapper {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 15px;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  color: #409EFF;
  font-size: 24px;
}

.user-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.info-item {
  display: flex;
  align-items: center;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  width: 80px;
}

.value {
  color: #606266;
}

.profile-actions {
  display: flex;
  justify-content: center;
}

.avatar-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-area {
  text-align: center;
  margin-bottom: 20px;
}

.preview {
  width: 200px;
  height: 200px;
  border-radius: 5px;
  object-fit: cover;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 200px;
  height: 200px;
  line-height: 200px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 5px;
}

.upload-text {
  margin-top: 10px;
  color: #606266;
}

.image-settings {
  width: 100%;
  max-width: 400px;
}

.setting {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.setting span:first-child {
  width: 80px;
}

.setting .el-slider {
  flex: 1;
  margin: 0 15px;
}
</style>