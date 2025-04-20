<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>SKU管理</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
      <div class="button-group">
        <el-button type="primary" @click="showAddDialog">添加SKU</el-button>
        <el-button type="success" @click="exportExcel">导出Excel</el-button>
      </div>
      
      <el-table :data="skuList" style="width: 100%; margin-top: 20px">
        <el-table-column prop="sku_code" label="SKU编码" />
        <el-table-column prop="specifications" label="规格">
          <template #default="scope">
            <div v-for="(value, key) in scope.row.specifications" :key="key">
              {{ key }}: {{ value }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" />
        <el-table-column prop="stock" label="库存" />
        <el-table-column prop="sales" label="销量" />
        <el-table-column label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="scope">
            <el-button-group>
              <el-button 
                type="primary" 
                @click="editSKU(scope.row)"
                :icon="Edit"
              >编辑</el-button>
              <el-button 
                type="danger" 
                @click="deleteSKU(scope.row)"
                :icon="Delete"
              >删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑SKU对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="50%">
      <el-form :model="skuForm" ref="skuFormRef" :rules="skuRules" label-width="80px">
        <el-form-item label="商品" prop="product_id">
          <el-select v-model.number="skuForm.product_id" placeholder="请选择商品" teleported popper-append-to-body>
            <el-option
              v-for="item in productList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="规格" prop="specifications">
          <div v-for="(spec, index) in specifications" :key="index" class="spec-item">
            <el-input v-model="spec.name" placeholder="规格名称" style="width: 200px" />
            <el-input v-model="spec.value" placeholder="规格值" style="width: 200px; margin-left: 10px" />
            <el-button @click="removeSpec(index)" type="danger" icon="Delete" circle class="spec-delete" />
          </div>
          <el-button @click="addSpec" type="primary" style="margin-top: 10px">添加规格</el-button>
        </el-form-item>

        <el-form-item label="价格" prop="price">
          <el-input v-model.number="skuForm.price" type="number" placeholder="请输入价格" />
        </el-form-item>

        <el-form-item label="库存" prop="stock">
          <el-input v-model.number="skuForm.stock" type="number" placeholder="请输入库存" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitSKU">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      title="确认删除"
      v-model="deleteDialogVisible"
      width="30%"
      :close-on-click-modal="false"
      :show-close="!isDeleting"
      :close-on-press-escape="!isDeleting"
    >
      <span>确认删除SKU: {{ skuToDelete?.sku_code }} 吗？</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false" :disabled="isDeleting">取消</el-button>
          <el-button type="primary" @click="confirmDelete" :loading="isDeleting">
            {{ isDeleting ? '删除中...' : '确定' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, h, nextTick } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue'
import { Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api/index'
import base from '@/api/base'

const skuList = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加SKU')
const productList = ref([])
const specifications = ref([])
const deleteDialogVisible = ref(false)
const skuToDelete = ref(null)
const isDeleting = ref(false)

const skuForm = reactive({
  product_id: '',
  price: '',
  stock: '',
  specifications: {}
})

const skuRules = {
  product_id: [{ required: true, message: '请选择商品', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入库存', trigger: 'blur' }]
}

onMounted(() => {
  nextTick(() => {
    getSKUList()
    getProductList()
  })
})

const getSKUList = () => {
  api.get_sku_list()
    .then(res => {
      if (res?.data?.status === 200) {
        skuList.value = res.data.data.data || []
      } else {
        ElMessage.error(res?.data?.msg || '获取SKU列表失败')
      }
    })
    .catch(err => {
      console.error('获取SKU列表错误:', err)
      ElMessage.error('获取SKU列表失败，请检查网络连接')
    })
}

// const getProductList = () => {
//   //要state=2的商品 
//   console.log('获取商品列表sku')
//   api.get_product_list().then(res => {
//     console.log('获取商品列表sku',res.data.data)
//     if (res.data && res.data.status === 200 ) {
 
//       productList.value = res.data.data.items.filter(item => item.state === 1) || []
//     } else {
//       ElMessage.error(res.data?.msg || '获取商品列表失败')
//     }
//   }).catch(err => {
//     console.error('获取商品列表错误:', err)
//     ElMessage.error('获取商品列表失败')
//   })
// }
//获取所有商品
const getProductList = () => {
  api.get_all_products().then(res => {
    productList.value = res.data.data.filter(item => item.state === 1) || []
  })
}


const showAddDialog = () => {
  dialogTitle.value = '添加SKU'
  dialogVisible.value = true
  // 重置表单所有字段
  skuForm.product_id = null
  skuForm.price = ''
  skuForm.stock = ''
  skuForm.specifications = {}
  specifications.value = []
}

const addSpec = () => {
  specifications.value.push({
    name: '',
    value: ''
  })
}

const removeSpec = (index) => {
  specifications.value.splice(index, 1)
}

const submitSKU = () => {
  // 数据验证
  if (!skuForm.product_id) {
    ElMessage.error('请选择商品')
    return
  }
  if (!skuForm.price || skuForm.price <= 0) {
    ElMessage.error('请输入有效的价格')
    return
  }
  if (!skuForm.stock || skuForm.stock < 0) {
    ElMessage.error('请输入有效的库存')
    return
  }
  if (specifications.value.length === 0) {
    ElMessage.error('请至少添加一个规格')
    return
  }

  // 将规格数组转换为对象
  const specs = {}
  for (const spec of specifications.value) {
    if (!spec.name || !spec.value) {
      ElMessage.error('规格名称和值不能为空')
      return
    }
    specs[spec.name] = spec.value
  }

  // 准备提交的数据
  const submitData = {
    product_id: skuForm.product_id,
    specifications: specs,
    price: parseFloat(skuForm.price),
    stock: parseInt(skuForm.stock)
  }

  if (dialogTitle.value === '添加SKU') {
    api.add_sku(submitData)
      .then(res => {
        if (res.data.status === 200) {
          ElMessage({
            showClose: true,
            message: res.data.msg,
            type: 'success'
          })
          dialogVisible.value = false
          getSKUList()
          // 重置表单
          skuForm.product_id = ''
          skuForm.price = ''
          skuForm.stock = ''
          specifications.value = []
        } else {
          ElMessage.warning({
            showClose: true,
            message: res.data.msg
          })
        }
      })
      .catch(err => {
        console.error('添加SKU错误:', err)
        ElMessage.warning({
          showClose: true,
          message: '添加SKU失败，请检查网络连接'
        })
      })
  } else {
    api.update_sku(skuForm.id, skuForm).then(res => {
      if (res.data.status === 200) {
        ElMessage({
          showClose: true,
          message: res.data.msg,
          type: 'success'
        })
        dialogVisible.value = false
        getSKUList()
      } else {
        ElMessage.warning({
          showClose: true,
          message: res.data.msg
        })
      }
    })
  }
}

const editSKU = (row) => {
  dialogTitle.value = '编辑SKU'
  dialogVisible.value = true
  Object.assign(skuForm, row)
  
  // 将规格对象转换为数组
  specifications.value = []
  for (let key in row.specifications) {
    specifications.value.push({
      name: key,
      value: row.specifications[key]
    })
  }
}

const deleteSKU = (row) => {
  skuToDelete.value = row
  deleteDialogVisible.value = true
}

const confirmDelete = () => {
  if (!skuToDelete.value) return
  
  isDeleting.value = true
  // console.log('开始删除SKU请求:', skuToDelete.value.id)
  
  api.delete_sku(skuToDelete.value.id).then(res => {
    isDeleting.value = false
    // console.log('删除SKU响应:', res)
    if (res.data.status === 200) {
      ElMessage({
        showClose: true,
        message: res.data.msg,
        type: 'success'
      })
      getSKUList()
      deleteDialogVisible.value = false
    } else {
      console.error('删除SKU失败:', res.data)
      ElMessage.warning({
        showClose: true,
        message: res.data.msg || '删除失败，请查看控制台',
        duration: 5000 // 延长显示时间
      })
      // 不关闭对话框，让用户可以重试
    }
  }).catch(err => {
    isDeleting.value = false
    console.error('删除SKU错误详情:', err)
    let errorMessage = '删除失败，请检查网络连接'
    
    if (err.response && err.response.data) {
      errorMessage = `删除失败: ${err.response.data.msg || '未知错误'}`
      console.error('错误响应数据:', err.response.data)
      console.error('错误状态码:', err.response.status)
    }
    
    ElMessage({
      type: 'error',
      message: errorMessage,
      duration: 5000,
      showClose: true
    })
    // 不关闭对话框，让用户可以重试
  })
}

const exportExcel = () => {
  fetch(base.baseUrl + base.export_sku_excel, {
    method: 'GET',
    headers: {
      'token': sessionStorage.getItem('token')
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    return response.blob()
  })
  .then(blob => {
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'sku_list.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('Excel导出成功')
  })
  .catch(err => {
    console.error('导出Excel失败:', err)
    ElMessage.error('导出Excel失败')
  })
}
</script>

<style>
/* 全局消息弹窗样式 */
.el-message-box__wrapper {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  z-index: 2000 !important;
}

/* 自定义居中消息框样式 */
.centered-message-box {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
}

.centered-message-box .el-message-box__header {
  justify-content: center !important;
}

.centered-message-box .el-message-box__message {
  justify-content: center !important;
  margin: 0 !important;
  padding: 10px 0 !important;
}

/* 自定义删除对话框样式 */
.sku-delete-dialog {
  width: 400px !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  overflow: hidden !important;
  z-index: 2001 !important;
}

.sku-delete-dialog .el-message-box__header {
  background-color: #F56C6C;
  padding: 16px;
  text-align: center;
  border-bottom: none;
}

.sku-delete-dialog .el-message-box__title {
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  width: 100%;
}

.sku-delete-dialog .el-message-box__headerbtn {
  top: 16px;
  right: 16px;
}

.sku-delete-dialog .el-message-box__headerbtn .el-message-box__close {
  color: white;
  font-size: 18px;
}

.sku-delete-dialog .el-message-box__content {
  padding: 20px;
  font-size: 14px;
  color: #606266;
}

.sku-delete-dialog .el-message-box__container {
  position: relative;
  padding: 0;
}

.sku-delete-dialog .el-message-box__status {
  color: #F56C6C;
  font-size: 24px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 15px;
}

.sku-delete-dialog .el-message-box__message {
  padding-left: 0;
  margin-left: 0;
}

.sku-delete-dialog .el-message-box__btns {
  padding: 10px 20px 20px;
  display: flex;
  justify-content: center;
  border-top: none;
}

.sku-delete-dialog .el-button {
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 4px;
  transition: all 0.3s;
}

.sku-delete-dialog .el-button--default {
  background-color: #fff;
  border-color: #dcdfe6;
  color: #606266;
}

.sku-delete-dialog .el-button--default:hover {
  background-color: #f5f7fa;
  border-color: #c6e2ff;
  color: #409eff;
}

.sku-delete-dialog .el-button--primary {
  background-color: #F56C6C;
  border-color: #F56C6C;
  color: white;
}

.sku-delete-dialog .el-button--primary:hover {
  background-color: #f78989;
  border-color: #f78989;
}

/* 修复遮罩层层级问题 */
.v-modal {
  opacity: 0.6 !important;
  background-color: #000 !important;
  z-index: 1999 !important;
}
</style>

<style scoped>
.box-card {
  margin-top: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.el-button-group {
  display: flex;
  gap: 5px;
}

.el-button-group .el-button {
  padding: 8px 16px;
  font-size: 14px;
}

.spec-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.spec-delete {
  margin-left: 10px;
}

/* 确保操作按钮列的宽度足够 */
:deep(.el-table .cell) {
  white-space: nowrap;
}

/* 调整图标和文字的间距 */
:deep(.el-button [class*='el-icon'] + span) {
  margin-left: 6px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style> 