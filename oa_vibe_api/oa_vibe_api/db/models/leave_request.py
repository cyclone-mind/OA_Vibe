from tortoise import fields, Model


class LeaveRequest(Model):
    """请假单模型"""

    id = fields.IntField(pk=True)
    leave_type = fields.CharField(max_length=50, description="请假类型: annual/病假/sick/事假/personal")
    start_date = fields.DateField(description="开始日期")
    end_date = fields.DateField(description="结束日期")
    reason = fields.TextField(description="请假原因")
    status = fields.CharField(
        max_length=20,
        default="draft",
        description="状态: draft/pending/approved/rejected/cancelled"
    )
    approved_at = fields.DatetimeField(null=True, description="审批时间")
    approved_comment = fields.TextField(null=True, description="审批意见")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="leave_requests", on_delete=fields.CASCADE
    )
    approver: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="approved_leaves", null=True, on_delete=fields.SET_NULL
    )

    class Meta:
        table = "oa_leave_request"
