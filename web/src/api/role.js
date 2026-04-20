import request from './request'

export function getRoleList(params) {
  return request.get('/system/roles', { params })
}

export function getRoleDetail(id) {
  return request.get(`/system/roles/${id}`)
}

export function createRole(data) {
  return request.post('/system/roles', data)
}

export function updateRole(id, data) {
  return request.patch(`/system/roles/${id}`, data)
}

export function deleteRole(id) {
  return request.delete(`/system/roles/${id}`)
}
