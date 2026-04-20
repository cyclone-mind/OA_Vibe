import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLeaveStore = defineStore('leave', () => {
  const leaveList = ref([])

  function setLeaveList(list) {
    leaveList.value = list
  }

  function addLeave(leave) {
    leaveList.value.unshift(leave)
  }

  function updateLeave(id, updates) {
    const index = leaveList.value.findIndex(l => l.id === id)
    if (index > -1) {
      leaveList.value[index] = { ...leaveList.value[index], ...updates }
    }
  }

  return {
    leaveList,
    setLeaveList,
    addLeave,
    updateLeave,
  }
})
