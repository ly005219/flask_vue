<template>
  <div class="welcome-container">
    <!-- 顶部欢迎区域 -->
    <div class="welcome-header">
      <h1>欢迎使用电商后台管理系统</h1>
      <div class="time-info">
        <p>{{ currentTime }}</p>
        <p>{{ greeting }}</p>
      </div>
    </div>

    <!-- 数据概览卡片区域 -->
    <div class="data-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>商品总数</span>
                <el-icon><Goods /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>{{ statistics.products }}</h2>
              <p>较昨日 <span class="up">+10</span></p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>订单数量</span>
                <el-icon><List /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>{{ statistics.orders }}</h2>
              <p>较昨日 <span class="up">+5</span></p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>用户数量</span>
                <el-icon><User /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>{{ statistics.users }}</h2>
              <p>较昨日 <span class="up">+3</span></p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <span>总收入</span>
                <el-icon><Money /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h2>¥{{ statistics.income }}</h2>
              <p>较昨日 <span class="up">+1890</span></p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 快捷操作区域 -->
    <div class="quick-actions">
      <el-card class="action-card">
        <template #header>
          <div class="card-header">
            <span>快捷操作</span>
          </div>
        </template>
        <div class="action-buttons">
          <el-button type="primary" @click="$router.push('/add_product/')">
            <el-icon><Plus /></el-icon>添加商品
          </el-button>
          <el-button type="success" @click="$router.push('/order_list/')">
            <el-icon><List /></el-icon>查看订单
          </el-button>
          <el-button type="warning" @click="$router.push('/user_list/')">
            <el-icon><User /></el-icon>用户管理
          </el-button>
          <el-button type="info" @click="$router.push('/statistics_list/')">
            <el-icon><DataLine /></el-icon>数据统计
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 系统信息区域 -->
    <div class="system-info">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>系统信息</span>
          </div>
        </template>
        <div class="info-list">
          <p><span>系统版本：</span>{{ systemVersion }}</p>
          <p><span>上次登录：</span>{{ lastLoginTime || '加载中...' }}</p>
          <p><span>浏览器：</span>{{ browserInfo || '加载中...' }}</p>
          <p><span>操作系统：</span>{{ osInfo || '加载中...' }}</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Goods, List, User, Money, Plus, DataLine } from '@element-plus/icons-vue'
import api from '@/api/index'

// 统计数据
const statistics = ref({
  products: 1234,
  orders: 89,
  users: 456,
  income: '23,678.00'
})

// 时间相关
const currentTime = ref('')
const greeting = ref('')
const lastLoginTime = ref('')

// 系统信息
const browserInfo = ref('')
const osInfo = ref('')
const systemVersion = ref('v1.0.0')

// 更新时间和问候语
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString()
  const hour = now.getHours()
  if (hour < 12) {
    greeting.value = '早上好！开启愉快的一天'
  } else if (hour < 18) {
    greeting.value = '下午好！继续努力'
  } else {
    greeting.value = '晚上好！注意休息'
  }
}

// 获取系统信息
const getSystemInfo = () => {
  // 获取浏览器信息
  const userAgent = navigator.userAgent
  let browser = 'Unknown'
  if (userAgent.indexOf('Chrome') > -1) {
    browser = 'Chrome ' + userAgent.match(/Chrome\/(\d+\.\d+)/)[1]
  } else if (userAgent.indexOf('Firefox') > -1) {
    browser = 'Firefox ' + userAgent.match(/Firefox\/(\d+\.\d+)/)[1]
  } else if (userAgent.indexOf('Safari') > -1) {
    browser = 'Safari ' + userAgent.match(/Safari\/(\d+\.\d+)/)[1]
  }
  browserInfo.value = browser

  // 获取操作系统信息
  let os = 'Unknown'
  if (userAgent.indexOf('Win') > -1) {
    os = 'Windows'
  } else if (userAgent.indexOf('Mac') > -1) {
    os = 'MacOS'
  } else if (userAgent.indexOf('Linux') > -1) {
    os = 'Linux'
  }
  osInfo.value = os
}

// 获取上次登录时间
const getLastLoginTime = () => {
  const username = sessionStorage.getItem('username')
  if (username) {
    api.getLastLogin(username).then(res => {
      if (res.data.status === 200) {
        lastLoginTime.value = res.data.data.last_login || '暂无登录记录'
      }
    }).catch(err => {
      console.error('获取上次登录时间失败:', err)
      lastLoginTime.value = '获取失败'
    })
  }
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
  getSystemInfo()
  getLastLoginTime()
})
</script>

<style scoped>
.welcome-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
}

.welcome-header {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.welcome-header h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #409EFF;
}

.time-info {
  font-size: 16px;
  color: #606266;
}

.data-overview {
  margin-bottom: 30px;
}

.data-card {
  transition: all 0.3s;
}

.data-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  color: #303133;
}

.card-content {
  text-align: center;
}

.card-content h2 {
  font-size: 24px;
  color: #409EFF;
  margin: 10px 0;
}

.up {
  color: #67C23A;
}

.quick-actions {
  margin-bottom: 30px;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 15px;
}

.action-buttons .el-button {
  min-width: 120px;
}

.system-info .info-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.info-list p {
  margin: 0;
  color: #606266;
}

.info-list p span {
  color: #303133;
  font-weight: bold;
  margin-right: 10px;
}

@media screen and (max-width: 768px) {
  .system-info .info-list {
    grid-template-columns: 1fr;
  }
}
</style>
