---
name: frontend-app-spec
description: OA_Vibe 前端应用规格说明
type: spec
---
# OA_Vibe 前端应用规格说明

## 项目概述

- **项目名称**: OA_Vibe 前端
- **技术栈**: Vue 3 + Composition API + Vite + Pinia + Element Plus + Vue Router + ECharts
- **目标用户**: 企业内部所有员工

## 架构设计

### 整体布局

```
┌────────────────────────────────────────────────────────────┐
│  顶部固定栏 (56px)                                          │
│  [Logo] [系统名称]              [通知图标] [用户下拉] [退出]   │
├──────────────┬─────────────────────────────────────────────┤
│              │  Tab 导航栏                                  │
│  左侧菜单栏   │  [首页] [请假] [审批] [×]                    │
│  (固定宽度)   ├─────────────────────────────────────────────┤
│              │                                              │
│  【普通员工】  │              主内容区                        │
│  - 首页       │                                              │
│  - 请假管理    │         (根据路由显示对应页面)                │
│  - 审批中心    │                                              │
│  - 个人中心    │                                              │
│              │                                              │
│  【管理员】    │                                              │
│  - 系统管理    │                                              │
│    · 用户管理  │                                              │
│    · 部门管理  │                                              │
│    · 职位管理  │                                              │
│    · 角色管理  │                                              │
│    · 菜单管理  │                                              │
│    · 权限管理  │                                              │
│              │                                              │
└──────────────┴─────────────────────────────────────────────┘
```

### 角色菜单可见性

| 角色                               | 可见的菜单                         |
| ---------------------------------- | ---------------------------------- |
| 超级管理员 (`is_superuser=True`) | 所有菜单                           |
| 管理员 (admin)                     | 所有菜单（系统管理 + 业务模块）    |
| 普通员工 (employee)                | 首页、请假管理、审批中心、个人中心 |

> 菜单根据 `/system/menus/user` 接口返回，由后端根据用户角色过滤

### 路由级 Tab 页设计

- 每个 tab 对应一个路由
- 点击菜单切换路由，同时切换/新增 tab
- Tab 可关闭（移除路由）
- 当前 tab 高亮显示

## 后端 API 对接

### 基础信息

- **Base URL**: `http://localhost:8000/api`
- **认证方式**: JWT Bearer Token
- **认证头**: `Authorization: Bearer <access_token>`

### API 端点汇总

#### 认证 (`/system/auth`)

| 方法 | 路径                     | 请求体                   | 响应                                          |
| ---- | ------------------------ | ------------------------ | --------------------------------------------- |
| POST | `/system/auth/login`   | `{username, password}` | `{access_token, refresh_token, token_type}` |
| POST | `/system/auth/logout`  | -                        | `{message}`                                 |
| POST | `/system/auth/refresh` | `{refresh_token}`      | `{access_token, refresh_token, token_type}` |

#### 用户 (`/system/users`)

| 方法   | 路径                   | 说明             |
| ------ | ---------------------- | ---------------- |
| GET    | `/system/users/me`   | 获取当前用户信息 |
| GET    | `/system/users`      | 用户列表         |
| POST   | `/system/users`      | 创建用户         |
| GET    | `/system/users/{id}` | 用户详情         |
| PATCH  | `/system/users/{id}` | 更新用户         |
| DELETE | `/system/users/{id}` | 删除用户         |

#### 部门 (`/system/departments`)

| 方法   | 路径                         | 说明             |
| ------ | ---------------------------- | ---------------- |
| GET    | `/system/departments`      | 部门列表（扁平） |
| GET    | `/system/departments/tree` | 部门树结构       |
| POST   | `/system/departments`      | 创建部门         |
| GET    | `/system/departments/{id}` | 部门详情         |
| PATCH  | `/system/departments/{id}` | 更新部门         |
| DELETE | `/system/departments/{id}` | 删除部门         |

#### 职位 (`/system/positions`)

| 方法   | 路径                       | 说明     |
| ------ | -------------------------- | -------- |
| GET    | `/system/positions`      | 职位列表 |
| POST   | `/system/positions`      | 创建职位 |
| GET    | `/system/positions/{id}` | 职位详情 |
| PATCH  | `/system/positions/{id}` | 更新职位 |
| DELETE | `/system/positions/{id}` | 删除职位 |

#### 角色 (`/system/roles`)

| 方法   | 路径                   | 说明     |
| ------ | ---------------------- | -------- |
| GET    | `/system/roles`      | 角色列表 |
| POST   | `/system/roles`      | 创建角色 |
| GET    | `/system/roles/{id}` | 角色详情 |
| PATCH  | `/system/roles/{id}` | 更新角色 |
| DELETE | `/system/roles/{id}` | 删除角色 |

#### 菜单 (`/system/menus`)

| 方法   | 路径                   | 说明                             |
| ------ | ---------------------- | -------------------------------- |
| GET    | `/system/menus`      | 菜单列表（扁平）                 |
| GET    | `/system/menus/tree` | 菜单树结构                       |
| GET    | `/system/menus/user` | 当前用户可访问的菜单（基于角色） |
| POST   | `/system/menus`      | 创建菜单                         |
| PATCH  | `/system/menus/{id}` | 更新菜单                         |
| DELETE | `/system/menus/{id}` | 删除菜单                         |

#### 权限 (`/system/permissions`)

| 方法   | 路径                         | 说明     |
| ------ | ---------------------------- | -------- |
| GET    | `/system/permissions`      | 权限列表 |
| POST   | `/system/permissions`      | 创建权限 |
| PATCH  | `/system/permissions/{id}` | 更新权限 |
| DELETE | `/system/permissions/{id}` | 删除权限 |

#### 菜单 (`/system/menus`)

| 方法 | 路径                   | 说明                             |
| ---- | ---------------------- | -------------------------------- |
| GET  | `/system/menus`      | 菜单列表（扁平）                 |
| GET  | `/system/menus/tree` | 菜单树结构                       |
| GET  | `/system/menus/user` | 当前用户可访问的菜单（基于角色） |

#### 请假单 (`/oa/leave-requests`)

| 方法  | 路径                                | 说明               |
| ----- | ----------------------------------- | ------------------ |
| POST  | `/oa/leave-requests`              | 创建请假单（草稿） |
| GET   | `/oa/leave-requests`              | 请假单列表         |
| GET   | `/oa/leave-requests/{id}`         | 请假单详情         |
| PATCH | `/oa/leave-requests/{id}`         | 更新草稿           |
| POST  | `/oa/leave-requests/{id}/submit`  | 提交审批           |
| POST  | `/oa/leave-requests/{id}/approve` | 批准               |
| POST  | `/oa/leave-requests/{id}/reject`  | 拒绝               |
| POST  | `/oa/leave-requests/{id}/cancel`  | 取消               |

### 数据模型

#### 用户信息

```typescript
interface User {
  id: number;
  username: string;
  real_name: string;
  email?: string;
  phone?: string;
  department_id?: number;
  position_id?: number;
  status: number;
  created_at: string;
  updated_at: string;
}
```

#### 菜单节点

```typescript
interface MenuNode {
  id: number;
  name: string;
  path?: string;
  icon?: string;
  parent_id?: number;
  sort: number;
  children: MenuNode[];
}
```

#### 请假单

```typescript
interface LeaveRequest {
  id: number;
  user_id: number;
  leave_type: string;  // annual/sick/personal
  start_date: string;  // YYYY-MM-DD
  end_date: string;    // YYYY-MM-DD
  reason: string;
  status: string;      // draft/pending/approved/rejected/cancelled
  approver_id?: number;
  approved_at?: string;
  approved_comment?: string;
  created_at: string;
  updated_at: string;
}
```

### 权限控制

后端已实现完整的用户-角色-权限关联系统。前端使用 `/system/menus/user` 接口获取基于用户角色的过滤菜单。

- **超级管理员用户** (`is_superuser=True`)：可绕过角色权限限制，访问所有菜单
- **普通用户**：根据关联角色的权限访问对应菜单

> 详细说明参见 [backend-api-spec.md](./backend-api-spec.md) 和 [user-role-association/spec.md](./user-role-association/spec.md)

## 页面规划

### 登录页 (`/login`)

- 用户名/密码输入
- 登录按钮
- 错误提示

### 首页 (`/dashboard`)

- 统计数据卡片（Mock 数据）
- 待审批数量提醒
- ECharts 图表（假数据）

### 请假管理 (`/leave`)

- 我的请假列表
- 新建请假按钮
- 请假单详情弹窗
- 状态标签显示

### 审批中心 (`/approval`)

- 待审批列表
- 已审批列表
- 批准/拒绝操作

### 个人中心 (`/profile`)

- 用户信息展示
- 信息编辑

### 系统管理模块

> 以下页面仅管理员角色可见

#### 用户管理 (`/system/users`)

- 用户列表（分页、筛选）
- 创建用户
- 编辑用户
- 删除用户
- 分配角色

#### 部门管理 (`/system/departments`)

- 部门树形列表
- 创建/编辑/删除部门
- 部门拖拽排序

#### 职位管理 (`/system/positions`)

- 职位列表
- 创建/编辑/删除职位

#### 角色管理 (`/system/roles`)

- 角色列表
- 创建/编辑/删除角色
- 角色关联权限配置

#### 菜单管理 (`/system/menus`)

- 菜单树形列表
- 创建/编辑/删除菜单
- 菜单图标选择
- 菜单排序

#### 权限管理 (`/system/permissions`)

- 权限列表（按菜单分组）
- 创建/编辑/删除权限
- 权限关联菜单和 API 路径

## 拦截器设计

### 请求拦截器

1. 从 localStorage 获取 Token
2. 添加 `Authorization: Bearer <token>` 头
3. Token 过期时自动 refresh（401 响应时）

### 响应拦截器

1. 正常响应：直接返回 data
2. 401 未授权：跳转登录页
3. 其他错误：显示 Element Plus Message 错误提示

## 状态管理 (Pinia)

### stores

- `useUserStore` - 用户信息、Token
- `useMenuStore` - 菜单树、权限菜单
- `useTabStore` - Tab 页列表、当前 Tab
- `useLeaveStore` - 请假单列表（可选）

## 项目结构

```
web/
├── index.html
├── package.json
├── vite.config.js
├── public/
│   └── favicon.svg
└── src/
    ├── main.js                 # 应用入口
    ├── App.vue                 # 根组件
    ├── api/                    # API 请求封装
    │   ├── request.js          # Axios 实例 + 拦截器
    │   ├── auth.js             # 认证相关 API
    │   ├── user.js             # 用户管理 API
    │   ├── menu.js             # 菜单管理 API
    │   ├── leave.js            # 请假管理 API
    │   ├── department.js       # 部门管理 API
    │   ├── position.js         # 职位管理 API
    │   ├── role.js             # 角色管理 API
    │   └── permission.js       # 权限管理 API
    ├── router/
    │   └── index.js            # 路由配置 + 守卫
    ├── stores/                 # Pinia 状态管理
    │   ├── user.js              # 用户信息、Token
    │   ├── menu.js              # 菜单树、权限菜单
    │   ├── tab.js               # Tab 页列表、当前 Tab
    │   └── leave.js             # 请假单列表
    ├── views/                  # 页面组件
    │   ├── layout/              # 布局组件
    │   │   ├── MainLayout.vue   # 主布局
    │   │   ├── Header.vue       # 顶部栏
    │   │   ├── SideMenu.vue     # 左侧菜单
    │   │   └── TabNav.vue       # Tab 导航
    │   ├── login/
    │   │   └── Login.vue        # 登录页
    │   ├── dashboard/
    │   │   └── Dashboard.vue    # 首页
    │   ├── leave/
    │   │   └── Leave.vue        # 请假管理
    │   ├── approval/
    │   │   └── Approval.vue     # 审批中心
    │   ├── profile/
    │   │   └── Profile.vue      # 个人中心
    │   └── system/              # 系统管理
    │       ├── Users.vue        # 用户管理
    │       ├── Departments.vue  # 部门管理
    │       ├── Positions.vue    # 职位管理
    │       ├── Roles.vue        # 角色管理
    │       ├── Menus.vue        # 菜单管理
    │       └── Permissions.vue  # 权限管理
    └── assets/                  # 静态资源
```

## 下一步

1. ~~确认后端权限控制方案（是否需要补充用户-角色关联）~~ ✅ 后端 RBAC 已实现
2. ~~创建登录页面和布局框架~~ ✅ 已完成
3. ~~实现请求/响应拦截器~~ ✅ 已完成
4. ~~实现路由守卫~~ ✅ 已完成
5. ~~实现系统管理模块页面（用户/部门/职位/角色/菜单/权限）~~ ✅ 已完成
6. ~~实现业务模块页面（请假/审批）~~ ✅ 已完成
7. ~~实现首页和个人中心~~ ✅ 已完成
8. 前后端联调测试
9. 补充 Mock 数据和真实 API 替换
