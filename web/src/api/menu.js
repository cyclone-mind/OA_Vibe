import request from './request'

export function getMenuTree() {
  return request.get('/system/menus/tree')
}

export function getUserMenus() {
  return request.get('/system/menus/user')
}

export function getMenuList() {
  return request.get('/system/menus')
}

export function createMenu(data) {
  return request.post('/system/menus', data)
}

export function updateMenu(id, data) {
  return request.patch(`/system/menus/${id}`, data)
}

export function deleteMenu(id) {
  return request.delete(`/system/menus/${id}`)
}
