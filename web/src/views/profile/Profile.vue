<template>
  <div class="profile-page">
    <el-row :gutter="16">
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>个人信息</span>
            <el-button v-if="!isEditing" type="primary" size="small" @click="isEditing = true">编辑</el-button>
            <template v-else>
              <el-button size="small" @click="cancelEdit">取消</el-button>
              <el-button type="primary" size="small" @click="saveProfile">保存</el-button>
            </template>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="用户名">{{ profile.username }}</el-descriptions-item>
            <el-descriptions-item label="真实姓名">
              <el-input v-if="isEditing" v-model="profile.real_name" size="small" />
              <template v-else>{{ profile.real_name }}</template>
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              <el-input v-if="isEditing" v-model="profile.email" size="small" />
              <template v-else>{{ profile.email || '-' }}</template>
            </el-descriptions-item>
            <el-descriptions-item label="手机号">
              <el-input v-if="isEditing" v-model="profile.phone" size="small" />
              <template v-else>{{ profile.phone || '-' }}</template>
            </el-descriptions-item>
            <el-descriptions-item label="部门">{{ profile.department || '-' }}</el-descriptions-item>
            <el-descriptions-item label="职位">{{ profile.position || '-' }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="profile.status === 1 ? 'success' : 'info'" size="small">
                {{ profile.status === 1 ? '启用' : '禁用' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ profile.created_at }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>修改密码</span>
          </template>
          <el-form ref="pwdFormRef" :model="pwdForm" :rules="pwdRules" label-width="80px">
            <el-form-item label="旧密码" prop="oldPassword">
              <el-input v-model="pwdForm.oldPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input v-model="pwdForm.newPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="pwdForm.confirmPassword" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getCurrentUser } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const isEditing = ref(false)
const profile = ref({
  username: '',
  real_name: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  status: 1,
  created_at: '',
})

const pwdFormRef = ref(null)
const pwdForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const pwdRules = {
  oldPassword: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== pwdForm.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

onMounted(() => {
  // 模拟数据
  profile.value = {
    username: userStore.userInfo?.username || 'admin',
    real_name: userStore.userInfo?.real_name || '管理员',
    email: 'admin@example.com',
    phone: '13800138000',
    department: '技术部',
    position: '技术总监',
    status: 1,
    created_at: '2024-01-01 00:00:00',
  }
})

function cancelEdit() {
  isEditing.value = false
}

function saveProfile() {
  ElMessage.success('保存成功')
  isEditing.value = false
}

function changePassword() {
  pwdFormRef.value.validate(valid => {
    if (valid) {
      ElMessage.success('密码修改成功')
      pwdForm.oldPassword = ''
      pwdForm.newPassword = ''
      pwdForm.confirmPassword = ''
    }
  })
}
</script>

<style scoped>
.profile-page {
  max-width: 1000px;
}
</style>
