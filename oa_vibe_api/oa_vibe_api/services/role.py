"""Role service."""
from typing import Optional, List
from oa_vibe_api.db.models import Role


class RoleService:
    """Service for role operations."""

    @staticmethod
    async def create_role(name: str, code: str, description: Optional[str] = None) -> Role:
        """Create a new role."""
        role = Role(name=name, code=code, description=description)
        await role.save()
        return role

    @staticmethod
    async def get_role_by_id(role_id: int) -> Optional[Role]:
        """Get role by ID."""
        return await Role.filter(id=role_id).first()

    @staticmethod
    async def list_roles(status: Optional[int] = None) -> List[Role]:
        """List roles with optional status filter."""
        query = Role.all()
        if status is not None:
            query = query.filter(status=status)
        else:
            query = query.filter(status=1)
        return await query.order_by("id")

    @staticmethod
    async def update_role(
        role_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[int] = None,
    ) -> Optional[Role]:
        """Update role information."""
        role = await Role.filter(id=role_id).first()
        if not role:
            return None
        if name is not None:
            role.name = name
        if description is not None:
            role.description = description
        if status is not None:
            role.status = status
        await role.save()
        return role

    @staticmethod
    async def delete_role(role_id: int) -> bool:
        """Soft delete a role."""
        role = await Role.filter(id=role_id).first()
        if not role:
            return False
        role.status = 0
        await role.save()
        return True


role_service = RoleService()
