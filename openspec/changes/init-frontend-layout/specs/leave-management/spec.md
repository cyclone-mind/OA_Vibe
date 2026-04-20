## ADDED Requirements

### Requirement: 请假列表页
请假管理页 SHALL 显示当前用户的请假单列表，包含状态标签、请假类型、日期范围等字段

### Requirement: 新建请假按钮
页面 SHALL 包含"新建请假"按钮，点击打开请假单填写弹窗

### Requirement: 新建请假弹窗
新建请假弹窗 SHALL 包含：请假类型选择（年假/病假/事假）、开始日期、结束日期、请假原因输入

### Requirement: 请假单提交
用户 SHALL 能提交请假单，状态从"草稿"变为"待审批"

### Requirement: 请假单详情
用户 SHALL 能查看请假单详情弹窗，显示完整的请假信息

### Requirement: 请假单取消
用户 SHALL 能取消自己提交的请假单（仅限草稿或待审批状态）

### Requirement: 状态标签显示
请假单列表 SHALL 使用不同颜色的标签显示状态：草稿(灰色)、待审批(蓝色)、已批准(绿色)、已拒绝(红色)、已取消(灰色)

### Requirement: 请假类型显示
请假单列表 SHALL 显示请假类型：年假、病假、事假

#### Scenario: 用户创建请假单
- **WHEN** 用户填写请假表单并点击提交
- **THEN** 系统 SHALL 创建请假单（草稿状态）
- **AND** 系统 SHALL 调用提交接口将状态改为待审批

#### Scenario: 用户查看请假详情
- **WHEN** 用户点击请假单列表中的某一项
- **THEN** 系统 SHALL 显示请假单详情弹窗
