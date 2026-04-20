<template>
  <div class="permissions-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>权限管理</span>
          <el-button type="primary" @click="showDialog('create')">新建权限</el-button>
        </div>
      </template>
      <el-table :data="permissionList" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="权限名称" width="150" />
        <el-table-column prop="code" label="权限标识" width="150" />
        <el-table-column prop="menu_name" label="关联菜单" width="120" />
        <el-table-column prop="api_path" label="API 路径" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDialog('edit', row)">编辑</el-button>
            <el-button link type="danger" @click="deletePermission(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showEditDialog" :title="isEdit ? '编辑权限' : '新建权限'" width="500px">
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="权限标识" prop="code">
          <el-input v-model="form.code" placeholder="请输入权限标识" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="关联菜单" prop="menu_id">
          <el-select v-model="form.menu_id" style="width: 100%" placeholder="请选择关联菜单">
            <el-option v-for="m in menus" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="API 路径" prop="api_path">
          <el-input v-model="form.api_path" placeholder="请输入 API 路径，如: /system/users" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const permissionList = ref([
  { id: 1, name: '查看用户', code: 'system.users.list', menu_name: '用户管理', api_path: '/system/users' },
  { id: 2, name: '创建用户', code: 'system.users.create', menu_name: '用户管理', api_path: '/system/users' },
  { id: 3, name: '编辑用户', code: 'system.users.edit', menu_name: '用户管理', api_path: '/system/users/{id}' },
  { id: 4, name: '删除用户', code: 'system.users.delete', menu_name: '用户管理', api_path: '/system/users/{id}' },
  { id: 5, name: '查看请假', code: 'oa.leave.list', menu_name: '请假管理', api_path: '/oa/leave-requests' },
])

const menus = ref([
  { id: 1, name: '用户管理' },
  { id: 2, name: '部门管理' },
  { id: 3, name: '职位管理' },
  { id: 4, name: '角色管理' },
  { id: 5, name: '菜单管理' },
  { id: 6, name: '权限管理' },
  { id: 7, name: '请假管理' },
  { id: 8, name: '审批中心' },
])

const showEditDialog = ref(false)
const isEdit = ref(false)
const form = reactive({ id: null, name: '', code: '', menu_id: null, api_path: '' })

function showDialog(type, row = null) {
  isEdit.value = type === 'edit'
  if (type === 'create') {
    Object.keys(form).forEach(k => form[k] = k === 'menu_id' ? null : '')
  } else {
    Object.assign(form, row)
  }
  showEditDialog.value = true
}

function submitForm() {
  if (!form.name || !form.code) {
    ElMessage.warning('请填写完整信息')
    return
  }
  ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
  showEditDialog.value = false
}

function deletePermission(row) {
  ElMessageBox.confirm('确定删除该权限吗？', '提示').then(() => {
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
