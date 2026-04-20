## ADDED Requirements

### Requirement: 角色管理路由
角色管理页 SHALL 路由路径为 `/system/roles`

### Requirement: 角色列表
角色管理页 SHALL 显示角色列表，包含角色名称、角色标识、描述、状态等字段

### Requirement: 创建角色
管理员 SHALL 能创建新角色，填写角色名称、角色标识、描述

### Requirement: 编辑角色
管理员 SHALL 能编辑角色信息

### Requirement: 删除角色
管理员 SHALL 能删除角色（需处理关联用户）

### Requirement: 权限配置
管理员 SHALL 能为角色分配权限，通过权限树勾选

### Requirement: 仅管理员可见
角色管理页 SHALL 仅管理员或超级管理员可见

#### Scenario: 管理员配置角色权限
- **WHEN** 管理员在角色编辑页面勾选权限并保存
- **THEN** 系统 SHALL 调用权限分配接口
- **AND** 系统 SHALL 更新角色的权限关联
