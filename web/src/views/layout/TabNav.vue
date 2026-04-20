<template>
  <div class="tab-nav">
    <el-tabs v-model="currentTab" type="card" @tab-remove="removeTab" @tab-click="clickTab">
      <el-tab-pane
        v-for="tab in tabs"
        :key="tab.path"
        :label="tab.name"
        :name="tab.path"
        :closable="tab.closable"
      />
    </el-tabs>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTabStore } from '@/stores/tab'

const router = useRouter()
const tabStore = useTabStore()

const tabs = computed(() => tabStore.tabs)
const currentTab = computed({
  get: () => tabStore.currentTab,
  set: (val) => tabStore.setCurrentTab(val),
})

function removeTab(path) {
  tabStore.removeTab(path)
  router.push(tabStore.currentTab)
}

function clickTab(tab) {
  router.push(tab.props.name)
}
</script>

<style scoped>
.tab-nav {
  background-color: #fff;
  padding: 0 16px;
}

:deep(.el-tabs__header) {
  margin-bottom: 0;
}

:deep(.el-tabs__nav) {
  border: none;
}

:deep(.el-tabs__item) {
  border: none;
  height: 36px;
  line-height: 36px;
}

:deep(.el-tabs__item.is-active) {
  background-color: #f0f2f5;
}
</style>
