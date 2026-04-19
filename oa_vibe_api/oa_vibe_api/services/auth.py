"""Authentication service."""
from typing import Optional, Tuple
from oa_vibe_api.db.models import User
from oa_vibe_api.core.security import verify_password, create_access_token, create_refresh_token, decode_token


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    async def authenticate(username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = await User.filter(username=username, status=1).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_tokens(user_id: int, username: str) -> Tuple[str, str]:
        """Create access and refresh tokens for a user."""
        access_token = create_access_token({"sub": str(user_id), "username": username})
        refresh_token = create_refresh_token({"sub": str(user_id), "username": username})
        return access_token, refresh_token

    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[Tuple[str, str]]:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None
        user_id = int(payload.get("sub"))
        username = payload.get("username")
        return AuthService.create_tokens(user_id, username)


auth_service = AuthService()
