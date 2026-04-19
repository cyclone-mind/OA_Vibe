"""创建初始管理员用户"""
import asyncio
from tortoise import Tortoise
from oa_vibe_api.db.config import TORTOISE_CONFIG
from oa_vibe_api.core.security import hash_password


async def create_admin():
    await Tortoise.init(config=TORTOISE_CONFIG)

    # 导入模型
    from oa_vibe_api.db.models import User, Department, Position

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

    # 创建管理员用户
    username = "admin"
    password = "admin123"  # 生产环境请修改为强密码

    existing = await User.filter(username=username).first()
    if existing:
        print(f"User '{username}' already exists")
    else:
        user = await User.create(
            username=username,
            password_hash=hash_password(password),
            real_name="系统管理员",
            email="admin@example.com",
            department=dept,
            position=pos,
            status=1
        )
        print(f"Created user: {username}")
        print(f"Password: {password}")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(create_admin())
