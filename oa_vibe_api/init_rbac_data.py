"""Initialize RBAC data script.

Run this script to create default roles, permissions, and role-permission associations.

Usage:
    python init_rbac_data.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from oa_vibe_api.db.config import TORTOISE_CONFIG
from oa_vibe_api.db.models import Role, Permission, RolePermission, Menu
from tortoise import Tortoise


async def init_rbac_data():
    """Initialize RBAC data."""
    print("Initializing RBAC data...")

    # Initialize Tortoise ORM
    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas()

    # Create default roles
    roles_data = [
        {"name": "管理员", "code": "admin", "description": "系统管理员，拥有所有权限"},
        {"name": "普通员工", "code": "employee", "description": "普通员工，拥有基础权限"},
    ]

    created_roles = {}
    for role_data in roles_data:
        role, created = await Role.get_or_create(
            code=role_data["code"],
            defaults={
                "name": role_data["name"],
                "description": role_data["description"],
            }
        )
        created_roles[role.code] = role
        print(f"  {'Created' if created else 'Found'} role: {role.name} ({role.code})")

    # Get all menus
    menus = await Menu.filter(status=1)
    menu_map = {m.id: m for m in menus}
    print(f"  Found {len(menus)} menus")

    # Create permissions for each menu
    created_permissions = []
    for menu in menus:
        permission, created = await Permission.get_or_create(
            code=f"{menu.id}:view",
            defaults={
                "name": f"{menu.name}查看",
                "menu_id": menu.id,
            }
        )
        created_permissions.append(permission)
        if created:
            print(f"  Created permission: {permission.name} ({permission.code})")

    # Assign all permissions to admin role
    admin_role = created_roles.get("admin")
    if admin_role:
        for perm in created_permissions:
            rp, created = await RolePermission.get_or_create(
                role=admin_role,
                permission=perm,
            )
            if created:
                print(f"  Assigned permission {perm.code} to admin role")

    # Employee role gets only basic permissions (menus with id 1-5, typically: dashboard, leave, approval, profile)
    employee_role = created_roles.get("employee")
    if employee_role:
        basic_menu_ids = [m.id for m in menus if m.id <= 5]
        for perm in created_permissions:
            if perm.menu_id in basic_menu_ids:
                rp, created = await RolePermission.get_or_create(
                    role=employee_role,
                    permission=perm,
                )
                if created:
                    print(f"  Assigned permission {perm.code} to employee role")

    print("\nRBAC data initialization complete!")
    print(f"  Admin role has {len(created_permissions)} permissions")
    print(f"  Employee role has {len([p for p in created_permissions if p.menu_id <= 5])} basic permissions")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(init_rbac_data())
