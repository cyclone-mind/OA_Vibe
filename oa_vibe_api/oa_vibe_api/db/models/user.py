from tortoise import fields, Model


class User(Model):
    """用户模型"""

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    password_hash = fields.CharField(max_length=255, description="密码哈希")
    real_name = fields.CharField(max_length=100, description="真实姓名")
    email = fields.CharField(max_length=100, null=True, description="邮箱")
    phone = fields.CharField(max_length=20, null=True, description="手机号")
    status = fields.IntField(default=1, description="状态: 1=正常, 0=停用")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    department: fields.ForeignKeyRelation["Department"] = fields.ForeignKeyField(
        "models.Department", related_name="users", null=True, on_delete=fields.SET_NULL
    )
    position: fields.ForeignKeyRelation["Position"] = fields.ForeignKeyField(
        "models.Position", related_name="users", null=True, on_delete=fields.SET_NULL
    )
    role: fields.ForeignKeyRelation["Role"] = fields.ForeignKeyField(
        "models.Role", related_name="users", null=True, on_delete=fields.SET_NULL
    )
    is_superuser: fields.BooleanField(default=False, description="超级管理员标志")

    class Meta:
        table = "sys_user"
