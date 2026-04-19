"""Models for oa_vibe_api."""
from oa_vibe_api.db.models.department import Department
from oa_vibe_api.db.models.menu import Menu
from oa_vibe_api.db.models.permission import Permission
from oa_vibe_api.db.models.position import Position
from oa_vibe_api.db.models.role import Role
from oa_vibe_api.db.models.user import User
from oa_vibe_api.db.models.leave_request import LeaveRequest

__all__ = [
    "Department",
    "Menu",
    "Permission",
    "Position",
    "Role",
    "User",
    "LeaveRequest",
]
