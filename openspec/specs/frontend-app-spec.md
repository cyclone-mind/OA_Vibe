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
│  - 首页      │              主内容区                        │
│  - 请假管理   │                                              │
│  - 审批中心   │         (根据路由显示对应页面)                │
│  - 个人中心   │                                              │
│              │                                              │
│              │                                              │
└──────────────┴─────────────────────────────────────────────┘
```

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

| 方法 | 路径 | 请求体 | 响应 |
|------|------|--------|------|
| POST | `/system/auth/login` | `{username, password}` | `{access_token, refresh_token, token_type}` |
| POST | `/system/auth/logout` | - | `{message}` |
| POST | `/system/auth/refresh` | `{refresh_token}` | `{access_token, refresh_token, token_type}` |

#### 用户 (`/system/users`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/system/users/me` | 获取当前用户信息 |

#### 部门 (`/system/departments`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/system/departments` | 部门列表（扁平） |
| GET | `/system/departments/tree` | 部门树结构 |

#### 职位 (`/system/positions`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/system/positions` | 职位列表 |

#### 菜单 (`/system/menus`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/system/menus` | 菜单列表（扁平） |
| GET | `/system/menus/tree` | 菜单树结构 |

#### 请假单 (`/oa/leave-requests`)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/oa/leave-requests` | 创建请假单（草稿） |
| GET | `/oa/leave-requests` | 请假单列表 |
| GET | `/oa/leave-requests/{id}` | 请假单详情 |
| PATCH | `/oa/leave-requests/{id}` | 更新草稿 |
| POST | `/oa/leave-requests/{id}/submit` | 提交审批 |
| POST | `/oa/leave-requests/{id}/approve` | 批准 |
| POST | `/oa/leave-requests/{id}/reject` | 拒绝 |
| POST | `/oa/leave-requests/{id}/cancel` | 取消 |

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

> ⚠️ **待确认**: 后端当前没有用户-角色关联表
>
> 前端需要考虑：
> 1. **方案 A**: 前端硬编码菜单权限（不推荐）
> 2. **方案 B**: 后端补充用户-角色-权限关联表
> 3. **方案 C**: 菜单接口返回时过滤（简单但安全级别低）

建议：先使用 **方案 C**，后续补充完整 RBAC。

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
oa_vibe/
├── public/
├── src/
│   ├── api/              # API 请求模块
│   │   ├── request.ts     # axios 实例 + 拦截器
│   │   ├── auth.ts        # 认证相关 API
│   │   ├── user.ts        # 用户 API
│   │   ├── menu.ts        # 菜单 API
│   │   └── leave.ts       # 请假 API
│   ├── components/        # 公共组件
│   ├── layouts/           # 布局组件
│   │   └── MainLayout.vue
│   ├── pages/             # 页面组件
│   │   ├── Login.vue
│   │   ├── Dashboard.vue
│   │   ├── Leave.vue
│   │   ├── Approval.vue
│   │   └── Profile.vue
│   ├── router/            # 路由配置
│   ├── stores/            # Pinia stores
│   ├── styles/            # 全局样式
│   ├── utils/            # 工具函数
│   ├── App.vue
│   └── main.ts
├── index.html
├── vite.config.ts
└── package.json
```

## 下一步

1. 确认后端权限控制方案（是否需要补充用户-角色关联）
2. 创建登录页面和布局框架
3. 实现请求/响应拦截器
4. 实现路由守卫
5. 逐步实现各业务页面
