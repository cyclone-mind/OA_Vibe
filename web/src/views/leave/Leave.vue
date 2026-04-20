<template>
  <div class="leave-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的请假</span>
          <el-button type="primary" @click="showCreateDialog = true">新建请假</el-button>
        </div>
      </template>
      <el-table :data="leaveList" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="leave_type" label="请假类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getLeaveTypeText(row.leave_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column prop="reason" label="请假原因" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDetail(row)">详情</el-button>
            <el-button
              v-if="row.status === 'draft' || row.status === 'pending'"
              link
              type="primary"
              @click="submitLeave(row)"
            >
              提交
            </el-button>
            <el-button
              v-if="row.status === 'draft' || row.status === 'pending'"
              link
              type="danger"
              @click="cancelLeave(row)"
            >
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建请假弹窗 -->
    <el-dialog v-model="showCreateDialog" title="新建请假" width="500px">
      <el-form ref="formRef" :model="leaveForm" :rules="rules" label-width="100px">
        <el-form-item label="请假类型" prop="leave_type">
          <el-select v-model="leaveForm.leave_type" style="width: 100%">
            <el-option label="年假" value="annual" />
            <el-option label="病假" value="sick" />
            <el-option label="事假" value="personal" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="leaveForm.start_date" type="date" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="leaveForm.end_date" type="date" style="width: 100%" />
        </el-form-item>
        <el-form-item label="请假原因" prop="reason">
          <el-input v-model="leaveForm.reason" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">提交</el-button>
      </template>
    </el-dialog>

    <!-- 详情弹窗 -->
    <el-dialog v-model="showDetailDialog" title="请假详情" width="500px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="请假类型">{{ getLeaveTypeText(detailData.leave_type) }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailData.status)">{{ getStatusText(detailData.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ detailData.start_date }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ detailData.end_date }}</el-descriptions-item>
        <el-descriptions-item label="请假原因" :span="2">{{ detailData.reason }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailData.created_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getLeaveList, createLeave, submitLeave as apiSubmitLeave, cancelLeave as apiCancelLeave } from '@/api/leave'

const leaveList = ref([
  { id: 1, leave_type: 'annual', start_date: '2024-01-15', end_date: '2024-01-17', reason: '回家探亲', status: 'pending', created_at: '2024-01-10 10:00:00' },
  { id: 2, leave_type: 'sick', start_date: '2024-01-20', end_date: '2024-01-20', reason: '感冒发烧', status: 'approved', created_at: '2024-01-19 08:00:00' },
])

const showCreateDialog = ref(false)
const showDetailDialog = ref(false)
const detailData = ref({})

const leaveForm = reactive({
  leave_type: 'annual',
  start_date: '',
  end_date: '',
  reason: '',
})

const rules = {
  leave_type: [{ required: true, message: '请选择请假类型', trigger: 'change' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
  reason: [{ required: true, message: '请输入请假原因', trigger: 'blur' }],
}

function getLeaveTypeText(type) {
  const map = { annual: '年假', sick: '病假', personal: '事假' }
  return map[type] || type
}

function getStatusText(status) {
  const map = { draft: '草稿', pending: '待审批', approved: '已批准', rejected: '已拒绝', cancelled: '已取消' }
  return map[status] || status
}

function getStatusType(status) {
  const map = { draft: 'info', pending: 'warning', approved: 'success', rejected: 'danger', cancelled: 'info' }
  return map[status] || 'info'
}

function viewDetail(row) {
  detailData.value = row
  showDetailDialog.value = true
}

async function handleCreate() {
  try {
    await createLeave(leaveForm)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

async function submitLeave(row) {
  try {
    await ElMessageBox.confirm('确定提交此请假单吗？', '提示')
    await apiSubmitLeave(row.id)
    ElMessage.success('提交成功')
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('提交失败')
  }
}

async function cancelLeave(row) {
  try {
    await ElMessageBox.confirm('确定取消此请假单吗？', '提示')
    await apiCancelLeave(row.id)
    ElMessage.success('取消成功')
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('取消失败')
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
