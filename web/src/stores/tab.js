import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTabStore = defineStore('tab', () => {
  const tabs = ref([
    { path: '/dashboard', name: '首页', closable: false }
  ])
  const currentTab = ref('/dashboard')

  function addTab(tab) {
    const exists = tabs.value.find(t => t.path === tab.path)
    if (!exists) {
      tabs.value.push({ ...tab, closable: tab.path !== '/dashboard' })
    }
    currentTab.value = tab.path
  }

  function removeTab(path) {
    const index = tabs.value.findIndex(t => t.path === path)
    if (index > 0) {
      tabs.value.splice(index, 1)
      if (currentTab.value === path) {
        currentTab.value = tabs.value[index - 1]?.path || '/dashboard'
      }
    }
  }

  function setCurrentTab(path) {
    currentTab.value = path
  }

  return {
    tabs,
    currentTab,
    addTab,
    removeTab,
    setCurrentTab,
  }
})
