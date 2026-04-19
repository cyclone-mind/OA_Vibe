from tortoise import fields, Model


class Department(Model):
    """部门模型 - 支持树形结构"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, description="部门名称")
    level = fields.IntField(default=1, description="层级")
    sort = fields.IntField(default=0, description="排序")
    status = fields.IntField(default=1, description="状态: 1=正常, 0=停用")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    parent: fields.ForeignKeyRelation["Department"] = fields.ForeignKeyField(
        "models.Department", related_name="children", null=True, on_delete=fields.SET_NULL
    )
    children: fields.ReverseRelation["Department"]

    class Meta:
        table = "sys_department"
