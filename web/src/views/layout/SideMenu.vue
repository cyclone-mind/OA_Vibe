<template>
  <el-menu
    :default-active="activeMenu"
    background-color="#304156"
    text-color="#bfcbd9"
    active-text-color="#409eff"
    :router="true"
  >
    <el-menu-item index="/dashboard">
      <el-icon><HomeFilled /></el-icon>
      <span>首页</span>
    </el-menu-item>
    <el-menu-item index="/leave">
      <el-icon><Calendar /></el-icon>
      <span>请假管理</span>
    </el-menu-item>
    <el-menu-item index="/approval">
      <el-icon><Stamp /></el-icon>
      <span>审批中心</span>
    </el-menu-item>
    <el-menu-item index="/profile">
      <el-icon><User /></el-icon>
      <span>个人中心</span>
    </el-menu-item>
    <el-sub-menu v-if="isAdmin" index="/system">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>系统管理</span>
      </template>
      <el-menu-item index="/system/users">用户管理</el-menu-item>
      <el-menu-item index="/system/departments">部门管理</el-menu-item>
      <el-menu-item index="/system/positions">职位管理</el-menu-item>
      <el-menu-item index="/system/roles">角色管理</el-menu-item>
      <el-menu-item index="/system/menus">菜单管理</el-menu-item>
      <el-menu-item index="/system/permissions">权限管理</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Calendar, Stamp, User, Setting } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const isAdmin = computed(() => {
  const info = userStore.userInfo
  return info?.is_superuser || info?.role === 'admin'
})
</script>

<style scoped>
.el-menu {
  height: 100%;
  border-right: none;
}
</style>
