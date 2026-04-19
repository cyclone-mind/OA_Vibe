"""创建初始管理员用户"""
import asyncio
from tortoise import Tortoise
from oa_vibe_api.db.config import TORTOISE_CONFIG
from oa_vibe_api.core.security import hash_password


async def create_admin():
    await Tortoise.init(config=TORTOISE_CONFIG)

    # 导入模型
    from oa_vibe_api.db.models import User, Department, Position, Role

    # 创建默认部门（如果不存在）
    dept, created = await Department.get_or_create(
        id=1,
        defaults={"name": "总公司", "level": 1}
    )
    if created:
        print(f"Created department: {dept.name}")

    # 创建默认职位（如果不存在）
    pos, created = await Position.get_or_create(
        id=1,
        defaults={"name": "管理员", "code": "admin"}
    )
    if created:
        print(f"Created position: {pos.name}")

    # 获取管理员角色
    admin_role = await Role.filter(code="admin").first()
    if not admin_role:
        admin_role, _ = await Role.get_or_create(
            code="admin",
            defaults={"name": "管理员", "description": "系统管理员"}
        )
        print(f"Created admin role")

    # 创建管理员用户
    username = "admin"
    password = "admin123"  # 生产环境请修改为强密码

    existing = await User.filter(username=username).first()
    if existing:
        # Update existing user with role and superuser flag
        existing.role = admin_role
        existing.is_superuser = True
        await existing.save()
        print(f"Updated user '{username}' to superuser with admin role")
    else:
        user = await User.create(
            username=username,
            password_hash=hash_password(password),
            real_name="系统管理员",
            email="admin@example.com",
            department=dept,
            position=pos,
            role=admin_role,
            is_superuser=True,
            status=1
        )
        print(f"Created user: {username}")
        print(f"Password: {password}")
        print(f"Role: admin (superuser)")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(create_admin())
