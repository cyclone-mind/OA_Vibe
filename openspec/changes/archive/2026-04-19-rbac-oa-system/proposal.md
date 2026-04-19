## Why

需要一个企业级RBAC权限OA系统，实现基于职位和部门的细粒度权限控制，支撑请假审批等OA业务流程。采用FastAPI + PostgreSQL技术栈，通过MCP协议集成，为后续OA功能扩展奠定基础。

## What Changes

- 新增职位管理（Position）：支持增删改查，与用户绑定
- 新增部门管理（Department）：支持树形结构，可嵌套子部门
- 新增菜单/权限管理（Menu/Permission）：基于RBAC的权限控制，支持菜单树和API权限
- 新增角色管理（Role）：关联权限集，职位可绑定角色
- 新增用户管理（User）：不包含注册，需管理员创建，支持JWT认证
- 新增登录/退出（Auth）：JWT Token认证，不开放注册
- 新增请假单（LeaveRequest）：员工提交请假申请，支持审批流程（MCP）
- system路由：/auth/login, /auth/logout, /positions, /departments, /menus, /roles, /users
- oa路由：/leave-requests, /leave-requests/{id}/approve, /leave-requests/{id}/reject

## Capabilities

### New Capabilities

- `user-auth`: 用户JWT认证，登录/退出，无注册功能，Token过期刷新
- `department`: 树形部门管理，支持创建/查询/更新部门及其子部门
- `position`: 职位管理，与用户一一对应，职位可绑定多个角色
- `role`: 角色管理，角色关联权限集，支持权限的批量分配
- `menu-permission`: 菜单与API权限管理，支持菜单树形结构，权限点关联API路径
- `leave-request`: 请假单管理，员工提交请假，支持审批状态流转

### Modified Capabilities

（无）

## Impact

- **代码**：新增 `oa_vibe_api/web/api/system/` (认证、职位、部门、菜单、角色、用户) 和 `oa_vibe_api/web/api/oa/` (请假单) 模块
- **数据模型**：Position, Department, Menu, Permission, Role, User, LeaveRequest 模型
- **依赖**：FastAPI, Tortoise ORM, Aerich, Pydantic, Loguru, PyJWT
- **API**：RESTful风格，JWT Bearer认证，统一响应格式
- **工作流**：请假单状态机 (draft → pending → approved/rejected)
