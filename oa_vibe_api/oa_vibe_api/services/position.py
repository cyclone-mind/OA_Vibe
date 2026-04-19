"""Position service."""
from typing import Optional, List
from oa_vibe_api.db.models import Position


class PositionService:
    """Service for position operations."""

    @staticmethod
    async def create_position(name: str, code: str) -> Position:
        """Create a new position."""
        position = Position(name=name, code=code)
        await position.save()
        return position

    @staticmethod
    async def get_position_by_id(position_id: int) -> Optional[Position]:
        """Get position by ID."""
        return await Position.filter(id=position_id).first()

    @staticmethod
    async def list_positions(status: Optional[int] = None) -> List[Position]:
        """List positions with optional status filter."""
        query = Position.all()
        if status is not None:
            query = query.filter(status=status)
        else:
            query = query.filter(status=1)
        return await query.order_by("id")

    @staticmethod
    async def update_position(
        position_id: int,
        name: Optional[str] = None,
        status: Optional[int] = None,
    ) -> Optional[Position]:
        """Update position information."""
        position = await Position.filter(id=position_id).first()
        if not position:
            return None
        if name is not None:
            position.name = name
        if status is not None:
            position.status = status
        await position.save()
        return position

    @staticmethod
    async def delete_position(position_id: int) -> bool:
        """Soft delete a position."""
        position = await Position.filter(id=position_id).first()
        if not position:
            return False
        position.status = 0
        await position.save()
        return True


position_service = PositionService()
