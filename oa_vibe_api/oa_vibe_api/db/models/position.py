from tortoise import fields, Model


class Position(Model):
    """职位模型"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, description="职位名称")
    code = fields.CharField(max_length=50, unique=True, description="职位编码")
    status = fields.IntField(default=1, description="状态: 1=正常, 0=停用")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "sys_position"
