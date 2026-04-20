<template>
  <div class="approval-page">
    <el-card>
      <template #header>
        <el-radio-group v-model="activeTab">
          <el-radio-button label="pending">待审批</el-radio-button>
          <el-radio-button label="processed">已审批</el-radio-button>
        </el-radio-group>
      </template>
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="user_name" label="申请人" width="100" />
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
        <el-table-column v-if="activeTab === 'processed'" prop="approved_comment" label="审批意见" width="150" />
        <el-table-column v-if="activeTab === 'processed'" prop="approved_at" label="审批时间" width="180" />
        <el-table-column v-if="activeTab === 'pending'" label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDetail(row)">详情</el-button>
            <el-button link type="success" @click="handleApprove(row)">批准</el-button>
            <el-button link type="danger" @click="handleReject(row)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="showDetailDialog" title="请假详情" width="500px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="申请人">{{ detailData.user_name }}</el-descriptions-item>
        <el-descriptions-item label="请假类型">{{ getLeaveTypeText(detailData.leave_type) }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ detailData.start_date }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ detailData.end_date }}</el-descriptions-item>
        <el-descriptions-item label="请假原因" :span="2">{{ detailData.reason }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 审批弹窗 -->
    <el-dialog v-model="showApproveDialog" title="审批" width="400px">
      <el-form ref="approveFormRef" :model="approveForm" label-width="80px">
        <el-form-item label="审批意见">
          <el-input v-model="approveForm.comment" type="textarea" :rows="3" placeholder="请输入审批意见" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showApproveDialog = false">取消</el-button>
        <el-button type="success" @click="confirmApprove">批准</el-button>
        <el-button type="danger" @click="confirmReject">拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { approveLeave, rejectLeave } from '@/api/leave'

const activeTab = ref('pending')
const showDetailDialog = ref(false)
const showApproveDialog = ref(false)
const detailData = ref({})
const currentRow = ref({})

const approveForm = reactive({ comment: '', action: '' })

const pendingList = ref([
  { id: 1, user_name: '张三', leave_type: 'annual', start_date: '2024-01-15', end_date: '2024-01-17', reason: '回家探亲', status: 'pending' },
  { id: 2, user_name: '李四', leave_type: 'sick', start_date: '2024-01-20', end_date: '2024-01-20', reason: '感冒发烧', status: 'pending' },
])

const processedList = ref([
  { id: 3, user_name: '王五', leave_type: 'personal', start_date: '2024-01-10', end_date: '2024-01-11', reason: '家中有事', status: 'approved', approved_comment: '同意', approved_at: '2024-01-09 14:00:00' },
])

const tableData = computed(() => activeTab.value === 'pending' ? pendingList.value : processedList.value)

function getLeaveTypeText(type) {
  const map = { annual: '年假', sick: '病假', personal: '事假' }
  return map[type] || type
}

function getStatusText(status) {
  const map = { pending: '待审批', approved: '已批准', rejected: '已拒绝' }
  return map[status] || status
}

function getStatusType(status) {
  const map = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

function viewDetail(row) {
  detailData.value = row
  showDetailDialog.value = true
}

function handleApprove(row) {
  currentRow.value = row
  approveForm.action = 'approve'
  showApproveDialog.value = true
}

function handleReject(row) {
  currentRow.value = row
  approveForm.action = 'reject'
  showApproveDialog.value = true
}

async function confirmApprove() {
  try {
    await approveLeave(currentRow.value.id, { comment: approveForm.comment })
    ElMessage.success('已批准')
    showApproveDialog.value = false
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function confirmReject() {
  try {
    await rejectLeave(currentRow.value.id, { comment: approveForm.comment })
    ElMessage.success('已拒绝')
    showApproveDialog.value = false
  } catch (error) {
    ElMessage.error('操作失败')
  }
}
</script>

<style scoped>
.approval-page {
  max-width: 1200px;
}
</style>
