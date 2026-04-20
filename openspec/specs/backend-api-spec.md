---
name: backend-api-spec
description: OA_Vibe 后端 API 统一规范文档，定义所有 API 端点的请求/响应格式
type: spec
---
# OA_Vibe API 规范

## 概述

- **Base URL**: `http://localhost:8000/api`
- **认证方式**: JWT Bearer Token
- **认证头**: `Authorization: Bearer <access_token>`
- **内容类型**: `application/json`

## 公共响应格式

### 成功响应

```json
{
  "id": 1,
  "field": "value"
}
```

### 错误响应

```json
{
  "detail": "错误描述信息"
}
```

### HTTP 状态码

| 状态码 | 说明                       |
| ------ | -------------------------- |
| 200    | 成功                       |
| 201    | 创建成功                   |
| 204    | 删除成功（无响应体）       |
| 400    | 请求参数错误               |
| 401    | 未授权（Token 无效或过期） |
| 404    | 资源不存在                 |
| 409    | 冲突（如唯一约束冲突）     |

---

## 认证 (`/api/system/auth`)

### POST /system/auth/login

用户登录

**认证**: 不需要

**请求体**:

```json
{
  "username": "string",
  "password": "string"
}
```

**响应** `200`:

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}
```

---

### POST /system/auth/logout

用户登出

**认证**: 需要

**请求体**: 无

**响应** `200`:

```json
{
  "message": "Logged out successfully"
}
```

---

### POST /system/auth/refresh

刷新访问令牌

**认证**: 不需要

**请求体**:

```json
{
  "refresh_token": "string"
}
```

**响应** `200`:

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}
```

**错误** `401`: refresh_token 无效或过期

---

## 用户管理 (`/api/system/users`)

### GET /system/users/me

获取当前用户信息

**认证**: 需要

**响应** `200`: [UserResponse](#userresponse)

---

### GET /system/users

获取用户列表

**认证**: 需要

**查询参数**:

| 参数          | 类型 | 默认值 | 说明       |
| ------------- | ---- | ------ | ---------- |
| skip          | int  | 0      | 跳过数量   |
| limit         | int  | 20     | 返回数量   |
| department_id | int  | -      | 按部门筛选 |
| position_id   | int  | -      | 按职位筛选 |

**响应** `200`: `UserResponse[]`

---

### POST /system/users

创建用户

**认证**: 需要

**请求体**:

```json
{
  "username": "string",
  "password": "string",
  "real_name": "string",
  "email": "string?",
  "phone": "string?",
  "department_id": "number?",
  "position_id": "number?"
}
```

**响应** `201`: [UserResponse](#userresponse)

**错误** `409`: 用户名已存在

---

### GET /system/users/

获取用户详情

**认证**: 需要

**路径参数**: `user_id` - 用户 ID

**响应** `200`: [UserResponse](#userresponse)

**错误** `404`: 用户不存在

---

### PATCH /system/users/

更新用户

**认证**: 需要

**路径参数**: `user_id` - 用户 ID

**请求体**:

```json
{
  "real_name": "string?",
  "email": "string?",
  "phone": "string?",
  "department_id": "number?",
  "position_id": "number?",
  "status": "number?"
}
```

**响应** `200`: [UserResponse](#userresponse)

**错误** `404`: 用户不存在

---

### DELETE /system/users/

删除用户

**认证**: 需要

**路径参数**: `user_id` - 用户 ID

**响应** `204`: 无

**错误** `404`: 用户不存在

---

## 部门管理 (`/api/system/departments`)

### GET /system/departments

获取部门列表（扁平）

**认证**: 需要

**响应** `200`: `DepartmentResponse[]`

---

### GET /system/departments/tree

获取部门树结构

**认证**: 需要

**响应** `200`: 树形结构

---

### POST /system/departments

创建部门

**认证**: 需要

**请求体**:

```json
{
  "name": "string",
  "parent_id": "number?",
  "sort": "number"
}
```

**响应** `201`: [DepartmentResponse](#departmentresponse)

---

### GET /system/departments/

获取部门详情

**认证**: 需要

**路径参数**: `department_id` - 部门 ID

**响应** `200`: [DepartmentResponse](#departmentresponse)

**错误** `404`: 部门不存在

---

### PATCH /system/departments/

更新部门

**认证**: 需要

**路径参数**: `department_id` - 部门 ID

**请求体**:

```json
{
  "name": "string?",
  "parent_id": "number?",
  "sort": "number?",
  "status": "number?"
}
```

**响应** `200`: [DepartmentResponse](#departmentresponse)

---

### DELETE /system/departments/

删除部门

**认证**: 需要

**路径参数**: `department_id` - 部门 ID

**响应** `204`: 无

**错误** `409`: 无法删除（有子部门或用户）

---

## 职位管理 (`/api/system/positions`)

### GET /system/positions

获取职位列表

**认证**: 需要

**查询参数**:

| 参数   | 类型 | 说明       |
| ------ | ---- | ---------- |
| status | int? | 按状态筛选 |

**响应** `200`: `PositionResponse[]`

---

### POST /system/positions

创建职位

**认证**: 需要

**请求体**:

```json
{
  "name": "string",
  "code": "string"
}
```

**响应** `201`: [PositionResponse](#positionresponse)

**错误** `409`: 职位代码已存在

---

### GET /system/positions/

获取职位详情

**认证**: 需要

**响应** `200`: [PositionResponse](#positionresponse)

---

### PATCH /system/positions/

更新职位

**认证**: 需要

**请求体**:

```json
{
  "name": "string?",
  "status": "number?"
}
```

**响应** `200`: [PositionResponse](#positionresponse)

---

### DELETE /system/positions/

删除职位

**认证**: 需要

**响应** `204`: 无

**错误** `409`: 无法删除（有用户使用该职位）

---

## 角色管理 (`/api/system/roles`)

### GET /system/roles

获取角色列表

**认证**: 需要

**查询参数**:

| 参数   | 类型 | 说明       |
| ------ | ---- | ---------- |
| status | int? | 按状态筛选 |

**响应** `200`: `RoleResponse[]`

---

### POST /system/roles

创建角色

**认证**: 需要

**请求体**:

```json
{
  "name": "string",
  "code": "string",
  "description": "string?"
}
```

**响应** `201`: [RoleResponse](#roleresponse)

**错误** `409`: 角色代码已存在

---

### GET /system/roles/

获取角色详情

**认证**: 需要

**响应** `200`: [RoleResponse](#roleresponse)

---

### PATCH /system/roles/

更新角色

**认证**: 需要

**请求体**:

```json
{
  "name": "string?",
  "description": "string?",
  "status": "number?"
}
```

**响应** `200`: [RoleResponse](#roleresponse)

---

### DELETE /system/roles/

删除角色

**认证**: 需要

**响应** `204`: 无

**错误** `409`: 无法删除（有职位使用该角色）

---

## 菜单管理 (`/api/system/menus`)

### GET /system/menus

获取菜单列表（扁平）

**认证**: 需要

**响应** `200`: `MenuResponse[]`

---

### GET /system/menus/tree

获取菜单树结构

**认证**: 需要

**响应** `200`: 树形菜单结构

---

### GET /system/menus/user

**⚠️ 重要** 获取当前用户可访问的菜单（基于角色权限过滤）

**认证**: 需要

**响应** `200`: 当前用户角色可访问的菜单树

**说明**:

- 管理员角色返回所有菜单
- 普通员工角色返回基础菜单（首页、请假、审批、个人中心）
- 超级管理员用户返回所有菜单，不受角色限制

---

### POST /system/menus

创建菜单

**认证**: 需要

**请求体**:

```json
{
  "name": "string",
  "path": "string?",
  "icon": "string?",
  "parent_id": "number?",
  "sort": "number"
}
```

**响应** `201`: [MenuResponse](#menuresponse)

---

### PATCH /system/menus/

更新菜单

**认证**: 需要

**请求体**:

```json
{
  "name": "string?",
  "path": "string?",
  "icon": "string?",
  "parent_id": "number?",
  "sort": "number?",
  "status": "number?"
}
```

**响应** `200`: [MenuResponse](#menuresponse)

---

### DELETE /system/menus/

删除菜单

**认证**: 需要

**响应** `204`: 无

**错误** `409`: 无法删除（有子菜单）

---

## 权限管理 (`/api/system/permissions`)

### GET /system/permissions

获取权限列表

**认证**: 需要

**查询参数**:

| 参数    | 类型 | 说明       |
| ------- | ---- | ---------- |
| menu_id | int? | 按菜单筛选 |

**响应** `200`: `PermissionResponse[]`

---

### POST /system/permissions

创建权限

**认证**: 需要

**请求体**:

```json
{
  "name": "string",
  "code": "string",
  "api_path": "string?",
  "method": "string?",
  "menu_id": "number?"
}
```

**响应** `201`: [PermissionResponse](#permissionresponse)

**错误** `409`: 权限代码已存在

---

### PATCH /system/permissions/

更新权限

**认证**: 需要

**请求体**:

```json
{
  "name": "string?",
  "api_path": "string?",
  "method": "string?",
  "menu_id": "number?",
  "status": "number?"
}
```

**响应** `200`: [PermissionResponse](#permissionresponse)

---

### DELETE /system/permissions/

删除权限

**认证**: 需要

**响应** `204`: 无

---

## 请假流程 (`/api/oa/leave-requests`)

### POST /oa/leave-requests

创建请假单（草稿）

**认证**: 需要

**请求体**:

```json
{
  "leave_type": "annual | sick | personal",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "reason": "string"
}
```

**响应** `201`: [LeaveRequestResponse](#leaverequestresponse)

**错误** `400`: 结束日期早于开始日期

---

### GET /oa/leave-requests

获取请假单列表（当前用户的）

**认证**: 需要

**查询参数**:

| 参数       | 类型    | 默认值 | 说明         |
| ---------- | ------- | ------ | ------------ |
| status     | string? | -      | 筛选状态     |
| start_date | date?   | -      | 筛选开始日期 |
| end_date   | date?   | -      | 筛选结束日期 |
| skip       | int     | 0      | 跳过数量     |
| limit      | int     | 20     | 返回数量     |

**响应** `200`: `LeaveRequestResponse[]`

---

### GET /oa/leave-requests/

获取请假单详情

**认证**: 需要

**路径参数**: `leave_id` - 请假单 ID

**响应** `200`: [LeaveRequestResponse](#leaverequestresponse)

**错误** `404`: 请假单不存在

---

### PATCH /oa/leave-requests/

更新草稿状态的请假单

**认证**: 需要

**请求体**:

```json
{
  "leave_type": "annual | sick | personal?",
  "start_date": "YYYY-MM-DD?",
  "end_date": "YYYY-MM-DD?",
  "reason": "string?"
}
```

**响应** `200`: [LeaveRequestResponse](#leaverequestresponse)

**错误** `400`: 请假单不存在或不是草稿状态

---

### POST /oa/leave-requests//submit

提交请假单进行审批

**认证**: 需要

**响应** `200`: [LeaveRequestResponse](#leaverequestresponse)

**错误** `409`: 请假单不存在或不是草稿状态

---

### POST /oa/leave-requests//approve

批准请假单

**认证**: 需要

**请求体**:

```json
{
  "comment": "string?"
}
```

**响应** `200`: [LeaveRequestResponse](#leaverequestresponse)

**错误** `409`: 请假单不存在或不是待审批状态

---

### POST /oa/leave-requests//reject

拒绝请假单

**认证**: 需要

**请求体**:

```json
{
  "comment": "string?"
}
```

**响应** `200`: [LeaveRequestResponse](#leaverequestresponse)

**错误** `409`: 请假单不存在或不是待审批状态

---

### POST /oa/leave-requests//cancel

取消请假单

**认证**: 需要

**响应** `200`: [LeaveRequestResponse](#leaverequestresponse)

**错误** `409`: 请假单不存在或无法取消

---

## 数据模型

### UserResponse

```json
{
  "id": "number",
  "username": "string",
  "real_name": "string",
  "email": "string?",
  "phone": "string?",
  "department_id": "number?",
  "position_id": "number?",
  "status": "number",
  "created_at": "string (ISO8601)",
  "updated_at": "string (ISO8601)"
}
```

### DepartmentResponse

```json
{
  "id": "number",
  "name": "string",
  "parent_id": "number?",
  "level": "number",
  "sort": "number",
  "status": "number",
  "created_at": "string (ISO8601)",
  "updated_at": "string (ISO8601)"
}
```

### PositionResponse

```json
{
  "id": "number",
  "name": "string",
  "code": "string",
  "status": "number",
  "created_at": "string (ISO8601)",
  "updated_at": "string (ISO8601)"
}
```

### RoleResponse

```json
{
  "id": "number",
  "name": "string",
  "code": "string",
  "description": "string?",
  "status": "number",
  "created_at": "string (ISO8601)",
  "updated_at": "string (ISO8601)"
}
```

### MenuResponse

```json
{
  "id": "number",
  "name": "string",
  "path": "string?",
  "icon": "string?",
  "parent_id": "number?",
  "sort": "number",
  "status": "number",
  "created_at": "string (ISO8601)",
  "updated_at": "string (ISO8601)"
}
```

### PermissionResponse

```json
{
  "id": "number",
  "name": "string",
  "code": "string",
  "api_path": "string?",
  "method": "string?",
  "menu_id": "number?",
  "status": "number",
  "created_at": "string (ISO8601)",
  "updated_at": "string (ISO8601)"
}
```

### LeaveRequestResponse

```json
{
  "id": "number",
  "user_id": "number",
  "leave_type": "annual | sick | personal",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "reason": "string",
  "status": "draft | pending | approved | rejected | cancelled",
  "approver_id": "number?",
  "approved_at": "string? (ISO8601)",
  "approved_comment": "string?",
  "created_at": "string (ISO8601)",
  "updated_at": "string (ISO8601)"
}
```

---

## 请假单状态流转

```
                    ┌──────────┐
                    │  draft   │ ← 创建时的初始状态
                    └────┬─────┘
                         │ submit()
                         ▼
                    ┌──────────┐
         ┌──────────│ pending  │──────────┐
         │          └────┬─────┘          │
         │ cancel()      │         approve() / reject()
         ▼               │               │
    ┌──────────┐         │         ┌────┴────┐
    │ cancelled│         │         │         │
    └──────────┘         │         ▼         ▼
                          │   ┌─────────┐ ┌──────────┐
                          └──│ approved │ │ rejected │
                             └─────────┘ └──────────┘
```

---

## 角色权限说明

| 角色       | 代码     | 可访问菜单                 |
| ---------- | -------- | -------------------------- |
| 管理员     | admin    | 所有菜单                   |
| 普通员工   | employee | 首页、请假、审批、个人中心 |
| 超级管理员 | -        | 所有菜单（绕过角色限制）   |
