"""Permission service."""
from typing import Optional, List
from oa_vibe_api.db.models import Permission


class PermissionService:
    """Service for permission operations."""

    @staticmethod
    async def create_permission(
        name: str,
        code: str,
        api_path: Optional[str] = None,
        method: Optional[str] = None,
        menu_id: Optional[int] = None,
    ) -> Permission:
        """Create a new permission."""
        permission = Permission(
            name=name,
            code=code,
            api_path=api_path,
            method=method,
            menu_id=menu_id,
        )
        await permission.save()
        return permission

    @staticmethod
    async def get_permission_by_id(permission_id: int) -> Optional[Permission]:
        """Get permission by ID."""
        return await Permission.filter(id=permission_id).first()

    @staticmethod
    async def list_permissions(menu_id: Optional[int] = None, status: Optional[int] = None) -> List[Permission]:
        """List permissions with optional filters."""
        query = Permission.all()
        if status is not None:
            query = query.filter(status=status)
        else:
            query = query.filter(status=1)
        if menu_id is not None:
            query = query.filter(menu_id=menu_id)
        return await query.order_by("id")

    @staticmethod
    async def update_permission(
        permission_id: int,
        name: Optional[str] = None,
        api_path: Optional[str] = None,
        method: Optional[str] = None,
        menu_id: Optional[int] = None,
        status: Optional[int] = None,
    ) -> Optional[Permission]:
        """Update permission information."""
        permission = await Permission.filter(id=permission_id).first()
        if not permission:
            return None
        if name is not None:
            permission.name = name
        if api_path is not None:
            permission.api_path = api_path
        if method is not None:
            permission.method = method
        if menu_id is not None:
            permission.menu_id = menu_id
        if status is not None:
            permission.status = status
        await permission.save()
        return permission

    @staticmethod
    async def delete_permission(permission_id: int) -> bool:
        """Soft delete a permission."""
        permission = await Permission.filter(id=permission_id).first()
        if not permission:
            return False
        permission.status = 0
        await permission.save()
        return True


permission_service = PermissionService()
