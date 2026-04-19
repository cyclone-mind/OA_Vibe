"""Initialize default menu data.

Run this script to create default menus for the OA system.

Usage:
    python init_menu_data.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from oa_vibe_api.db.config import TORTOISE_CONFIG
from oa_vibe_api.db.models import Menu
from tortoise import Tortoise


async def init_menu_data():
    """Initialize default menu data."""
    print("Initializing menu data...")

    # Initialize Tortoise ORM
    await Tortoise.init(TORTOISE_CONFIG)

    # Default menus
    menus_data = [
        {"id": 1, "name": "首页", "path": "/dashboard", "icon": "HomeFilled", "sort": 1},
        {"id": 2, "name": "请假管理", "path": "/leave", "icon": "Calendar", "sort": 2},
        {"id": 3, "name": "审批中心", "path": "/approval", "icon": "Check", "sort": 3},
        {"id": 4, "name": "个人中心", "path": "/profile", "icon": "User", "sort": 4},
        {"id": 5, "name": "系统管理", "path": "/system", "icon": "Setting", "sort": 5},
        {"id": 6, "name": "部门管理", "path": "/system/department", "icon": "OfficeBuilding", "sort": 51, "parent_id": 5},
        {"id": 7, "name": "职位管理", "path": "/system/position", "icon": "Briefcase", "sort": 52, "parent_id": 5},
        {"id": 8, "name": "角色管理", "path": "/system/role", "icon": "Key", "sort": 53, "parent_id": 5},
        {"id": 9, "name": "用户管理", "path": "/system/user", "icon": "User", "sort": 54, "parent_id": 5},
        {"id": 10, "name": "菜单管理", "path": "/system/menu", "icon": "Menu", "sort": 55, "parent_id": 5},
    ]

    created_count = 0
    for menu_data in menus_data:
        menu, created = await Menu.get_or_create(
            id=menu_data["id"],
            defaults={
                "name": menu_data["name"],
                "path": menu_data.get("path"),
                "icon": menu_data.get("icon"),
                "sort": menu_data.get("sort", 0),
                "parent_id": menu_data.get("parent_id"),
                "status": 1,
            }
        )
        if created:
            created_count += 1
            print(f"  Created menu: {menu.name} (id={menu.id})")
        else:
            print(f"  Found menu: {menu.name} (id={menu.id})")

    print(f"\nMenu data initialization complete! Created {created_count} new menus.")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(init_menu_data())
