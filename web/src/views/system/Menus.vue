<template>
  <div class="menus-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>菜单管理</span>
          <el-button type="primary" @click="showDialog('create')">新建菜单</el-button>
        </div>
      </template>
      <el-tree :data="menuTree" :props="{ label: 'name', children: 'children' }" default-expand-all>
        <template #default="{ node, data }">
          <span class="tree-node">
            <span>{{ data.name }} ({{ data.path }})</span>
            <span class="actions">
              <el-button link type="primary" size="small" @click="showDialog('edit', data)">编辑</el-button>
              <el-button link type="primary" size="small" @click="showDialog('create', data)">新增子菜单</el-button>
              <el-button link type="danger" size="small" @click="deleteMenu(data)">删除</el-button>
            </span>
          </span>
        </template>
      </el-tree>
    </el-card>

    <el-dialog v-model="showEditDialog" :title="isEdit ? '编辑菜单' : '新建菜单'" width="500px">
      <el-form ref="formRef" :model="form" label-width="80px">
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入菜单名称" />
        </el-form-item>
        <el-form-item label="菜单路径" prop="path">
          <el-input v-model="form.path" placeholder="请输入菜单路径" />
        </el-form-item>
        <el-form-item label="上级菜单" prop="parent_id">
          <el-select v-model="form.parent_id" style="width: 100%" placeholder="请选择上级菜单">
            <el-option label="无" :value="null" />
            <el-option v-for="m in flatMenus" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="菜单图标" prop="icon">
          <el-select v-model="form.icon" style="width: 100%" placeholder="请选择图标">
            <el-option v-for="ic in icons" :key="ic" :label="ic" :value="ic">
              <span><component :is="ic" /></span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="form.sort" :min="0" />
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

const menuTree = ref([
  {
    id: 1, name: '首页', path: '/dashboard', icon: 'HomeFilled', children: [],
  },
  {
    id: 2, name: '请假管理', path: '/leave', icon: 'Calendar', children: [],
  },
  {
    id: 3, name: '审批中心', path: '/approval', icon: 'Stamp', children: [],
  },
  {
    id: 4, name: '个人中心', path: '/profile', icon: 'User', children: [],
  },
  {
    id: 5, name: '系统管理', path: '/system', icon: 'Setting', children: [
      { id: 51, name: '用户管理', path: '/system/users' },
      { id: 52, name: '部门管理', path: '/system/departments' },
      { id: 53, name: '职位管理', path: '/system/positions' },
      { id: 54, name: '角色管理', path: '/system/roles' },
      { id: 55, name: '菜单管理', path: '/system/menus' },
      { id: 56, name: '权限管理', path: '/system/permissions' },
    ],
  },
])

const icons = ['HomeFilled', 'Calendar', 'Stamp', 'User', 'Setting', 'Menu', 'Grid', 'Document', 'Folder']

const flatMenus = computed(() => {
  const result = []
  function flatten(nodes) {
    nodes.forEach(n => {
      result.push({ id: n.id, name: n.name })
      if (n.children) flatten(n.children)
    })
  }
  flatten(menuTree.value)
  return result
})

const showEditDialog = ref(false)
const isEdit = ref(false)
const form = reactive({ id: null, name: '', path: '', parent_id: null, icon: '', sort: 0 })

function showDialog(type, parent = null) {
  isEdit.value = type === 'edit'
  if (type === 'create') {
    Object.keys(form).forEach(k => form[k] = k === 'sort' ? 0 : k === 'parent_id' ? (parent?.id || null) : '')
  } else {
    Object.assign(form, parent)
  }
  showEditDialog.value = true
}

function submitForm() {
  if (!form.name || !form.path) {
    ElMessage.warning('请填写完整信息')
    return
  }
  ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
  showEditDialog.value = false
}

function deleteMenu(data) {
  ElMessageBox.confirm('确定删除该菜单吗？', '提示').then(() => {
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
