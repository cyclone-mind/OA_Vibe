## 1. Project Setup

- [x] 1.1 Create `oa_vibe_api/db/models/` and `oa_vibe_api/web/api/` directory structure with `system/` and `oa/` modules
- [x] 1.2 Add dependencies to requirements.txt (fastapi, uvicorn, tortoise-orm, aerich, pydantic, pyjwt, bcrypt, loguru, python-multipart) - Template already has dependencies
- [x] 1.3 Create `core/config.py` with environment-based configuration - Template has settings.py
- [x] 1.4 Create `core/database.py` for Tortoise ORM initialization - TORTOISE_CONFIG in db/config.py
- [x] 1.5 Create `core/security.py` with JWT and password utilities
- [x] 1.6 Configure Aerich for database migrations - Aerich in MODELS_MODULES

## 2. Data Models

- [x] 2.1 Create `oa_vibe_api/db/models/department.py` with Department model (树形结构)
- [x] 2.2 Create `oa_vibe_api/db/models/position.py` with Position model
- [x] 2.3 Create `oa_vibe_api/db/models/role.py` with Role model
- [x] 2.4 Create `oa_vibe_api/db/models/menu.py` with Menu model
- [x] 2.5 Create `oa_vibe_api/db/models/permission.py` with Permission model
- [x] 2.6 Create `oa_vibe_api/db/models/user.py` with User model
- [x] 2.7 Create `oa_vibe_api/db/models/leave_request.py` with LeaveRequest model
- [x] 2.8 Run Aerich migrations to create database tables

## 3. System API - Auth

- [x] 3.1 Create `POST /api/system/auth/login` - User login with JWT
- [x] 3.2 Create `POST /api/system/auth/logout` - User logout
- [x] 3.3 Create `POST /api/system/auth/refresh` - Token refresh
- [x] 3.4 Create JWT dependency in `oa_vibe_api/web/api/system/deps.py` for authentication

## 4. System API - Department

- [x] 4.1 Create `POST /api/system/departments` - Create department
- [x] 4.2 Create `GET /api/system/departments` - List departments (flat)
- [x] 4.3 Create `GET /api/system/departments/tree` - Get department tree
- [x] 4.4 Create `GET /api/system/departments/{id}` - Get department detail
- [x] 4.5 Create `PATCH /api/system/departments/{id}` - Update department
- [x] 4.6 Create `DELETE /api/system/departments/{id}` - Delete department

## 5. System API - Position

- [x] 5.1 Create `POST /api/system/positions` - Create position
- [x] 5.2 Create `GET /api/system/positions` - List positions
- [x] 5.3 Create `GET /api/system/positions/{id}` - Get position detail
- [x] 5.4 Create `PATCH /api/system/positions/{id}` - Update position
- [x] 5.5 Create `PUT /api/system/positions/{id}/roles` - Assign roles to position (simplified, roles assigned via position update)
- [x] 5.6 Create `DELETE /api/system/positions/{id}` - Delete position

## 6. System API - Role

- [x] 6.1 Create `POST /api/system/roles` - Create role
- [x] 6.2 Create `GET /api/system/roles` - List roles
- [x] 6.3 Create `GET /api/system/roles/{id}` - Get role with permissions
- [x] 6.4 Create `PATCH /api/system/roles/{id}` - Update role
- [x] 6.5 Create `PUT /api/system/roles/{id}/permissions` - Assign permissions to role (simplified)
- [x] 6.6 Create `DELETE /api/system/roles/{id}` - Delete role

## 7. System API - Menu & Permission

- [x] 7.1 Create `POST /api/system/menus` - Create menu
- [x] 7.2 Create `GET /api/system/menus` - List menus (flat)
- [x] 7.3 Create `GET /api/system/menus/tree` - Get menu tree
- [x] 7.4 Create `PATCH /api/system/menus/{id}` - Update menu
- [x] 7.5 Create `DELETE /api/system/menus/{id}` - Delete menu
- [x] 7.6 Create `POST /api/system/permissions` - Create permission
- [x] 7.7 Create `GET /api/system/permissions` - List permissions
- [x] 7.8 Create `PATCH /api/system/permissions/{id}` - Update permission
- [x] 7.9 Create `DELETE /api/system/permissions/{id}` - Delete permission

## 8. System API - User

- [x] 8.1 Create `POST /api/system/users` - Create user (admin only)
- [x] 8.2 Create `GET /api/system/users` - List users
- [x] 8.3 Create `GET /api/system/users/{id}` - Get user detail
- [x] 8.4 Create `PATCH /api/system/users/{id}` - Update user
- [x] 8.5 Create `DELETE /api/system/users/{id}` - Delete user

## 9. OA API - Leave Request

- [x] 9.1 Create `POST /api/oa/leave-requests` - Create leave request (draft)
- [x] 9.2 Create `GET /api/oa/leave-requests` - List leave requests (filtered)
- [x] 9.3 Create `GET /api/oa/leave-requests/{id}` - Get leave request detail
- [x] 9.4 Create `PATCH /api/oa/leave-requests/{id}` - Update draft leave request
- [x] 9.5 Create `POST /api/oa/leave-requests/{id}/submit` - Submit for approval
- [x] 9.6 Create `POST /api/oa/leave-requests/{id}/approve` - Approve leave request
- [x] 9.7 Create `POST /api/oa/leave-requests/{id}/reject` - Reject leave request
- [x] 9.8 Create `POST /api/oa/leave-requests/{id}/cancel` - Cancel leave request

## 10. RBAC Permission Middleware

- [x] 10.1-10.2 Skipped (user requested basic auth only, no role-permission checks)
- [x] 10.3 Create `/api/system/users/me` endpoint for current user info

## 11. MCP Integration (Skipped per user request)

- [x] 11.1 Created `utils/mcp.py` placeholder for future MCP integration
- [x] 11.2-11.3 Skipped (user requested no MCP)

## 12. Testing & Documentation

- [x] 12.1 Write unit tests for core services (optional)
- [x] 12.2 Verify API endpoints with integration tests (optional)
- [x] 12.3 Update main.py with all routers
