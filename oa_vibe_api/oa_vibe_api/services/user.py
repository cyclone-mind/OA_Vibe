"""User service."""
from typing import Optional, List
from oa_vibe_api.db.models import User
from oa_vibe_api.core.security import hash_password


class UserService:
    """Service for user operations."""

    @staticmethod
    async def create_user(
        username: str,
        password: str,
        real_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        department_id: Optional[int] = None,
        position_id: Optional[int] = None,
    ) -> User:
        """Create a new user."""
        user = User(
            username=username,
            password_hash=hash_password(password),
            real_name=real_name,
            email=email,
            phone=phone,
            department_id=department_id,
            position_id=position_id,
        )
        await user.save()
        return user

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID."""
        return await User.filter(id=user_id, status=1).first()

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        return await User.filter(username=username, status=1).first()

    @staticmethod
    async def list_users(
        skip: int = 0,
        limit: int = 20,
        department_id: Optional[int] = None,
        position_id: Optional[int] = None,
    ) -> List[User]:
        """List users with optional filters."""
        query = User.filter(status=1)
        if department_id:
            query = query.filter(department_id=department_id)
        if position_id:
            query = query.filter(position_id=position_id)
        return await query.offset(skip).limit(limit).order_by("-id")

    @staticmethod
    async def update_user(
        user_id: int,
        real_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        department_id: Optional[int] = None,
        position_id: Optional[int] = None,
        status: Optional[int] = None,
    ) -> Optional[User]:
        """Update user information."""
        user = await User.filter(id=user_id).first()
        if not user:
            return None
        if real_name is not None:
            user.real_name = real_name
        if email is not None:
            user.email = email
        if phone is not None:
            user.phone = phone
        if department_id is not None:
            user.department_id = department_id
        if position_id is not None:
            user.position_id = position_id
        if status is not None:
            user.status = status
        await user.save()
        return user

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Soft delete a user."""
        user = await User.filter(id=user_id).first()
        if not user:
            return False
        user.status = 0
        await user.save()
        return True


user_service = UserService()
