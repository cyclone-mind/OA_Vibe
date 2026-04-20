## Context

OA_Vibe 后端已完成 RBAC 权限系统（用户-角色-权限关联），前端应用需从零初始化。项目使用 Vue 3 + Vite + Composition API，技术栈已在前端规格说明中定义。前端需对接现有后端 API `/api` 端点。

## Goals / Non-Goals

**Goals:**
- 初始化 Vue 3 项目到 `web/` 目录，使用 `create-vue`
- 实现主布局框架：顶部栏 + 左侧菜单 + Tab 导航 + 主内容区
- 实现路由级 Tab 页切换机制
- 实现 JWT 认证（登录/登出/Token 刷新）
- 实现请求/响应拦截器
- 实现路由守卫（权限控制）
- 创建所有业务页面和系统管理页面
- 补充 frontend-app-spec.md 项目结构内容

**Non-Goals:**
- 后端实现（已独立完成）
- 真实 ECharts 数据（使用 Mock 数据）
- 移动端适配
- 单元测试/E2E 测试

## Decisions

### 1. 项目初始化方式

**决定**: 使用 `npm create vue@latest` 初始化项目

**理由**: Vue 官方 CLI 工具，集成 Vite + Composition API，支持 TypeScript/JSX/路由/状态管理等选项的交互式选择。相比 Vite 手动创建，create-vue 提供更规范的项目结构。

**替代方案**:
- Vite 手动创建: 需要手动配置 Vue 插件、路径别名等，增加配置成本
- Vue CLI: 已deprecated，官方推荐 create-vue + Vite

### 2. 目录结构

**决定**: 使用 src/views 按模块组织页面，src/components 放公共组件，src/stores 放 Pinia store

```
web/src/
├── api/          # API 请求封装
├── assets/       # 静态资源
├── components/   # 公共组件（布局、表格、表单等）
├── router/       # 路由配置
├── stores/       # Pinia 状态管理
├── utils/        # 工具函数
├── views/        # 页面组件
│   ├── layout/   # 布局组件
│   ├── login/    # 登录
│   ├── dashboard/# 首页
│   ├── leave/    # 请假管理
│   ├── approval/ # 审批中心
│   ├── profile/  # 个人中心
│   └── system/   # 系统管理模块
└── App.vue
```

**理由**: 符合 Vue 社区惯例，便于后续维护和扩展

### 3. 路由守卫方案

**决定**: 使用 Vue Router 的 `beforeEach` 守卫结合 Pinia store 中的用户状态

```typescript
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')
  } else {
    next()
  }
})
```

**理由**: 轻量级方案，无需额外依赖。配合路由 meta 信息可灵活控制权限。

### 4. 状态管理

**决定**: Pinia stores 分域管理（user/menu/tab/leave）

**理由**:
- 比 Vuex 更轻量，TypeScript 支持更好
- 分域管理避免单一 store 过于臃肿
- 支持组合式 store 写法

### 5. HTTP 请求封装

**决定**: Axios + 拦截器模式

```typescript
// 请求拦截器：注入 Token
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// 响应拦截器：401 处理 + 错误提示
axios.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // refresh 或跳转登录
    }
    return Promise.reject(error)
  }
)
```

**理由**: Axios 生态成熟，拦截器机制完善，是 Vue 项目事实标准

### 6. Tab 页实现方案

**决定**: 使用 `vue-router` 的动态路由 + Pinia `useTabStore` 管理 Tab 列表

- Tab 列表存储在 Pinia tabStore
- 切换 Tab 即切换路由
- 关闭 Tab 移除对应路由
- 路由缓存使用 `keep-alive`

**理由**: 利用 Vue Router 现有机制，无需额外标签页组件库

## Risks / Trade-offs

- [Risk] Element Plus 组件库体积较大 → [Mitigation] 按需引入，减少打包体积
- [Risk] 路由守卫的 token 校验依赖 localStorage → [Mitigation] Token 已通过 HTTPS传输，localStorage 在前端场景可接受
- [Risk] Mock 数据与真实 API 可能存在字段差异 → [Mitigation] 后续联调阶段统一核对字段

## Migration Plan

1. 初始化项目：`npm create vue@latest web`
2. 安装依赖：vue-router, pinia, element-plus, echarts, axios
3. 配置 Vite 代理：将 `/api` 代理到 `http://localhost:8000`
4. 实现布局组件和路由配置
5. 实现认证拦截器和路由守卫
6. 创建各业务页面
7. 补充 frontend-app-spec.md 项目结构

## Open Questions

- 是否需要实现 Token 自动刷新机制？（当前方案：401 时跳转登录）
- ECharts 图表的具体数据格式和刷新策略？
