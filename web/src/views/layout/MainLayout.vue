<template>
  <el-container class="main-layout">
    <el-aside width="200px">
      <SideMenu />
    </el-aside>
    <el-container>
      <el-header height="56px">
        <Header />
      </el-header>
      <TabNav />
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import Header from './Header.vue'
import SideMenu from './SideMenu.vue'
import TabNav from './TabNav.vue'
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  padding: 0 16px;
}

.el-main {
  background-color: #f0f2f5;
  padding: 16px;
}
</style>
