<template>
    <!-- 一个面包屑导航路由 -->
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>商品列表</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
        <!-- 一个搜索按钮 -->
        <el-row :gutter="12" class="mb-4">
            <el-col :span="8">
                <el-input v-model="product_data.queryName" placeholder="请输入要搜索的商品" @input="handleInput" clearable @clear="getProductList" @keyup.enter="getProductList">
                    <template #append>
                        <el-button :icon="Search" @click="getProductList" />
                    </template>
                </el-input>
            </el-col>
            <el-col :span="16">
                <el-button type="primary" :icon="CirclePlus" round plain @click="addProduct">添加商品</el-button>
            </el-col>
        </el-row>

        <!-- 筛选条件 -->
        <el-row :gutter="20" class="mb-4">
            <el-col :span="8">
                <el-select v-model="product_data.sortBy" placeholder="排序方式" @change="getProductList" teleported popper-append-to-body>
                    <el-option label="默认排序" value=""></el-option>
                    <el-option label="价格从低到高" value="price_asc"></el-option>
                    <el-option label="价格从高到低" value="price_desc"></el-option>
                    <el-option label="商品数量从高到低" value="number_desc"></el-option>
                </el-select>
            </el-col>
            <el-col :span="8">
                <el-input-number v-model="product_data.minPrice" placeholder="最低价格" :min="0" @change="getProductList"></el-input-number>
                <span class="mx-2">-</span>
                <el-input-number v-model="product_data.maxPrice" placeholder="最高价格" :min="0" @change="getProductList"></el-input-number>
            </el-col>
            <el-col :span="8">
                <el-select 
                    v-model="product_data.state" 
                    placeholder="商品状态" 
                    @change="getProductList" 
                    teleported 
                    popper-append-to-body
                    :teleported-append-to-body="true"
                    :popper-options="{ strategy: 'fixed' }">
                    <el-option label="全部" value=""></el-option>
                    <el-option label="上架" :value="1"></el-option>
                    <el-option label="下架" :value="-1"></el-option>
                    <el-option label="预售" :value="0"></el-option>
                </el-select>
            </el-col>
        </el-row>

        <el-row>
            <el-table :data="product_data.productList" style="width: 100%;margin-top: 15px;" stripe v-loading="loading">
                <!-- 从数据库获取的数据首先会赋值到productList中，然后在el-table中显示,所以这里的prop要和数据库中字段名一致 -->
                <!-- 也就是prop绑定在:data中对应的数据字段,data里面的数据由数据库返回 -->
                <!-- <el-table-column type="index" width="50"></el-table-column> -->
                <el-table-column prop="id" label="id" width="120"></el-table-column>
                <el-table-column label="商品名称" prop="name" show-overflow-tooltip></el-table-column>
                <el-table-column label="商品价格" prop="price" width="150"></el-table-column>
                <el-table-column label="商品数量" prop="number" width="150"></el-table-column>
                <el-table-column label="商品状态" prop="state" width="150">
                    <template #default="scope">
                        <el-tag v-if="scope.row.state === 1" type="success">上架</el-tag>
                        <el-tag v-else-if="scope.row.state === -1" type="warning">下架</el-tag>
                        <el-tag v-else type="danger">预售</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" @click="ProductEdit(scope.$index,scope.row)">编辑</el-button>
                        <el-button type="danger" @click="handleDelete(scope.$index,scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="pagination-container">
                <el-pagination
                    v-model:current-page="product_data.currentPage"
                    v-model:page-size="product_data.pageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    :total="product_data.total"
                    layout="total, sizes, prev, pager, next, jumper"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                />
            </div>
        </el-row>

        <!-- 编辑商品弹框 -->
        <el-dialog 
            title="编辑商品" 
            v-model="ProductEditDialogVisible" 
            width="30%" 
            :close-on-click-modal="false"
            center
            :teleported="true"
            :append-to-body="true"
            @closed="handleClose">
            <el-form :model="productEditForm">
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
                    <el-select 
                        v-model="productEditForm.state" 
                        placeholder="请选择商品状态" 
                        teleported 
                        popper-append-to-body
                        :teleported-append-to-body="true"
                        :popper-options="{ strategy: 'fixed' }">
                        <el-option label="上架" :value="1"></el-option>
                        <el-option label="下架" :value="-1"></el-option>
                        <el-option label="预售" :value="0"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="ProductEditCancel">取 消</el-button>
                    <el-button type="primary" @click="ProductEditSubmit">确 定</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- 删除商品弹框 -->
        <el-dialog
            title="删除商品"
            v-model="deleteDialogVisible"
            width="30%"
            :close-on-click-modal="false"
            center>
            <span>确认删除商品"{{ deleteProductName }}"吗？</span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleDeleteCancel">取 消</el-button>
                    <el-button type="danger" @click="handleDeleteConfirm">确 定</el-button>
                </span>
            </template>
        </el-dialog>
    </el-card>
</template>

<script setup>
import { ArrowRight, Search, CirclePlus } from '@element-plus/icons-vue'
import { ref, reactive, onMounted, nextTick, onBeforeUnmount } from 'vue'
import api from '@/api/index'
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const categories = ref([])
const product_data = reactive({
    queryName: '',
    productList: [],
    sortBy: '',
    minPrice: null,
    maxPrice: null,
    state: '',
    currentPage: 1,
    pageSize: 10,
    total: 0
})

//const lastQueryName = ref('') // 用于存储上一个 queryName 的值

onMounted(() => {
    nextTick(() => {
        getCategories()
        getProductList()
    })
})

// 获取分类列表
const getCategories = async () => {
    try {
        const res = await api.get_category_list(0)
        if (res.data.status === 200) {
            categories.value = res.data.data
        }
    } catch (error) {
        console.error('获取分类列表失败:', error)
    }
}

// 优化ResizeObserver处理
let productStateChangeTimeout = null;

// 修改状态更改函数以使用节流
const getProductList = async () => {
    // 清除上一个timeout
    if (productStateChangeTimeout) {
        clearTimeout(productStateChangeTimeout);
    }
    
    // 设置新的timeout，延迟执行请求
    productStateChangeTimeout = setTimeout(async () => {
        loading.value = true
        try {
            let params = {}
            
            if (product_data.queryName) {
                params.name = product_data.queryName
            }
            
            if (product_data.sortBy) {
                const [sortField, order] = product_data.sortBy.split('_')
                params.sort_by = sortField
                params.order = order
            }
            
            if (product_data.minPrice !== null) {
                params.min_price = product_data.minPrice
            }
            
            if (product_data.maxPrice !== null) {
                params.max_price = product_data.maxPrice
            }
            
            if (product_data.state !== '') {
                params.state = product_data.state
            }
            
            params.page = product_data.currentPage
            params.per_page = product_data.pageSize

            // console.log('发送请求参数:', params)  // 调试日志
            
            const res = await api.get_product_list({params})
            // console.log('接收到响应:', res.data)  // 调试日志
            
            if (res.data.status === 200) {
                product_data.productList = res.data.data.items || []
                product_data.total = res.data.data.total || 0
            } else {
                ElMessage.warning({
                    message: res.data.msg || '获取商品列表失败',
                    type: 'warning'
                })
            }
        } catch (error) {
            console.error('获取商品列表失败:', error)
            if (error.response) {
                console.error('错误响应:', error.response.data)  // 调试日志
                ElMessage.error(error.response.data.msg || '获取商品列表失败')
            } else {
                ElMessage.error('网络错误，请检查您的连接')
            }
        } finally {
            loading.value = false
        }
    }, 50); // 短暂延迟，避免频繁触发
}

const handleSizeChange = (val) => {
    product_data.pageSize = val
    product_data.currentPage = 1
    getProductList()
}

const handleCurrentChange = (val) => {
    product_data.currentPage = val
    getProductList()
}

const handleInput = () => {
    if (product_data.queryName !== '') {
        getProductList()
    }else{
        getProductList()
    }
  
    //lastQueryName.value = product_data.queryName

}

// 删除商品相关
const deleteDialogVisible = ref(false)
const deleteProductId = ref(null)
const deleteProductName = ref('')

// 打开删除对话框
const handleDelete = (index, row) => {
    deleteProductId.value = row.id
    deleteProductName.value = row.name
    deleteDialogVisible.value = true
}

// 取消删除
const handleDeleteCancel = () => {
    deleteDialogVisible.value = false
    deleteProductId.value = null
    deleteProductName.value = ''
}

// 确认删除
const handleDeleteConfirm = async () => {
    try {
        const res = await api.del_product(deleteProductId.value)
        if (res.data.status === 200) {
            ElMessage({
                type: 'success',
                message: res.data.msg
            })
            await getProductList()
        } else {
            ElMessage.warning({
                message: res.data.msg
            })
        }
        deleteDialogVisible.value = false
    } catch (error) {
        console.error('删除商品失败:', error)
        ElMessage.error('删除失败，请重试')
    } finally {
        deleteProductId.value = null
        deleteProductName.value = ''
    }
}

const router = useRouter()
//点击添加商品按钮,跳转到添加商品页面
const addProduct = () => {
    router.push('/add_product/')
}

// 编辑商品
const ProductEditDialogVisible = ref(false)
const productEditForm = reactive({
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
    productEditID.value = row.id
    ProductEditDialogVisible.value = true
}

// 防止频繁触发状态变化导致的问题
let stateChangeTimer = null;
const handleStateChange = () => {
    if (stateChangeTimer) {
        clearTimeout(stateChangeTimer);
    }
    
    stateChangeTimer = setTimeout(() => {
        getProductList();
    }, 100);
};

const ProductEditSubmit = () => {
    if (!productEditForm.name || !productEditForm.price || !productEditForm.number || productEditForm.state === '') {
        ElMessage.warning('请填写完整的商品信息')
        return
    }

    // 状态切换时添加DOM更新完成后的延迟
    const oldState = product_data.productList.find(p => p.id === productEditID.value)?.state;
    
    api.update_product(productEditID.value, productEditForm).then(res => {
        if (res.data.status === 200) {
            ElMessage({
                type: 'success',
                message: res.data.msg
            })
            
            // 如果是预售状态变更，添加额外处理
            if (oldState !== 0 && productEditForm.state === 0 || 
                oldState === 0 && productEditForm.state !== 0) {
                // 延迟获取列表，让DOM更新完成
                setTimeout(() => getProductList(), 100);
            } else {
                getProductList();
            }
            
            ProductEditDialogVisible.value = false
        } else {
            ElMessage.warning({
                message: res.data.msg
            })
        }
    }).catch(error => {
        console.error('更新商品失败:', error)
        ElMessage.error('更新失败，请重试')
    })
}

const ProductEditCancel = () => {
    ProductEditDialogVisible.value = false
    productEditForm.name = ''
    productEditForm.price = ''
    productEditForm.number = ''
    productEditForm.state = ''
}

const handleClose = () => {
    productEditForm.name = ''
    productEditForm.price = ''
    productEditForm.number = ''
    productEditForm.state = ''
}

// 确保组件销毁时清除timeout
onBeforeUnmount(() => {
    if (productStateChangeTimeout) {
        clearTimeout(productStateChangeTimeout);
    }
});

</script>

<style scoped>
.box-card {
    margin-top: 20px;
}

.mb-4 {
    margin-bottom: 1rem;
}

.mx-2 {
    margin: 0 0.5rem;
}

.pagination-container {
    margin-top: 1rem;
    display: flex;
    justify-content: flex-end;
}

.el-input-number {
    width: 130px;
}

.el-select {
    width: 100%;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
    .el-col {
        margin-bottom: 1rem;
    }
    
    .el-input-number {
        width: 100%;
    }
}

/* 添加预售状态的特殊样式，减少布局变化 */
.el-tag.el-tag--danger {
    min-width: 42px;
    text-align: center;
}

.el-tag.el-tag--success, 
.el-tag.el-tag--warning {
    min-width: 42px;  
    text-align: center;
}
</style>
