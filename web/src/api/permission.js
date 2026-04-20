import request from './request'

export function getPermissionList(params) {
  return request.get('/system/permissions', { params })
}

export function createPermission(data) {
  return request.post('/system/permissions', data)
}

export function updatePermission(id, data) {
  return request.patch(`/system/permissions/${id}`, data)
}

export function deletePermission(id) {
  return request.delete(`/system/permissions/${id}`)
}
