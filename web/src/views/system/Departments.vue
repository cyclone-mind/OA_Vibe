<template>
  <div class="departments-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>部门管理</span>
          <el-button type="primary" @click="showDialog('create')">新建部门</el-button>
        </div>
      </template>
      <el-tree :data="treeData" :props="{ label: 'name', children: 'children' }" default-expand-all>
        <template #default="{ node, data }">
          <span class="tree-node">
            <span>{{ data.name }}</span>
            <span class="actions">
              <el-button link type="primary" size="small" @click="showDialog('edit', data)">编辑</el-button>
              <el-button link type="primary" size="small" @click="showDialog('create', data)">新增子部门</el-button>
              <el-button link type="danger" size="small" @click="deleteDept(data)">删除</el-button>
            </span>
          </span>
        </template>
      </el-tree>
    </el-card>

    <el-dialog v-model="showEditDialog" :title="isEdit ? '编辑部门' : '新建部门'" width="400px">
      <el-form ref="formRef" :model="form" label-width="80px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent_id">
          <el-select v-model="form.parent_id" style="width: 100%" placeholder="请选择上级部门">
            <el-option label="无" :value="null" />
            <el-option v-for="d in flatDepts" :key="d.id" :label="d.name" :value="d.id" />
          </el-select>
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
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const treeData = ref([
  {
    id: 1,
    name: '技术部',
    children: [
      { id: 11, name: '前端组' },
      { id: 12, name: '后端组' },
    ],
  },
  { id: 2, name: '产品部', children: [] },
  { id: 3, name: '运营部', children: [] },
])

const flatDepts = computed(() => {
  const result = []
  function flatten(nodes) {
    nodes.forEach(n => {
      result.push({ id: n.id, name: n.name })
      if (n.children) flatten(n.children)
    })
  }
  flatten(treeData.value)
  return result
})

const showEditDialog = ref(false)
const isEdit = ref(false)
const form = reactive({ id: null, name: '', parent_id: null })

function showDialog(type, parent = null) {
  isEdit.value = type === 'edit'
  form.id = type === 'edit' ? parent.id : null
  form.name = type === 'edit' ? parent.name : ''
  form.parent_id = parent?.id || null
  showEditDialog.value = true
}

function submitForm() {
  if (!form.name) {
    ElMessage.warning('请输入部门名称')
    return
  }
  ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
  showEditDialog.value = false
}

function deleteDept(data) {
  ElMessageBox.confirm('确定删除该部门吗？', '提示').then(() => {
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

.tree-node {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-right: 16px;
}

.actions .el-button {
  margin-left: 8px;
}
</style>
