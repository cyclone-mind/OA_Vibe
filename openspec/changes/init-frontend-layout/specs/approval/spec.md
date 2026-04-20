## ADDED Requirements

### Requirement: 审批中心路由
审批中心 SHALL 路由路径为 `/approval`

### Requirement: 待审批列表
审批中心 SHALL 显示待审批的请假单列表，包含申请人、请假类型、日期范围等字段

### Requirement: 已审批列表
审批中心 SHALL 提供切换到"已审批"列表的功能，显示历史审批记录

### Requirement: 批准操作
用户 SHALL 能批准选中的请假单，系统 SHALL 更新请假单状态为"已批准"

### Requirement: 拒绝操作
用户 SHALL 能拒绝选中的请假单，系统 SHALL 更新请假单状态为"已拒绝"

### Requirement: 批准评论
批准或拒绝时用户 SHALL 能输入审批评论

### Requirement: 审批操作按钮
待审批列表 SHALL 显示"批准"和"拒绝"操作按钮

#### Scenario: 管理员批准请假
- **WHEN** 管理员点击"批准"按钮
- **THEN** 系统 SHALL 调用批准接口
- **AND** 系统 SHALL 更新请假单状态为已批准
- **AND** 系统 SHALL 从待审批列表中移除

#### Scenario: 管理员拒绝请假
- **WHEN** 管理员点击"拒绝"按钮并填写拒绝原因
- **THEN** 系统 SHALL 调用拒绝接口
- **AND** 系统 SHALL 更新请假单状态为已拒绝
- **AND** 系统 SHALL 从待审批列表中移除
