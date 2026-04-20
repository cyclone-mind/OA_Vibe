import request from './request'

export function getUserList(params) {
  return request.get('/system/users', { params })
}

export function getUserDetail(id) {
  return request.get(`/system/users/${id}`)
}

export function createUser(data) {
  return request.post('/system/users', data)
}

export function updateUser(id, data) {
  return request.patch(`/system/users/${id}`, data)
}

export function deleteUser(id) {
  return request.delete(`/system/users/${id}`)
}
