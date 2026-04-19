"""Unit tests for core services."""
from datetime import datetime, timedelta

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from oa_vibe_api.services.auth import auth_service, AuthService
from oa_vibe_api.services.user import user_service, UserService
from oa_vibe_api.services.department import department_service, DepartmentService
from oa_vibe_api.services.leave_request import leave_request_service, LeaveRequestService
from oa_vibe_api.core.security import hash_password, verify_password


class TestSecurity:
    """Test security utilities."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password123"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Test verifying correct password."""
        password = "test_password123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        password = "test_password123"
        hashed = hash_password(password)

        assert verify_password("wrong_password", hashed) is False


class TestAuthService:
    """Test AuthService."""

    async def test_authenticate_success(self):
        """Test successful authentication."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.password_hash = hash_password("correct_password")

        with patch("oa_vibe_api.services.auth.User") as MockUser:
            MockUser.filter.return_value.first = AsyncMock(return_value=mock_user)

            result = await auth_service.authenticate("testuser", "correct_password")

            assert result == mock_user

    async def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user."""
        with patch("oa_vibe_api.services.auth.User") as MockUser:
            MockUser.filter.return_value.first = AsyncMock(return_value=None)

            result = await auth_service.authenticate("nonexistent", "password")

            assert result is None

    async def test_authenticate_wrong_password(self):
        """Test authentication with wrong password."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.password_hash = hash_password("correct_password")

        with patch("oa_vibe_api.services.auth.User") as MockUser:
            MockUser.filter.return_value.first = AsyncMock(return_value=mock_user)

            result = await auth_service.authenticate("testuser", "wrong_password")

            assert result is None

    def test_create_tokens(self):
        """Test token creation."""
        access_token, refresh_token = auth_service.create_tokens(1, "testuser")

        assert access_token is not None
        assert refresh_token is not None
        assert access_token != refresh_token

    def test_refresh_access_token_valid(self):
        """Test refreshing with valid token."""
        access_token, refresh_token = auth_service.create_tokens(1, "testuser")

        result = auth_service.refresh_access_token(refresh_token)

        assert result is not None
        new_access, new_refresh = result
        assert new_access != access_token
        assert new_refresh != refresh_token

    def test_refresh_access_token_invalid(self):
        """Test refreshing with invalid token."""
        result = auth_service.refresh_access_token("invalid_token")

        assert result is None


class TestUserService:
    """Test UserService."""

    async def test_create_user(self):
        """Test user creation."""
        with patch("oa_vibe_api.services.user.User") as MockUser:
            mock_user_instance = MagicMock()
            mock_user_instance.id = 1
            mock_user_instance.username = "newuser"
            mock_user_instance.save = AsyncMock()

            MockUser.return_value = mock_user_instance

            result = await user_service.create_user(
                username="newuser",
                password="password123",
                real_name="New User",
                email="new@example.com",
            )

            assert result.username == "newuser"
            mock_user_instance.save.assert_called_once()

    async def test_get_user_by_id(self):
        """Test getting user by ID."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "testuser"

        with patch("oa_vibe_api.services.user.User") as MockUser:
            MockUser.filter.return_value.first = AsyncMock(return_value=mock_user)

            result = await user_service.get_user_by_id(1)

            assert result == mock_user

    async def test_get_user_by_id_not_found(self):
        """Test getting non-existent user by ID."""
        with patch("oa_vibe_api.services.user.User") as MockUser:
            MockUser.filter.return_value.first = AsyncMock(return_value=None)

            result = await user_service.get_user_by_id(999)

            assert result is None

    async def test_delete_user(self):
        """Test soft deleting a user."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.status = 1
        mock_user.save = AsyncMock()

        with patch("oa_vibe_api.services.user.User") as MockUser:
            MockUser.filter.return_value.first = AsyncMock(return_value=mock_user)

            result = await user_service.delete_user(1)

            assert result is True
            assert mock_user.status == 0
            mock_user.save.assert_called_once()

    async def test_delete_user_not_found(self):
        """Test deleting non-existent user."""
        with patch("oa_vibe_api.services.user.User") as MockUser:
            MockUser.filter.return_value.first = AsyncMock(return_value=None)

            result = await user_service.delete_user(999)

            assert result is False


class TestDepartmentService:
    """Test DepartmentService."""

    async def test_create_department_root(self):
        """Test creating root department."""
        with patch("oa_vibe_api.services.department.Department") as MockDept:
            mock_dept = MagicMock()
            mock_dept.id = 1
            mock_dept.name = "Engineering"
            mock_dept.parent_id = None
            mock_dept.level = 1
            mock_dept.save = AsyncMock()
            MockDept.return_value = mock_dept

            result = await department_service.create_department(name="Engineering")

            assert result.name == "Engineering"
            assert result.level == 1
            mock_dept.save.assert_called_once()

    async def test_create_department_with_parent(self):
        """Test creating child department."""
        mock_parent = MagicMock()
        mock_parent.id = 1
        mock_parent.level = 1

        with patch("oa_vibe_api.services.department.Department") as MockDept:
            MockDept.filter.return_value.first = AsyncMock(return_value=mock_parent)

            mock_dept = MagicMock()
            mock_dept.id = 2
            mock_dept.name = "Backend"
            mock_dept.parent_id = 1
            mock_dept.level = 2
            mock_dept.save = AsyncMock()
            MockDept.return_value = mock_dept

            result = await department_service.create_department(name="Backend", parent_id=1)

            assert result.name == "Backend"
            assert result.level == 2

    async def test_get_department_tree(self):
        """Test getting department tree."""
        mock_depts = [
            MagicMock(id=1, name="Root", parent_id=None, level=1, sort=0),
            MagicMock(id=2, name="Child", parent_id=1, level=2, sort=0),
        ]

        with patch("oa_vibe_api.services.department.Department") as MockDept:
            MockDept.filter.return_value.order_by = MagicMock(return_value=mock_depts)

            result = await department_service.get_department_tree()

            assert len(result) == 1
            assert result[0]["name"] == "Root"
            assert len(result[0]["children"]) == 1
            assert result[0]["children"][0]["name"] == "Child"


class TestLeaveRequestService:
    """Test LeaveRequestService."""

    async def test_create_leave_request(self):
        """Test creating a leave request."""
        with patch("oa_vibe_api.services.leave_request.LeaveRequest") as MockLR:
            mock_lr = MagicMock()
            mock_lr.id = 1
            mock_lr.user_id = 1
            mock_lr.leave_type = "annual"
            mock_lr.status = "draft"
            mock_lr.save = AsyncMock()
            MockLR.return_value = mock_lr

            result = await leave_request_service.create_leave_request(
                user_id=1,
                leave_type="annual",
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=1),
                reason="Vacation",
            )

            assert result.leave_type == "annual"
            assert result.status == "draft"
            mock_lr.save.assert_called_once()

    async def test_submit_for_approval(self):
        """Test submitting leave request for approval."""
        mock_lr = MagicMock()
        mock_lr.id = 1
        mock_lr.status = "draft"
        mock_lr.save = AsyncMock()

        with patch("oa_vibe_api.services.leave_request.LeaveRequest") as MockLRClass:
            MockLRClass.filter.return_value.first = AsyncMock(return_value=mock_lr)

            result = await leave_request_service.submit_for_approval(1)

            assert result.status == "pending"
            mock_lr.save.assert_called_once()

    async def test_submit_for_approval_not_draft(self):
        """Test submitting non-draft leave request."""
        with patch("oa_vibe_api.services.leave_request.LeaveRequest") as MockLRClass:
            MockLRClass.filter.return_value.first = AsyncMock(return_value=None)

            result = await leave_request_service.submit_for_approval(1)

            assert result is None

    async def test_approve_leave_request(self):
        """Test approving a leave request."""
        mock_lr = MagicMock()
        mock_lr.id = 1
        mock_lr.status = "pending"
        mock_lr.save = AsyncMock()

        with patch("oa_vibe_api.services.leave_request.LeaveRequest") as MockLRClass:
            MockLRClass.filter.return_value.first = AsyncMock(return_value=mock_lr)

            result = await leave_request_service.approve(1, approver_id=2, comment="Approved")

            assert result.status == "approved"
            assert result.approver_id == 2
            assert result.approved_comment == "Approved"
            mock_lr.save.assert_called_once()

    async def test_reject_leave_request(self):
        """Test rejecting a leave request."""
        mock_lr = MagicMock()
        mock_lr.id = 1
        mock_lr.status = "pending"
        mock_lr.save = AsyncMock()

        with patch("oa_vibe_api.services.leave_request.LeaveRequest") as MockLRClass:
            MockLRClass.filter.return_value.first = AsyncMock(return_value=mock_lr)

            result = await leave_request_service.reject(1, approver_id=2, comment="Rejected")

            assert result.status == "rejected"
            assert result.approver_id == 2
            mock_lr.save.assert_called_once()

    async def test_cancel_leave_request_draft(self):
        """Test cancelling a draft leave request."""
        mock_lr = MagicMock()
        mock_lr.id = 1
        mock_lr.status = "draft"
        mock_lr.save = AsyncMock()

        with patch("oa_vibe_api.services.leave_request.LeaveRequest") as MockLRClass:
            MockLRClass.filter.return_value.first = AsyncMock(return_value=mock_lr)

            result = await leave_request_service.cancel(1)

            assert result.status == "cancelled"
            mock_lr.save.assert_called_once()

    async def test_cancel_leave_request_pending(self):
        """Test cancelling a pending leave request."""
        mock_lr = MagicMock()
        mock_lr.id = 1
        mock_lr.status = "pending"
        mock_lr.save = AsyncMock()

        with patch("oa_vibe_api.services.leave_request.LeaveRequest") as MockLRClass:
            MockLRClass.filter.return_value.first = AsyncMock(return_value=mock_lr)

            result = await leave_request_service.cancel(1)

            assert result.status == "cancelled"
