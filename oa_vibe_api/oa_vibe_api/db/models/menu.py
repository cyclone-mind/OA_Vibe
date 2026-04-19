from tortoise import fields, Model


class Menu(Model):
    """菜单模型 - 支持树形结构"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, description="菜单名称")
    path = fields.CharField(max_length=200, null=True, description="路由路径")
    icon = fields.CharField(max_length=100, null=True, description="图标")
    sort = fields.IntField(default=0, description="排序")
    status = fields.IntField(default=1, description="状态: 1=正常, 0=停用")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    parent: fields.ForeignKeyRelation["Menu"] = fields.ForeignKeyField(
        "models.Menu", related_name="children", null=True, on_delete=fields.SET_NULL
    )
    children: fields.ReverseRelation["Menu"]

    class Meta:
        table = "sys_menu"
