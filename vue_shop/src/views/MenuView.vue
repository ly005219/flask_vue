<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>权限管理</el-breadcrumb-item>
        <el-breadcrumb-item>权限列表</el-breadcrumb-item>

    </el-breadcrumb>

    <!-- 一个卡片 -->
    <el-card class="box-card">

        <el-row>

            <el-table :data="tableData.menulist" stripe style="width: 100%" class="table">
                <el-table-column prop="id" label="id"/>
                <el-table-column prop="name" label="名称"/>
                <el-table-column prop="path" label="路径" />
                <el-table-column prop="level" label="等级" >
                    <template #default="scope" >
                        <el-tag v-if="scope.row.level == 1" type="primary">一级</el-tag>
                        <el-tag v-else-if="scope.row.level == 2" type="success">二级</el-tag>
                    </template>

                </el-table-column>
            </el-table>

        </el-row>

    </el-card>


</template>




<script setup>
//面包屑的图标,搜索按钮的图标
import { ArrowRight } from '@element-plus/icons-vue'
import { reactive ,onMounted } from 'vue';
import api from '@/api/index'//导入api接口


const tableData = reactive({
    menulist: []
})
//页面渲染完加载
onMounted(() => {
    get_menu_list()
    
})
const get_menu_list = () => {
    //这里是获取菜单列表的接口
    api.get_menu_list().then(res => {
        console.log(res)
        tableData.menulist = res.data.data

    })

}




</script>




<style scoped>
.box-card {
    margin-top: 20px;
}





</style>



