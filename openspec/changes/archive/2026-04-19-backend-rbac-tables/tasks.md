## 1. 数据模型变更

- [x] 1.1 在 `oa_vibe_api/db/models/user.py` 的 User 模型中添加：
  - `role` 外键关联
  - `is_superuser` 布尔字段（默认 False）
- [x] 1.2 创建 `oa_vibe_api/db/models/role_permission.py` 角色-权限关联模型
- [x] 1.3 在 `oa_vibe_api/db/models/__init__.py` 中导出 RolePermission 模型
- [x] 1.4 执行数据库迁移生成 `sys_role_permission` 表并修改 `sys_user` 表 ✅

## 2. 服务层实现

- [x] 2.1 在 `oa_vibe_api/services/` 下创建 `role_permission.py` 服务（如果需要） - 无需单独服务，使用现有模型关联
- [x] 2.2 修改 `oa_vibe_api/services/menu.py` 添加 `get_user_menus()` 方法
  - 如果用户是 superuser，直接返回所有菜单
  - 否则：根据当前用户获取其角色
  - 根据角色获取所有权限点
  - 从权限点提取菜单 ID 列表
  - 返回去重后的菜单树

## 3. API 端点

- [x] 3.1 在 `oa_vibe_api/web/api/system/router.py` 添加 `GET /system/menus/user` 接口
- [x] 3.2 创建对应的 schema（如果需要）- 无需，返回 dict 树结构

## 4. 初始化数据

- [x] 4.1 创建 `oa_vibe_api/init_rbac_data.py` 脚本
  - 创建默认角色：admin（管理员）、employee（普通员工）
  - 创建基础权限点（至少包含菜单查看权限）
  - 为 admin 角色分配所有权限
  - 为 employee 角色分配基础权限
- [x] 4.2 运行初始化脚本并验证数据 ✅
  - 创建了 10 个默认菜单
  - admin 角色拥有全部 10 个权限
  - employee 角色拥有 5 个基础权限
  - admin 用户已更新为 superuser

## 5. 测试验证

- [x] 5.1 测试 superuser 用户获取所有菜单（不受角色限制） ✅ admin 用户可获取所有菜单
- [x] 5.2 测试 admin 用户获取完整菜单树 ✅
- [x] 5.3 测试 employee 用户获取过滤后的菜单树 ✅
- [x] 5.4 验证未分配角色的用户（role_id=NULL）只能看到基础菜单 ✅

## 6. 前置条件确认

- [x] 6.1 确认现有 Permission 数据中 `menu_id` 已正确关联 ✅
- [x] 6.2 确认 sys_menu 表中有基础菜单数据 ✅
