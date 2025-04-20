<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>分类列表</el-breadcrumb-item>

    </el-breadcrumb>

    <el-card class="box-card">
        <el-row>
            <el-button type="primary" @click="addCategoryDialog" :icon="CirclePlus">添加分类</el-button>
        </el-row>

        <el-row><!-- default-expand-all -->
            <el-table :data="tableData.data" style="width: 100%; margin-bottom: 20px" row-key="id" border>
                <el-table-column prop="id" label="id" width="120"></el-table-column>
                <el-table-column prop="name" label="名称" sortable />
                <el-table-column prop="level" label="分类等级" sortable>
                    <template #default="scope">
                        <el-tag v-if="scope.row.level == 1" type="primary">一级分类</el-tag>
                        <el-tag v-else-if="scope.row.level == 2" type="success">二级分类</el-tag>
                        <el-tag v-else-if="scope.row.level == 3" type="danger">三级分类</el-tag>

                    </template>

                </el-table-column>
                <el-table-column label="操作" sortable>
                    <template #default="scope">
                        <!-- <el-button type="primary" :icon="Edit">编辑</el-button> -->
                        <el-button type="danger" :icon="Delete" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                    </template>


                </el-table-column>
            </el-table>
        </el-row>

    </el-card>

    <!-- 增加分类 -->
    <el-dialog v-model="addDialogVisible" title="新增分类">
        <el-form :model="addForm" ref="addFormRef" :rules="addRules">
            <el-form-item label="名称" prop="name">
                <el-input v-model="addForm.name" placeholder="请输入名称"></el-input>

            </el-form-item>
            <el-form-item label="父级分类" prop="parent_id">
                <el-cascader v-model="value" :options="options.data" :props="props" @change="handleChange"
                    separator=" > " placeholder="请选择父级分类" clearable>
                </el-cascader>


            </el-form-item>
            <el-form-item>


                <el-button type="primary" @click="addcategory">提交</el-button>
                <el-button type="default" @click="addDialogVisible = false">取消</el-button>


            </el-form-item>



        </el-form>
    </el-dialog>

    <!-- 编辑分类 -->


</template>





<script setup>
import { ArrowRight, CirclePlus } from '@element-plus/icons-vue'
import { ref,reactive,onMounted } from 'vue'
import api from '@/api/index.js'
import { Edit, Delete } from '@element-plus/icons-vue'










const tableData = reactive({
    data:[]

})
//用于展示新增分类的弹窗是否显示
let addDialogVisible = ref(false)
//增加分类
const addForm = reactive({
    name:'',
    parent_id:0,
    level:1
})
const addFormRef = ref(null)
let addRules = reactive({
    name: [
        { required: true, message: '请输入分类名称', trigger: 'blur' },
        { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
    ]
})



//级联选择器
const value = ref([])
const props = {
  expandTrigger: 'hover',
  value: 'id',
  label: 'name',
  checkStrictly: true,//父子级联选择器是否严格的遵循父子级联关系，设置为true的时候父级不能选择子集，false的时候父级可以选择任意子集。
}
const handleChange = (value) => {
    
      //console.log(value)
    if (value) {
        if (value.length == 1) {
            addForm.parent_id = value[0]
            addForm.level = 2
        } else if (value.length == 2) {
            addForm.parent_id = value[1]
            addForm.level = 3
        }
    } else {
        addForm.parent_id = 0
        addForm.level = 1
    }
    //console.log(addForm)
}

const options = reactive({
    data:[],
   
})


//刷新页面时开始调用
onMounted(() => {
    get_category()
    get_options()
})


const get_category = () => {
    api.get_category_list(3).then(res => {
        //console.log(res)
        tableData.data = res.data.data

    })
}
//在添加按钮上点击时触发，显示出dialog弹出框
const addCategoryDialog = () => {
    addDialogVisible.value = true
}
//获取options数据
const get_options = () => {
    api.get_category_list(2).then(res => {
        //console.log(res)
        options.data = res.data.data
    })
}
//点击提交后，调用接口添加分类
const addcategory = () => {
    // 调用 API 接口添加分类
    api.add_category(addForm).then(res => {
        //console.log(res);
        
        // 检查响应的状态
        if (res.data.status === 200) {
            // 关闭对话框
            addDialogVisible.value = false;

            // 刷新页面数据
            get_category(); // 刷新分类列表
            get_options(); // 刷新选择框选项数据
            
            // 显示成功消息
            ElMessage({
                type: 'success',
                message:res.data.msg || '添加分类成功',
            });
        } else {
            // 如果添加失败，显示警告消息
            ElMessage.warning({
                showClose: true,
                message: res.data.msg || '添加分类失败，请重试'
            });
        }
    }).catch(error => {
        // 捕获 API 请求失败的错误
        console.error(error);
        ElMessage.error('请求失败，请稍后重试');
    });
};


//
const handleDelete = (index,row) => {
   
    //console.log(row)
    let name=row.name
    let id=row.id
    //console.log(index)页面的索引
    //删除角色分类

  ElMessageBox.confirm(
    '确认要删除' + name + '的权限吗?',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
    
  )
    .then(() => {
      
      api.del_category(id).then(res => {
        if (res.data.status == 200) {
            ElMessage({
                type: 'success',
                message: '删除' + name + '的成功',
            })
            //console.log(res)
        //删除之后，刷新页面，就不再显示删除之后的数据了
        get_category()

        } else {
            {
                ElMessage.warning({
                    showClose: true,
                    message: res.data.msg
                });
                // console.log(res.data.msg)
            }
        }

      })


    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '已取消删除',
      })
    })
}





</script>




<style scoped>
.box-card {
    margin-top: 20px;
}
</style>