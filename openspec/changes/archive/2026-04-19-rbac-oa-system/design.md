## Context

当前需要一个企业级RBAC权限OA系统后端，基于FastAPI + PostgreSQL技术栈。项目采用Tortoise ORM + Aerich进行数据库迁移管理，Loguru进行日志记录，JWT进行用户认证。

核心需求：
- 基于职位(Position)和部门(Department)的RBAC权限控制
- 部门支持树形结构嵌套
- 菜单(Menu)与API权限(Permission)关联
- 角色(Role)可绑定多个权限
- 用户(User)由管理员创建，不开放注册
- 请假单(LeaveRequest)支持审批流程

## Goals / Non-Goals

**Goals:**
- 实现完整的RBAC权限体系（用户-角色-权限）
- 支持部门树形结构
- 实现JWT认证的登录/退出
- 实现请假单CRUD及审批流程
- MCP协议集成支持

**Non-Goals:**
- 前端页面（纯后端API）
- 用户自主注册
- 其他OA流程（仅请假单）
- 钉钉/企业微信等第三方集成

## Decisions

### 1. 项目结构（适配 oa_vibe_api 模板）

```
oa_vibe_api/
├── db/
│   ├── config.py              # TORTOISE_CONFIG（保持不变）
│   ├── models/
│   │   ├── __init__.py        # 模型导入
│   │   ├── department.py     # Department 模型
│   │   ├── position.py        # Position 模型
│   │   ├── role.py            # Role 模型
│   │   ├── menu.py            # Menu 模型
│   │   ├── permission.py      # Permission 模型
│   │   ├── user.py            # User 模型
│   │   └── leave_request.py   # LeaveRequest 模型
│   └── migrations/
│       └── models/             # Aerich SQL 迁移文件
├── services/
│   ├── __init__.py
│   ├── auth.py                # JWT认证服务
│   ├── department.py          # 部门服务
│   ├── position.py            # 职位服务
│   ├── role.py                # 角色服务
│   ├── menu.py                # 菜单服务
│   ├── permission.py          # 权限服务
│   ├── user.py                # 用户服务
│   └── leave_request.py       # 请假单服务
├── web/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py          # 主路由（include system/ 和 oa/）
│   │   ├── system/            # system路由：认证、部门、职位、菜单、角色、用户
│   │   │   ├── __init__.py
│   │   │   ├── router.py      # system API 路由
│   │   │   ├── schemas.py     # Pydantic schemas
│   │   │   └── deps.py        # 依赖注入（JWT验证、权限检查）
│   │   └── oa/                # oa路由：请假单
│   │       ├── __init__.py
│   │       ├── router.py      # oa API 路由
│   │       └── schemas.py     # Pydantic schemas
│   ├── application.py         # get_app()（保持不变）
│   └── lifespan.py            # lifespan（保持不变）
├── utils/
│   ├── __init__.py
│
├── log.py                     # 日志配置（保持不变）
└── settings.py                # 配置（保持不变）
```

**Why**: 完全适配 `oa_vibe_api` 模板结构，模型放 `db/models/`，API路由放 `web/api/`，业务逻辑放 `services/`

### 2. 数据模型设计

**Department (部门)**
- id, name, parent_id(自关联), level, sort, status, created_at, updated_at
- 支持无限层级树形结构

**Position (职位)**
- id, name, code, status, created_at, updated_at
- 与Role多对多

**Role (角色)**
- id, name, code, description, status, created_at, updated_at
- 与Position多对多，与Permission多对多

**Menu (菜单)**
- id, name, path, icon, parent_id(自关联), sort, status, created_at, updated_at

**Permission (权限点)**
- id, name, code, menu_id(关联菜单), api_path, method, status, created_at, updated_at

**User (用户)**
- id, username, password_hash, real_name, email, phone, department_id, position_id, status, created_at, updated_at
- 无注册接口

**LeaveRequest (请假单)**
- id, user_id, leave_type, start_date, end_date, reason, status, approver_id, approved_at, approved_comment, created_at, updated_at
- status: draft(草稿), pending(待审批), approved(已批准), rejected(已拒绝)

### 3. JWT认证方案

- Access Token: 15分钟有效期
- Refresh Token: 7天有效期
- Token存储在请求头 `Authorization: Bearer <token>`
- 密码使用bcrypt加密

### 4. 权限验证流程

```
请求 → JWT验证 → 获取用户 → 查询用户角色+权限 → 权限匹配 → 允许/拒绝
```

### 5. 请假审批流程

```
draft → pending → approved
              ↘ rejected
```

- 员工创建请假单(status=draft) → 提交审批(status=pending)
- 审批人(管理员/上级)批准或拒绝
- 审批后记录审批人、审批时间、审批意见

## Risks / Trade-offs

[Risk] 部门树形查询性能
→ Mitigation: 添加level和path字段优化递归查询，使用物化路径或闭包表

[Risk] 权限变更后Token仍有效
→ Mitigation: 短期Token(15min)，敏感操作需重新验证


## Open Questions

1. 审批人如何确定？是固定角色还是动态配置？
2. 请假类型是否需要配置（年假、病假、事假等）？
3. 是否需要消息通知（审批结果通知申请人）？
