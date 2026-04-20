## ADDED Requirements

### Requirement: Vue 3 项目初始化
前端项目 SHALL be 使用 `npm create vue@latest` 初始化到 `web/` 目录，使用 Vite 构建工具和 Composition API。

### Requirement: 依赖安装
项目 SHALL 安装以下依赖：vue-router, pinia, element-plus, echarts, axios

### Requirement: 主布局结构
应用 SHALL 包含以下布局区域：
- 顶部固定栏（56px）：Logo、系统名称、通知图标、用户下拉菜单、退出按钮
- 左侧菜单栏（固定宽度）：根据用户角色显示对应菜单
- Tab 导航栏：显示已打开的路由 Tab，支持切换和关闭
- 主内容区：根据当前路由显示对应页面

### Requirement: Vite 代理配置
Vite SHALL 配置代理将 `/api` 请求转发到 `http://localhost:8000/api`

### Requirement: 路由配置
应用 SHALL 配置以下路由：
- `/login` - 登录页（无需认证）
- `/dashboard` - 首页
- `/leave` - 请假管理
- `/approval` - 审批中心
- `/profile` - 个人中心
- `/system/users` - 用户管理
- `/system/departments` - 部门管理
- `/system/positions` - 职位管理
- `/system/roles` - 角色管理
- `/system/menus` - 菜单管理
- `/system/permissions` - 权限管理

### Requirement: 状态管理
应用 SHALL 使用 Pinia 管理以下状态：
- useUserStore：用户信息、Token
- useMenuStore：菜单树、权限菜单
- useTabStore：Tab 页列表、当前 Tab
- useLeaveStore：请假单列表（可选）

### Requirement: 请求拦截器
请求拦截器 SHALL 从 localStorage 获取 Token 并添加到 Authorization 头

### Requirement: 响应拦截器
响应拦截器 SHALL 处理 401 响应（跳转登录）和其他错误（显示错误提示）

### Requirement: 路由守卫
路由守卫 SHALL 检查目标路由是否需要认证，如未认证则跳转登录页

### Requirement: 菜单权限控制
菜单 SHALL 根据 `/system/menus/user` 接口返回的菜单列表渲染，超级管理员显示所有菜单

### Requirement: Tab 页切换
Tab 页 SHALL 对应不同路由，点击切换路由，支持关闭 Tab（移除路由）

### Requirement: 项目结构
frontend-app-spec.md SHALL 补充完整项目结构定义
