<template>
  <div class="users-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="showDialog('create')">新建用户</el-button>
        </div>
      </template>
      <el-table :data="userList" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="real_name" label="真实姓名" width="100" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="department" label="部门" width="100" />
        <el-table-column prop="position" label="职位" width="100" />
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
            <el-button link type="primary" @click="assignRole(row)">分配角色</el-button>
            <el-button link type="danger" @click="deleteUser(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建/编辑弹窗 -->
    <el-dialog v-model="showEditDialog" :title="isEdit ? '编辑用户' : '新建用户'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="isEdit" />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="部门" prop="department_id">
          <el-select v-model="form.department_id" style="width: 100%">
            <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="职位" prop="position_id">
          <el-select v-model="form.position_id" style="width: 100%">
            <el-option v-for="p in positions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>

    <!-- 分配角色弹窗 -->
    <el-dialog v-model="showRoleDialog" title="分配角色" width="400px">
      <el-select v-model="selectedRoles" multiple style="width: 100%">
        <el-option v-for="r in roles" :key="r.id" :label="r.name" :value="r.id" />
      </el-select>
      <template #footer>
        <el-button @click="showRoleDialog = false">取消</el-button>
        <el-button type="primary" @click="submitRole">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const userList = ref([
  { id: 1, username: 'admin', real_name: '管理员', email: 'admin@example.com', phone: '13800138000', department: '技术部', position: '总监', status: 1 },
  { id: 2, username: 'user1', real_name: '张三', email: 'zhangsan@example.com', phone: '13800138001', department: '技术部', position: '工程师', status: 1 },
])

const departments = ref([{ id: 1, name: '技术部' }, { id: 2, name: '产品部' }])
const positions = ref([{ id: 1, name: '总监' }, { id: 2, name: '工程师' }])
const roles = ref([{ id: 1, name: '管理员' }, { id: 2, name: '普通员工' }])

const showEditDialog = ref(false)
const showRoleDialog = ref(false)
const isEdit = ref(false)
const currentUser = ref({})
const selectedRoles = ref([])

const form = reactive({
  username: '',
  password: '',
  real_name: '',
  email: '',
  phone: '',
  department_id: null,
  position_id: null,
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
}

function showDialog(type, row = null) {
  if (type === 'create') {
    isEdit.value = false
    Object.keys(form).forEach(k => form[k] = '')
  } else {
    isEdit.value = true
    Object.assign(form, row)
  }
  showEditDialog.value = true
}

function submitForm() {
  ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
  showEditDialog.value = false
}

function assignRole(row) {
  currentUser.value = row
  selectedRoles.value = []
  showRoleDialog.value = true
}

function submitRole() {
  ElMessage.success('角色分配成功')
  showRoleDialog.value = false
}

function deleteUser(row) {
  ElMessageBox.confirm('确定删除该用户吗？', '提示').then(() => {
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
