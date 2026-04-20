<template>
  <div class="positions-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>职位管理</span>
          <el-button type="primary" @click="showDialog('create')">新建职位</el-button>
        </div>
      </template>
      <el-table :data="positionList" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="职位名称" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDialog('edit', row)">编辑</el-button>
            <el-button link type="danger" @click="deletePosition(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showEditDialog" :title="isEdit ? '编辑职位' : '新建职位'" width="400px">
      <el-form ref="formRef" :model="form" label-width="80px">
        <el-form-item label="职位名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入职位名称" />
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

const positionList = ref([
  { id: 1, name: '技术总监', created_at: '2024-01-01 00:00:00' },
  { id: 2, name: '前端工程师', created_at: '2024-01-01 00:00:00' },
  { id: 3, name: '后端工程师', created_at: '2024-01-01 00:00:00' },
  { id: 4, name: '产品经理', created_at: '2024-01-01 00:00:00' },
])

const showEditDialog = ref(false)
const isEdit = ref(false)
const form = reactive({ id: null, name: '' })

function showDialog(type, row = null) {
  isEdit.value = type === 'edit'
  form.id = type === 'edit' ? row.id : null
  form.name = type === 'edit' ? row.name : ''
  showEditDialog.value = true
}

function submitForm() {
  if (!form.name) {
    ElMessage.warning('请输入职位名称')
    return
  }
  ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
  showEditDialog.value = false
}

function deletePosition(row) {
  ElMessageBox.confirm('确定删除该职位吗？', '提示').then(() => {
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
