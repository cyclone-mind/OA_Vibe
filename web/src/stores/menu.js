import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMenuStore = defineStore('menu', () => {
  const menuList = ref([])
  const permissionMenuList = ref([])

  function setMenuList(list) {
    menuList.value = list
  }

  function setPermissionMenuList(list) {
    permissionMenuList.value = list
  }

  return {
    menuList,
    permissionMenuList,
    setMenuList,
    setPermissionMenuList,
  }
})
