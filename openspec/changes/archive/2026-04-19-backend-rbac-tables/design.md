## Context

### 当前状态

后端已建立基础 RBAC 模型：
- `sys_user` - 用户表
- `sys_role` - 角色表
- `sys_permission` - 权限点表（含 `menu_id` 关联菜单）
- `sys_menu` - 菜单表

但这些模型之间**缺乏关联**：
- User 没有 `role_id` 字段
- 没有 Role-Permission 关联表
- 菜单 API 返回所有菜单，不根据用户权限过滤

### 约束

- 使用 Tortoise ORM + PostgreSQL
- 保持 API 兼容性（现有接口不变）
- 支持未来的多角色扩展（但初始版本只支持单一角色）

## Goals / Non-Goals

**Goals:**
- 建立 User → Role → Permission → Menu 的权限链路
- 新增 API 返回当前用户可访问的菜单树
- 确保管理员拥有完整权限，普通员工按角色分配
- 支持超级管理员，可绕过权限限制访问所有菜单

**Non-Goals:**
- 不实现多角色（User 多角色关联）
- 不实现数据级别的行权限（如部门数据隔离）
- 不实现 API 级别的权限校验（只做菜单过滤）

## Decisions

### Decision 1: 用户-角色关联方式

**选择**: 单一角色（User.role_id → Role）

```python
class User(Model):
    role: fields.ForeignKeyRelation["Role"] = fields.ForeignKeyField(
        "models.Role", related_name="users", null=True
    )
```

**理由**:
- 简单实用，符合大多数 OA 系统场景
- 降低实现复杂度
- 后续可轻松扩展为多角色（N:N）

### Decision 2: 角色-权限关联表

**选择**: 新建 `sys_role_permission` 关联表

```python
class RolePermission(Model):
    role: fields.ForeignKeyRelation["Role"]
    permission: fields.ForeignKeyRelation["Permission"]

    class Meta:
        table = "sys_role_permission"
        unique_together = (("role", "permission"),)
```

**理由**:
- N:N 关系，支持一个角色拥有多个权限
- 符合标准 RBAC 实践
- 扩展性好

### Decision 3: 权限链路

```
User → role_id → Role → role_permissions → RolePermission → permission_id → Permission → menu_id → Menu
```

**理由**:
- 利用现有 Permission.menu_id 字段
- 菜单过滤逻辑清晰
- 从权限点可以找到对应菜单

### Decision 4: 新增 API

**选择**: 新增 `GET /system/menus/user` 而非修改现有 `/system/menus/tree`

```python
@router.get("/menus/user")
async def get_user_menus(current_user: User = Depends(get_current_user)):
    """Get menus accessible by current user's role."""
    return await menu_service.get_user_menus(current_user)
```

**理由**:
- 不破坏现有 API 兼容性
- 前端可通过统一入口获取权限菜单
- 职责分离清晰

### Decision 5: 超级管理员

**选择**: User 模型添加 `is_superuser` 布尔字段

```python
class User(Model):
    is_superuser: fields.BooleanField(default=False, description="超级管理员标志")
```

**权限判断逻辑**:
```python
def get_user_menus(user):
    if user.is_superuser:
        return all_menus  # 返回所有菜单
    # 否则走正常的 Role → Permission → Menu 链路
```

**理由**:
- 超级管理员可绕过角色权限限制，访问所有菜单
- 适合系统维护场景（即使没有任何角色分配也能管理系统）
- 简单明确，不影响普通用户的权限逻辑

### Decision 6: 默认数据

**初始角色**:
| 角色 | Code | 说明 |
|------|------|------|
| 管理员 | admin | 拥有所有权限 |
| 普通员工 | employee | 基础功能权限 |

**理由**:
- admin 用于系统管理
- employee 作为普通用户默认角色
- 确保新建用户有角色可归属

## Risks / Trade-offs

| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| 迁移复杂度 | 修改现有 User 表添加 role_id | 使用 Aerich 迁移工具 |
| 权限遗漏 | 初始角色权限分配可能不全 | 后续可调整权限配置 |
| 性能 | 菜单查询增加关联 | 考虑缓存用户菜单 |

## Open Questions

1. Permission 的 `api_path` 和 `method` 字段是否用于 API 拦截？
   - 当前方案只做菜单过滤，不做 API 级别校验
   - 如需 API 拦截，需要额外的请求拦截中间件

2. ~~是否需要"超级管理员"概念（不受权限控制）？~~ ✅ 已解决
   - 已在 Decision 5 中确认：添加 User.is_superuser 字段
