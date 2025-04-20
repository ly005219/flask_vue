<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>权限管理</el-breadcrumb-item>
        <el-breadcrumb-item>我的权限</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 用户角色信息卡片 -->
    <el-card class="box-card" v-if="userRole">
        <template #header>
            <div class="card-header">
                <span>我的角色: {{ userRole.name }}</span>
            </div>
        </template>
        <p v-if="userRole.desc">描述: {{ userRole.desc }}</p>
    </el-card>
    
    <!-- 用户权限菜单卡片 -->
    <el-card class="box-card">
        <template #header>
            <div class="card-header">
                <span>我的权限菜单</span>
                <el-button type="primary" size="small" @click="getUserPermissions">刷新权限</el-button>
            </div>
        </template>
        
        <el-empty v-if="!userMenus || userMenus.length === 0" description="无权限菜单" />
        
        <el-row v-else>
            <el-table 
                :data="userMenus" 
                style="width: 100%" 
                row-key="id" 
                border 
                :tree-props="{ 
                    children: 'children',
                    hasChildren: 'hasChildren'
                }"
                :default-expand-all="true"
            >
                <el-table-column prop="name" label="菜单名称" width="180">
                    <template #default="scope">
                        <span :style="{ paddingLeft: scope.row.level === 2 ? '20px' : '0' }">
                            {{ scope.row.name }}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column prop="path" label="路径" width="180" />
                <el-table-column prop="level" label="菜单等级">
                    <template #default="scope">
                        <el-tag :type="scope.row.level === 1 ? 'primary' : 'success'">
                            {{ scope.row.level === 1 ? '一级' : '二级' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                    <template #default="scope">
                        <el-button 
                            v-if="scope.row.path"
                            type="primary" 
                            :icon="ArrowRight"
                            circle
                            @click="handleNavigate(scope.row)"
                        />
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/index'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 用户权限数据
const userRole = ref(null)
const userMenus = ref([])

// 页面加载时获取数据
onMounted(() => {
    getUserPermissions()
})

// 获取用户权限
const getUserPermissions = () => {
    api.getUserPermissions().then(res => {
        // console.log('用户权限数据:', res)
        if (res.data.status === 200) {
            userRole.value = res.data.data.role
            userMenus.value = res.data.data.menus
        } else {
            ElMessage.error(res.data.msg || '获取用户权限失败')
        }
    }).catch(error => {
        console.error('获取用户权限失败:', error)
        ElMessage.error('获取用户权限失败')
    })
}

// 处理页面跳转
const handleNavigate = (row) => {
    if (row.path) {
        router.push(row.path)
    } else {
        ElMessage.warning('该菜单项没有配置路径')
    }
}
</script>

<style scoped>
.box-card {
    margin-top: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>



