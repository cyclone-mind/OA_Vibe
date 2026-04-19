from tortoise import fields, Model


class RolePermission(Model):
    """角色-权限关联模型"""

    role: fields.ForeignKeyRelation["Role"] = fields.ForeignKeyField(
        "models.Role", related_name="role_permissions", on_delete=fields.CASCADE
    )
    permission: fields.ForeignKeyRelation["Permission"] = fields.ForeignKeyField(
        "models.Permission", related_name="role_permissions", on_delete=fields.CASCADE
    )

    class Meta:
        table = "sys_role_permission"
        unique_together = (("role", "permission"),)
