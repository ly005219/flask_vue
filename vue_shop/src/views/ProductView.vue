<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>商品列表</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
        <!-- 一个搜索按钮 -->
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input v-model="product_data.queryName" placeholder="请输入要搜索的商品" @input="handleInput" clearable @clear="getProductList" @keyup.enter="getProductList">
                    <template #append>
                        <el-button :icon="Search" @click="getProductList" />
                    </template>
                </el-input>
            </el-col>
            <el-row>
                <el-button type="primary" :icon="CirclePlus" round plain @click="addProduct">添加商品</el-button>
            </el-row>
        </el-row>

        <el-row>
            <el-table :data="product_data.productList" style="width: 100%;margin-top: 15px;" stripe>
                <!-- 从数据库获取的数据首先会赋值到productList中，然后在el-table中显示,所以这里的prop要和数据库中字段名一致 -->
                <!-- 也就是prop绑定在:data中对应的数据字段,data里面的数据由数据库返回 -->
                <!-- <el-table-column type="index" width="50"></el-table-column> -->
                <el-table-column prop="id" label="id" width="120"></el-table-column>
                <el-table-column label="商品名称" prop="name" show-overflow-tooltip></el-table-column>
                <el-table-column label="商品价格" prop="price" width="150"></el-table-column>
                <el-table-column label="商品数量" prop="number" width="150"></el-table-column>
                <el-table-column label="商品状态" prop="state" width="150">

                    <template #default="scope">
                        <el-tag v-if="scope.row.state == 1" type="success">上架</el-tag>
                        <el-tag v-else-if="scope.row.state == -1" type="warning">下架</el-tag>
                        <el-tag v-else type="danger">预售</el-tag>
                    </template>
              


                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" @click="ProductEdit(scope.$index,scope.row)">编辑</el-button>
                        <el-button type="danger" @click="ProductDelete(scope.$index,scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>

        <!-- 编辑商品弹框 -->
         <el-dialog title="编辑商品" v-model="ProductEditDialogVisible" width="30%"  @closed="handleClose">
            <el-form  :model="productEditForm" >
                <el-form-item label="商品名称" prop="name">
                    <el-input v-model="productEditForm.name" clearable></el-input>
                </el-form-item>
                <el-form-item label="商品价格" prop="price">
                    <el-input v-model="productEditForm.price" clearable></el-input>
                </el-form-item>
                <el-form-item label="商品数量" prop="number">
                    <el-input v-model="productEditForm.number" clearable></el-input>
                </el-form-item>
                <el-form-item label="商品状态" prop="state">
                    <el-select v-model="productEditForm.state" placeholder="请选择商品状态">
                        <!-- value绑定在表单的state字段上,label是显示的选项 -->
                        <el-option label="上架" value="1"></el-option>
                        <el-option label="下架" value="-1"></el-option>
                        <el-option label="预售" value="0"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="ProductEditCancel">取 消</el-button>
                <el-button type="primary" @click="ProductEditSubmit">确 定</el-button>
            </div>
        </el-dialog>




    </el-card>
</template>

<script setup>
import { ArrowRight, Search, CirclePlus } from '@element-plus/icons-vue'
import { ref, reactive, onMounted } from 'vue'
import api from '@/api/index'
import { useRouter } from 'vue-router';


const addDialogVisible = ref(false)
const product_data = reactive({
    queryName: '',
    productList: []
})

//const lastQueryName = ref('') // 用于存储上一个 queryName 的值

onMounted(() => {
    getProductList()
})

const getProductList = () => {
    let params = {
        'name': product_data.queryName,//这个name是数据库中字段名,会直接携带这个name到接口里面
    }

    api.get_product_list({params}).then(res => {
        console.log(res)
        product_data.productList = res.data.data.data
    })
}

const handleInput = () => {
    if (product_data.queryName !== '') {
        getProductList()
    }else{
        getProductList()
    }
  
    //lastQueryName.value = product_data.queryName

}

//删除商品
const ProductDelete = (index, row) => {
    //index就是当前行的索引,0开始,row就包含当前行的所有数据,就是 :data product_data.productList = res.data.data.data后端里面数据库的值
    console.log(index, row)
    ElMessageBox.confirm('确认删除'+row.name+'商品吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        }).then(() => {
            api.del_product(row.id).then(res => {
                if (res.data.status == 200) {
                    //弹出框
                    ElMessage({
                        showClose: true,
                        message: res.data.msg,
                        type: 'success',
                    })

                    console.log(res)
                    //刷新查询显示商品数据页面
                    getProductList()

                    } else {
                        ElMessage.warning({
                            showClose: true,
                            message: res.data.msg});
                        // console.log(res.data.msg)
                    }
            })
        }).catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消删除'
            })
        })

}
const router = useRouter()
//点击添加商品按钮,跳转到添加商品页面
const addProduct = () => {
    router.push('/add_product/')
}



//编辑商品弹框
const ProductEditDialogVisible = ref(false)
const productEditForm = reactive({
    name: '',
    price: '',
    number: '',
    state: ''
})

const tmpdata = reactive({
    name: '',
    price: '',
    number: '',
    state: ''
    })

const productEditID = ref('')
const ProductEdit = (index, row) => {
    productEditForm.name = row.name
    productEditForm.price = row.price
    productEditForm.number = row.number
    productEditForm.state = row.state 


    ProductEditDialogVisible.value = true
    productEditID.value= row.id


    // 保存原始产品数据的变量
    tmpdata.name = row.name
    tmpdata.price = row.price
    tmpdata.number = row.number
    tmpdata.state = row.state

}
// 保存原始产品数据的变量

const ProductEditSubmit = () => {
    // 输出表单内容
    console.log(productEditForm)
    
    // 直接调用 API 接口进行更新
    api.update_product(productEditID.value, productEditForm).then(res => {
        if (res.data.status == 200) {
            // 弹出提示框
            ElMessage({
                showClose: true,
                message: res.data.msg,
                type: 'success',
            });

            console.log(res);
            // 刷新查询显示商品数据页面
            getProductList();

            // 关闭编辑对话框
            ProductEditDialogVisible.value = false;
        } else {
            // 如果返回的状态不是200，弹出警告信息
            ElMessage.warning({
                showClose: true,
                message: res.data.msg
            });
        }
    }).catch(error => {
        // 处理请求错误
        console.error(error);
        ElMessage.error({
            showClose: true,
            message: '更新失败，请填写所有信息并重试。'
        });
        productEditForm.name=tmpdata.name
        productEditForm.price=tmpdata.price
        productEditForm.number=tmpdata.number
        productEditForm.state=tmpdata.state


    });
}


const ProductEditCancel = () => {
    ProductEditDialogVisible.value = false
    //清空表单
    productEditForm.name = ''
    productEditForm.price = ''
    productEditForm.number = ''
    productEditForm.state = ''
    }


const handleClose = () => {
    addDialogVisible.value = false
   
    //清空表单
    productEditForm.name = ''
    productEditForm.price = ''
    productEditForm.number = ''
    productEditForm.state = ''
}


</script>

<style scoped>
.box-card {
    margin-top: 20px;
}
</style>
