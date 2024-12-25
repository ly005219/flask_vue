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
          <el-select v-model="skuForm.product_id" placeholder="请选择商品">
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
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

const skuForm = reactive({
  product_id: '',
  price: '',
  stock: '',
  specifications: {}
})

const skuRules = {
  product_id: [{ required: true, message: '请选择商品', trigger: 'change' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入库存', trigger: 'blur' }]
}

onMounted(() => {
  getSKUList()
  getProductList()
})

const getSKUList = () => {
  api.get_sku_list()
    .then(res => {
      console.log('SKU列表响应:', res)
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

const getProductList = () => {
  api.get_product_list().then(res => {
    if (res.data && res.data.status === 200) {
      productList.value = res.data.data.data || []
    } else {
      ElMessage.error(res.data?.msg || '获取商品列表失败')
    }
  }).catch(err => {
    console.error('获取商品列表错误:', err)
    ElMessage.error('获取商品列表失败')
  })
}

const showAddDialog = () => {
  dialogTitle.value = '添加SKU'
  dialogVisible.value = true
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
    product_id: parseInt(skuForm.product_id),
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
  ElMessageBox.confirm(`确认删除${row.sku_code}商品吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    api.delete_sku(row.id).then(res => {
      if (res.data.status === 200) {
        ElMessage({
          showClose: true,
          message: res.data.msg,
          type: 'success'
        })
        getSKUList()
      } else {
        ElMessage.warning({
          showClose: true,
          message: res.data.msg
        })
      }
    })
  }).catch(() => {
    ElMessage({
      type: 'info',
      message: '已取消删除'
    })
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