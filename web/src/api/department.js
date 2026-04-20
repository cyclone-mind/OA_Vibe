import request from './request'

export function getDepartmentTree() {
  return request.get('/system/departments/tree')
}

export function getDepartmentList() {
  return request.get('/system/departments')
}

export function getDepartmentDetail(id) {
  return request.get(`/system/departments/${id}`)
}

export function createDepartment(data) {
  return request.post('/system/departments', data)
}

export function updateDepartment(id, data) {
  return request.patch(`/system/departments/${id}`, data)
}

export function deleteDepartment(id) {
  return request.delete(`/system/departments/${id}`)
}
