<template>
  <div class="roles-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>角色管理</span>
          <el-button type="primary" @click="showDialog('create')">新建角色</el-button>
        </div>
      </template>
      <el-table :data="roleList" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="角色名称" width="150" />
        <el-table-column prop="code" label="角色标识" width="150" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'" size="small">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDialog('edit', row)">编辑</el-button>
            <el-button link type="primary" @click="showPermissionDialog(row)">配置权限</el-button>
            <el-button link type="danger" @click="deleteRole(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showEditDialog" :title="isEdit ? '编辑角色' : '新建角色'" width="400px">
      <el-form ref="formRef" :model="form" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色标识" prop="code">
          <el-input v-model="form.code" placeholder="请输入角色标识" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showPermDialog" title="配置权限" width="500px">
      <el-tree
        ref="permTreeRef"
        :data="permissionTree"
        :props="{ label: 'name', children: 'children' }"
        show-checkbox
        node-key="id"
      />
      <template #footer>
        <el-button @click="showPermDialog = false">取消</el-button>
        <el-button type="primary" @click="submitPermission">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const roleList = ref([
  { id: 1, name: '超级管理员', code: 'superadmin', description: '系统超级管理员，拥有所有权限', status: 1 },
  { id: 2, name: '管理员', code: 'admin', description: '系统管理员', status: 1 },
  { id: 3, name: '普通员工', code: 'employee', description: '普通员工', status: 1 },
])

const permissionTree = ref([
  { id: 1, name: '系统管理', children: [
    { id: 11, name: '用户管理' },
    { id: 12, name: '部门管理' },
    { id: 13, name: '职位管理' },
    { id: 14, name: '角色管理' },
    { id: 15, name: '菜单管理' },
    { id: 16, name: '权限管理' },
  ]},
  { id: 2, name: '业务模块', children: [
    { id: 21, name: '请假管理' },
    { id: 22, name: '审批中心' },
  ]},
])

const showEditDialog = ref(false)
const showPermDialog = ref(false)
const isEdit = ref(false)
const currentRole = ref({})
const permTreeRef = ref(null)

const form = reactive({ id: null, name: '', code: '', description: '' })

function showDialog(type, row = null) {
  isEdit.value = type === 'edit'
  if (type === 'create') {
    Object.keys(form).forEach(k => form[k] = '')
  } else {
    Object.assign(form, row)
  }
  showEditDialog.value = true
}

function showPermissionDialog(row) {
  currentRole.value = row
  showPermDialog.value = true
}

function submitForm() {
  if (!form.name || !form.code) {
    ElMessage.warning('请填写完整信息')
    return
  }
  ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
  showEditDialog.value = false
}

function submitPermission() {
  const checked = permTreeRef.value.getCheckedKeys()
  ElMessage.success('权限配置成功')
  showPermDialog.value = false
}

function deleteRole(row) {
  ElMessageBox.confirm('确定删除该角色吗？', '提示').then(() => {
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
