## Why

当前后端已建立 User、Role、Permission、Menu 数据模型，但这些模型之间缺乏关联：
- User 没有关联 Role
- 没有 Role-Permission 关联表
- 菜单 API 无法根据用户角色返回不同的菜单

前端需要 RBAC 权限系统来控制不同用户看到的菜单和可访问的功能。当前后端无法支持这一需求。

## What Changes

1. **User 模型新增 role_id 字段**
   - 每个用户关联一个角色（简单场景先支持单一角色）

2. **新增角色-权限关联表 `sys_role_permission`**
   - 建立 Role 与 Permission 的多对多关系
   - 支持一个角色拥有多个权限点

3. **新增用户-角色关联查询逻辑**
   - User → Role → Permissions → Menus 的权限链路
   - 提供 API 返回用户有权访问的菜单树

4. **更新菜单 API**
   - 新增 `GET /system/menus/user` 接口，返回当前用户可访问的菜单树
   - 基于用户角色拥有的权限自动过滤菜单

5. **补充初始化数据**
   - 创建默认角色（管理员、普通员工）
   - 创建默认权限点
   - 为管理员角色分配所有权限

## Capabilities

### New Capabilities

- `user-role-association`: 用户-角色关联能力
  - 用户关联角色，角色拥有权限，权限关联菜单
  - 实现基于角色的菜单过滤

## Impact

- **数据库**: 新增 `sys_role_permission` 表
- **模型**: 修改 `sys_user` 表新增 `role_id` 字段
- **API**: 新增 `GET /system/menus/user` 接口
- **服务层**: 修改 `menu_service` 添加基于用户权限的菜单过滤
