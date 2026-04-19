## ADDED Requirements

### Requirement: Superuser Bypasses Role Permissions

超级管理员用户可以绕过角色权限限制，访问所有菜单。

#### Scenario: Superuser Gets All Menus
- **WHEN** 用户 `is_superuser=True` 请求获取可访问菜单
- **THEN** 返回系统中的所有菜单，不受角色权限限制

#### Scenario: Superuser Without Role Assignment
- **WHEN** 用户 `is_superuser=True` 但 `role_id=NULL`
- **THEN** 该用户仍然可以访问所有菜单

### Requirement: User Belongs to a Role

系统中的每个用户必须关联一个角色，用户拥有的权限由其角色决定。

#### Scenario: User with Admin Role
- **WHEN** 用户 "admin" 关联角色 "admin"（管理员）
- **THEN** 该用户可以访问所有菜单

#### Scenario: User with Employee Role
- **WHEN** 用户 "zhangsan" 关联角色 "employee"（普通员工）
- **THEN** 该用户只能访问基础功能菜单（首页、请假、审批、个人中心）

### Requirement: Role Has Multiple Permissions

一个角色可以拥有多个权限点，权限点关联到具体的菜单。

#### Scenario: Admin Role Has All Permissions
- **WHEN** 查询角色 "admin" 的权限
- **THEN** 返回所有权限点

#### Scenario: Employee Role Has Limited Permissions
- **WHEN** 查询角色 "employee" 的权限
- **THEN** 只返回基础功能相关的权限点

### Requirement: User Can Access Menus Based on Role

系统应根据用户角色返回其可访问的菜单树。

#### Scenario: Get Accessible Menus for Admin
- **WHEN** 管理员用户请求获取可访问菜单
- **THEN** 返回完整菜单树（所有菜单）

#### Scenario: Get Accessible Menus for Employee
- **WHEN** 普通员工用户请求获取可访问菜单
- **THEN** 返回过滤后的菜单树（仅基础功能菜单）

### Requirement: Menu Tree Filtered by Permissions

菜单树接口返回的菜单应基于用户角色拥有的权限进行过滤。

#### Scenario: Filtered Menu Tree Response
- **WHEN** 调用 `GET /api/system/menus/user` 接口
- **THEN** 返回当前用户角色可访问的菜单树结构

### Requirement: New User Gets Default Role

新建用户时，如未指定角色，应分配默认角色。

#### Scenario: Create User Without Role
- **WHEN** 创建新用户时未指定 role_id
- **THEN** 该用户的 role_id 为 NULL，无法访问系统管理功能
- **AND** 建议在用户创建后立即分配角色

### Requirement: Permission Links to Menu

每个权限点应关联到一个菜单，菜单通过权限点实现访问控制。

#### Scenario: Permission With Menu Link
- **WHEN** 权限点 "user:view" 关联菜单 "用户管理"
- **THEN** 拥有该权限的用户可以在菜单树中看到"用户管理"
