## ADDED Requirements

### Requirement: 用户管理路由
用户管理页 SHALL 路由路径为 `/system/users`

### Requirement: 用户列表
用户管理页 SHALL 显示用户列表（分页），包含用户名、真实姓名、邮箱、部门、职位、状态等信息

### Requirement: 创建用户
管理员 SHALL 能创建新用户，填写用户名、密码、真实姓名、邮箱、手机号、部门、职位

### Requirement: 编辑用户
管理员 SHALL 能编辑已有用户信息

### Requirement: 删除用户
管理员 SHALL 能删除用户（软删除或硬删除）

### Requirement: 分配角色
管理员 SHALL 能为用户分配角色

### Requirement: 筛选功能
用户列表 SHALL 支持按部门、职位、状态筛选

### Requirement: 仅管理员可见
用户管理页 SHALL 仅角色为管理员或超级管理员的用户可见

#### Scenario: 管理员创建用户
- **WHEN** 管理员填写用户信息并点击创建
- **THEN** 系统 SHALL 调用创建用户接口
- **AND** 系统 SHALL 在用户列表中显示新用户

#### Scenario: 管理员分配角色
- **WHEN** 管理员为用户选择角色并保存
- **THEN** 系统 SHALL 调用分配角色接口
- **AND** 系统 SHALL 更新用户的角色信息
