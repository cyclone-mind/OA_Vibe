import request from './request'

export function getPositionList(params) {
  return request.get('/system/positions', { params })
}

export function getPositionDetail(id) {
  return request.get(`/system/positions/${id}`)
}

export function createPosition(data) {
  return request.post('/system/positions', data)
}

export function updatePosition(id, data) {
  return request.patch(`/system/positions/${id}`, data)
}

export function deletePosition(id) {
  return request.delete(`/system/positions/${id}`)
}
