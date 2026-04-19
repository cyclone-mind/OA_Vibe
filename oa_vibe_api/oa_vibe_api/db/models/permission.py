from tortoise import fields, Model


class Permission(Model):
    """权限点模型"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, description="权限名称")
    code = fields.CharField(max_length=100, unique=True, description="权限编码")
    api_path = fields.CharField(max_length=200, null=True, description="API路径")
    method = fields.CharField(max_length=10, null=True, description="HTTP方法: GET/POST/PUT/DELETE/PATCH")
    status = fields.IntField(default=1, description="状态: 1=正常, 0=停用")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    menu: fields.ForeignKeyRelation["Menu"] = fields.ForeignKeyField(
        "models.Menu", related_name="permissions", null=True, on_delete=fields.SET_NULL
    )

    class Meta:
        table = "sys_permission"
