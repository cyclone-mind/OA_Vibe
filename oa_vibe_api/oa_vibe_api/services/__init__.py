"""Services for oa_vibe_api."""
from oa_vibe_api.services.auth import auth_service
from oa_vibe_api.services.user import user_service
from oa_vibe_api.services.department import department_service
from oa_vibe_api.services.position import position_service
from oa_vibe_api.services.role import role_service
from oa_vibe_api.services.menu import menu_service
from oa_vibe_api.services.permission import permission_service
from oa_vibe_api.services.leave_request import leave_request_service

__all__ = [
    "auth_service",
    "user_service",
    "department_service",
    "position_service",
    "role_service",
    "menu_service",
    "permission_service",
    "leave_request_service",
]
