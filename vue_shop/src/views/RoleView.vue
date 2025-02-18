<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>权限管理</el-breadcrumb-item>
      <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
      <el-button type="primary" @click="showAddDialog">添加角色</el-button>

      <el-table :data="tableData.rolelist" stripe style="width: 100%; margin-top: 20px">
        <el-table-column prop="id" label="ID" width="100"/>
        <el-table-column prop="name" label="角色名称" width="150"/>
        <el-table-column prop="desc" label="描述" width="150"/>
        <el-table-column label="操作" width="500">
          <template #default="scope">
            <el-button-group>
              <el-button 
                type="primary" 
                :icon="Edit"
                @click="showEditDialog(scope.row)"
              >编辑</el-button>
              <el-button 
                type="warning" 
                :icon="Setting"
                @click="handlePermission(scope.row)"
              >分配权限</el-button>
              <el-button 
                type="danger" 
                :icon="Delete"
                @click="handleDelete(scope.row)"
              >删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 编辑角色对话框 -->
    <el-dialog 
      v-model="editDialogVisible" 
      :title="editForm.id ? '编辑角色' : '添加角色'" 
      width="40%"
    >
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="角色名称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.desc" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRole">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 分配权限对话框 -->
    <el-dialog v-model="menuDialogVisible" title="分配权限" width="50%">
      <el-tree
        ref="treeRef"
        :data="menuList"
        :props="menuProps"
        show-checkbox
        node-key="id"
        default-expand-all
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="menuDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPermission">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue'
import { Edit, Setting, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api/index'

const tableData = reactive({
  rolelist: []
})

const editDialogVisible = ref(false)
const menuDialogVisible = ref(false)
const menuList = reactive([])
const rid = ref(null)
const treeRef = ref(null)

const editForm = reactive({
  id: '',
  name: '',
  desc: ''
})

const menuProps = {
  label: 'name',
  children: 'children'
}

onMounted(() => {
  get_roles_list()
  getMenuList()
})

const get_roles_list = () => {
  api.get_roles_list().then(res => {
    if (res.data.status === 200) {
      tableData.rolelist = res.data.roles_data
    }
  })
}

const getMenuList = () => {
  api.get_menu({type_: 'tree'}).then(res => {
    console.log('菜单列表响应:', res)
    if (res.data.status === 200) {
      if (Array.isArray(res.data.data)) {
        menuList.splice(0, menuList.length, ...res.data.data)
      } else {
        console.warn('菜单数据不是数组:', res.data.data)
        menuList.splice(0, menuList.length)
      }
    } else {
      ElMessage.warning({
        showClose: true,
        message: res.data.msg || '获取菜单列表失败'
      })
    }
  }).catch(err => {
    console.error('获取菜单列表错误:', err)
    ElMessage.warning({
      showClose: true,
      message: '获取菜单列表失败'
    })
  })
}

const showAddDialog = () => {
  editForm.id = ''
  editForm.name = ''
  editForm.desc = ''
  editDialogVisible.value = true
}

const showEditDialog = (row) => {
  editForm.id = row.id
  editForm.name = row.name
  editForm.desc = row.desc
  editDialogVisible.value = true
}

const submitRole = () => {
  if (!editForm.name || !editForm.desc) {
    return ElMessage.warning('请填写完整信息')
  }

  const request = editForm.id
    ? api.update_role(editForm.id, editForm)
    : api.add_role(editForm)

  request.then(res => {
    if (res.data.status === 200) {
      ElMessage({
        showClose: true,
        message: res.data.msg,
        type: 'success'
      })
      editDialogVisible.value = false
      get_roles_list()
    } else {
      ElMessage.warning({
        showClose: true,
        message: res.data.msg
      })
    }
  })
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除角色"${row.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    api.del_role(row.id).then(res => {
      if (res.data.status === 200) {
        ElMessage({
          showClose: true,
          message: res.data.msg,
          type: 'success'
        })
        get_roles_list()
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

// 用于存储选中的菜单节点ID
const KeyList = ref([])

// 分配权限
const handlePermission = (row) => {
  console.log('当前角色数据:', row)
  menuDialogVisible.value = true
  rid.value = row.id
  KeyList.value = [] // 清空之前的选中状态

  if (row.menus && Array.isArray(row.menus) && row.menus.length > 0) {
    row.menus.forEach(menu => {
      KeyList.value.push(menu.id)
      
      if (menu.children && Array.isArray(menu.children)) {
        menu.children.forEach(subMenu => {
          KeyList.value.push(subMenu.id)
        })
      }
    })
  }

  console.log('选中的菜单ID:', KeyList.value)

  // 等待DOM更新后设置选中状态
  nextTick(() => {
    if (treeRef.value) {
      treeRef.value.setCheckedKeys(KeyList.value)
    }
  })
}

// 提交权限设置
const submitPermission = () => {
  if (!treeRef.value) {
    ElMessage.warning('菜单树未加载完成')
    return
  }

  // 获取选中和半选中的节点
  const checkedKeys = treeRef.value.getCheckedKeys() || []
  const halfCheckedKeys = treeRef.value.getHalfCheckedKeys() || []
  
  // 合并所有需要的菜单ID
  const menuIds = [...new Set([...checkedKeys, ...halfCheckedKeys])].join(',')
  console.log('提交的菜单ID:', menuIds)

  if (!menuIds) {
    ElMessage.warning('请选择要分配的权限')
    return
  }

  api.set_menu(rid.value, { menu_id: menuIds }).then(res => {
    if (res.data.status === 200) {
      ElMessage({
        showClose: true,
        message: res.data.msg,
        type: 'success'
      })
      menuDialogVisible.value = false
      get_roles_list() // 刷新角色列表
    } else {
      ElMessage.warning({
        showClose: true,
        message: res.data.msg || '分配权限失败'
      })
    }
  }).catch(err => {
    console.error('分配权限错误:', err)
    ElMessage.warning({
      showClose: true,
      message: '分配权限失败，请重试'
    })
  })
}
</script>

<style scoped>
.box-card {
  margin-top: 20px;
}

.el-button-group {
  display: flex;
  gap: 5px;
}

.el-button-group .el-button {
  padding: 8px 16px;
  font-size: 14px;
}

:deep(.el-table .cell) {
  white-space: nowrap;
}

:deep(.el-button [class*='el-icon'] + span) {
  margin-left: 6px;
}
</style>