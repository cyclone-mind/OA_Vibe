<template>
  <div class="dashboard">
    <el-row :gutter="16">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #409eff">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">128</div>
              <div class="stat-label">员工总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #67c23a">
              <el-icon :size="32"><OfficeBuilding /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">12</div>
              <div class="stat-label">部门数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #e6a23c">
              <el-icon :size="32"><Briefcase /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">36</div>
              <div class="stat-label">职位数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #f56c6c">
              <el-icon :size="32"><Calendar /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">24</div>
              <div class="stat-label">请假申请数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>待审批提醒</span>
          </template>
          <div class="pending-alert" @click="$router.push('/approval')">
            <el-icon :size="40" color="#f56c6c"><Bell /></el-icon>
            <span class="pending-count">{{ pendingCount }} 条待审批</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>请假申请趋势</span>
          </template>
          <div ref="trendChartRef" style="height: 200px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>部门人员分布</span>
          </template>
          <div ref="deptChartRef" style="height: 250px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近请假记录</span>
          </template>
          <el-table :data="recentLeaves" style="width: 100%">
            <el-table-column prop="user_name" label="申请人" />
            <el-table-column prop="leave_type" label="类型" width="80" />
            <el-table-column prop="days" label="天数" width="60" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ row.status_text }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { User, OfficeBuilding, Briefcase, Calendar, Bell } from '@element-plus/icons-vue'

const pendingCount = ref(5)

const recentLeaves = ref([
  { user_name: '张三', leave_type: '年假', days: 3, status: 'pending', status_text: '待审批' },
  { user_name: '李四', leave_type: '病假', days: 1, status: 'approved', status_text: '已批准' },
  { user_name: '王五', leave_type: '事假', days: 2, status: 'pending', status_text: '待审批' },
])

const trendChartRef = ref(null)
const deptChartRef = ref(null)

function getStatusType(status) {
  const map = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    cancelled: 'info',
  }
  return map[status] || 'info'
}

onMounted(() => {
  // 请假趋势图
  const trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '请假数',
        type: 'line',
        smooth: true,
        data: [12, 15, 8, 18, 22, 5, 3],
        areaStyle: { color: 'rgba(64, 158, 255, 0.2)' },
        lineStyle: { color: '#409eff' },
      },
    ],
  })

  // 部门分布饼图
  const deptChart = echarts.init(deptChartRef.value)
  deptChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: 30, name: '技术部' },
          { value: 25, name: '产品部' },
          { value: 20, name: '运营部' },
          { value: 15, name: '市场部' },
          { value: 10, name: '人事部' },
        ],
      },
    ],
  })

  window.addEventListener('resize', () => {
    trendChart.resize()
    deptChart.resize()
  })
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.pending-alert {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  padding: 16px;
  background-color: #fef0f0;
  border-radius: 8px;
}

.pending-count {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}
</style>
