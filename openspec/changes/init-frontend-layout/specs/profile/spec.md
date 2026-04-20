## ADDED Requirements

### Requirement: 个人中心路由

个人中心 SHALL 路由路径为 `/profile`

### Requirement: 用户信息展示

个人中心 SHALL 展示当前用户的详细信息：用户名、真实姓名、邮箱、手机号、部门、职位、状态、创建时间

### Requirement: 信息编辑

个人中心 SHALL 提供编辑按钮，允许用户修改自己的邮箱和手机号

### Requirement: 密码修改

个人中心 SHOULD 提供修改密码功能

#### Scenario: 用户查看个人信息

- **WHEN** 用户访问个人中心页面
- **THEN** 系统 SHALL 显示当前用户的完整信息

#### Scenario: 用户更新个人信息

- **WHEN** 用户修改邮箱或手机号并保存
- **THEN** 系统 SHALL 调用更新接口保存更改
- **AND** 系统 SHALL 显示保存成功提示
