import request from './request'

export function login(data) {
  return request.post('/system/auth/login', data)
}

export function logout() {
  return request.post('/system/auth/logout')
}

export function refreshToken(data) {
  return request.post('/system/auth/refresh', data)
}

export function getCurrentUser() {
  return request.get('/system/users/me')
}
