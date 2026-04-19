# oa_vibe_api

企业级 RBAC 权限 OA 系统后端，基于 FastAPI + PostgreSQL + Tortoise ORM。

## 启动方式

### 方式一：使用 python -m（推荐）

```bash
cd oa_vibe_api
python -m oa_vibe_api
```

### 方式二：使用 uvicorn

```bash
cd oa_vibe_api
uvicorn oa_vibe_api.web.application:get_app --reload --host 0.0.0.0 --port 8000
```

### 方式三：使用虚拟环境

```bash
# 激活虚拟环境
.\.venv\Scripts\activate

# 启动服务
python -m oa_vibe_api
```

服务器启动后访问：
- API 文档：http://localhost:8000/api/docs
- 管理账户：admin / admin123

## 环境配置

在项目根目录创建 `.env` 文件：

```bash
OA_VIBE_API_DB_HOST=dbconn.sealoshzh.site
OA_VIBE_API_DB_PORT=30241
OA_VIBE_API_DB_USER=postgres
OA_VIBE_API_DB_PASS=zrqx9q89
OA_VIBE_API_DB_BASE=postgres
OA_VIBE_API_RELOAD=true
OA_VIBE_API_PORT=8000
```

## 数据库迁移

```bash
# 生成迁移
aerich migrate

# 执行迁移
aerich upgrade
```

## 项目结构

```
oa_vibe_api/
├── db/
│   ├── config.py          # Tortoise ORM 配置
│   └── models/            # 数据模型
│       ├── department.py  # 部门（树形结构）
│       ├── position.py    # 职位
│       ├── role.py        # 角色
│       ├── menu.py        # 菜单
│       ├── permission.py  # 权限点
│       ├── user.py        # 用户
│       └── leave_request.py  # 请假单
├── services/              # 业务逻辑
│   ├── auth.py            # JWT 认证
│   ├── department.py
│   ├── position.py
│   ├── role.py
│   ├── menu.py
│   ├── permission.py
│   ├── user.py
│   └── leave_request.py   # 请假单审批流程
├── web/
│   └── api/
│       ├── router.py      # 主路由
│       ├── system/        # 系统管理 API
│       │   ├── auth/      # 登录/退出
│       │   ├── departments/
│       │   ├── positions/
│       │   ├── menus/
│       │   ├── roles/
│       │   └── users/
│       └── oa/            # OA 业务 API
│           └── leave-requests/  # 请假单
├── core/
│   ├── config.py
│   └── security.py        # JWT / bcrypt 密码工具
├── log.py                 # Loguru 日志配置
└── settings.py            # 应用配置
```

## API 路由

### System（系统管理）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/system/auth/login | 用户登录 |
| POST | /api/system/auth/logout | 用户退出 |
| POST | /api/system/auth/refresh | 刷新 Token |
| GET | /api/system/users/me | 当前用户信息 |
| CRUD | /api/system/departments | 部门管理 |
| CRUD | /api/system/positions | 职位管理 |
| CRUD | /api/system/roles | 角色管理 |
| CRUD | /api/system/menus | 菜单管理 |
| CRUD | /api/system/permissions | 权限点管理 |
| CRUD | /api/system/users | 用户管理 |

### OA（请假单）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/oa/leave-requests | 创建请假单（草稿） |
| GET | /api/oa/leave-requests | 列表查询 |
| GET | /api/oa/leave-requests/{id} | 详情 |
| PATCH | /api/oa/leave-requests/{id} | 更新草稿 |
| POST | /api/oa/leave-requests/{id}/submit | 提交审批 |
| POST | /api/oa/leave-requests/{id}/approve | 批准 |
| POST | /api/oa/leave-requests/{id}/reject | 拒绝 |
| POST | /api/oa/leave-requests/{id}/cancel | 取消 |

## 请假单状态流转

```
draft(草稿) → pending(待审批) → approved(已批准)
                               ↘ rejected(已拒绝)
```
