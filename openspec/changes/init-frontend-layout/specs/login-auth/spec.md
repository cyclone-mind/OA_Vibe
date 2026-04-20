## ADDED Requirements

### Requirement: 登录页面
登录页 SHALL 包含用户名输入框、密码输入框、登录按钮和错误提示

### Requirement: 登录请求
登录 SHALL 发送 POST 请求到 `/system/auth/login`，请求体为 `{username, password}`

### Requirement: 登录成功
登录成功后 SHALL 存储 access_token 和 refresh_token 到 localStorage，并跳转到首页 `/dashboard`

### Requirement: Token 管理
系统 SHALL 在后续请求的 Authorization 头中携带 `Bearer <access_token>`

### Requirement: 登出功能
用户点击退出时 SHALL 清除 localStorage 中的 Token 并跳转登录页

### Requirement: 401 处理
当响应状态码为 401 时，系统 SHALL 清除 Token 并跳转登录页

### Requirement: 路由守卫认证
对于需要认证的路由，如用户未登录 SHALL 跳转登录页

### Requirement: 登录状态保持
页面刷新时 SHALL 从 localStorage 恢复用户登录状态

#### Scenario: 用户成功登录
- **WHEN** 用户输入正确的用户名和密码并点击登录
- **THEN** 系统 SHALL 返回 access_token 和 refresh_token
- **AND** 系统 SHALL 存储 Token 到 localStorage
- **AND** 系统 SHALL 跳转到首页

#### Scenario: 用户登录失败
- **WHEN** 用户输入错误的用户名或密码
- **THEN** 系统 SHALL 显示错误提示"用户名或密码错误"

#### Scenario: Token 过期
- **WHEN** 用户操作时收到 401 响应
- **THEN** 系统 SHALL 清除本地 Token
- **AND** 系统 SHALL 跳转到登录页

#### Scenario: 访问未授权页面
- **WHEN** 用户尝试访问需要认证的页面但未登录
- **THEN** 系统 SHALL 跳转到登录页
