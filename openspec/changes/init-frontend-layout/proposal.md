## Why

OA_Vibe 后端已完成 RBAC 权限系统实现，前端应用需要初始化 Vue 3 项目并实现所有页面框架，包括登录、布局、各业务模块页面和系统管理页面，为前后端联调做好准备。

## What Changes

- 使用 `create-vue` 初始化 Vue 3 前端项目到 `web/` 目录
- 安装依赖：Vue Router、Pinia、Element Plus、ECharts、Axios
- 实现主布局组件（顶部栏 + 左侧菜单 + Tab 导航 + 主内容区）
- 实现路由级 Tab 页切换机制
- 实现登录页面及 JWT 认证拦截器
- 实现请求/响应拦截器（Token 注入、401 处理）
- 实现路由守卫（权限控制）
- 创建所有业务页面：首页、请假管理、审批中心、个人中心
- 创建系统管理页面：用户管理、部门管理、职位管理、角色管理、菜单管理、权限管理
- 补充 frontend-app-spec.md 中的项目结构内容

## Capabilities

### New Capabilities

- `frontend-app`: 前端应用主体结构，包含项目初始化、布局框架、路由配置、状态管理、拦截器等核心基础设施
- `login-auth`: 登录认证模块，包含登录页面、Token 管理、路由守卫
- `dashboard`: 首页模块，包含统计卡片、ECharts 图表展示
- `leave-management`: 请假管理模块，包含请假列表、新建请假、详情弹窗
- `approval`: 审批中心模块，包含待审批列表、已审批列表、批准/拒绝操作
- `profile`: 个人中心模块，包含用户信息展示与编辑
- `system-users`: 系统用户管理模块，包含用户 CRUD、角色分配
- `system-departments`: 部门管理模块，包含部门树、CRUD、拖拽排序
- `system-positions`: 职位管理模块，包含职位 CRUD
- `system-roles`: 角色管理模块，包含角色 CRUD、权限配置
- `system-menus`: 菜单管理模块，包含菜单树、CRUD、图标选择、排序
- `system-permissions`: 权限管理模块，包含权限列表、CRUD、菜单/API 关联

### Modified Capabilities

- `frontend-app-spec`: 补充项目结构定义，更新下一步计划状态

## Impact

- **新增目录**: `web/` - Vue 3 前端项目
- **依赖变化**: 新增 vue-router, pinia, element-plus, echarts, axios
- **配置变化**: Vite 配置（代理 API）、环境变量
- **无 API 变更**: 前端对接现有后端 API 端点
