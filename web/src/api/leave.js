import request from './request'

export function getLeaveList(params) {
  return request.get('/oa/leave-requests', { params })
}

export function getLeaveDetail(id) {
  return request.get(`/oa/leave-requests/${id}`)
}

export function createLeave(data) {
  return request.post('/oa/leave-requests', data)
}

export function updateLeave(id, data) {
  return request.patch(`/oa/leave-requests/${id}`, data)
}

export function submitLeave(id) {
  return request.post(`/oa/leave-requests/${id}/submit`)
}

export function approveLeave(id, data) {
  return request.post(`/oa/leave-requests/${id}/approve`, data)
}

export function rejectLeave(id, data) {
  return request.post(`/oa/leave-requests/${id}/reject`, data)
}

export function cancelLeave(id) {
  return request.post(`/oa/leave-requests/${id}/cancel`)
}
