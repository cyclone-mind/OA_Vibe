"""Integration tests for API endpoints."""
from datetime import date, timedelta

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from oa_vibe_api.core.security import hash_password, create_access_token
from oa_vibe_api.db.models import User


async def create_test_user(username: str = "testuser") -> User:
    """Helper to create a test user."""
    password_hash = hash_password("testpassword")
    user = User(
        username=username,
        password_hash=password_hash,
        real_name="Test User",
        status=1,
    )
    await user.save()
    return user


class TestAuthEndpoints:
    """Test authentication API endpoints."""

    async def test_login_success(self, client: AsyncClient):
        """Test successful login."""
        password_hash = hash_password("testpassword")
        user = User(
            username="testuser",
            password_hash=password_hash,
            real_name="Test User",
            status=1,
        )
        await user.save()

        response = await client.post(
            "/api/system/auth/login",
            json={"username": "testuser", "password": "testpassword"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

        await user.delete()

    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        response = await client.post(
            "/api/system/auth/login",
            json={"username": "nonexistent", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"

    async def test_logout(self, client: AsyncClient):
        """Test logout endpoint."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        response = await client.post(
            "/api/system/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

        await user.delete()

    async def test_refresh_token(self, client: AsyncClient):
        """Test token refresh."""
        user = await create_test_user()

        login_response = await client.post(
            "/api/system/auth/login",
            json={"username": "testuser", "password": "testpassword"},
        )
        tokens = login_response.json()

        refresh_response = await client.post(
            "/api/system/auth/refresh",
            json={"refresh_token": tokens["refresh_token"]},
        )

        assert refresh_response.status_code == 200
        new_tokens = refresh_response.json()
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens

        await user.delete()


class TestDepartmentEndpoints:
    """Test department API endpoints."""

    async def test_create_department(self, client: AsyncClient):
        """Test creating a department."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        response = await client.post(
            "/api/system/departments",
            json={"name": "Engineering"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Engineering"
        assert data["level"] == 1

        await user.delete()

    async def test_list_departments(self, client: AsyncClient):
        """Test listing departments."""
        from oa_vibe_api.db.models import Department

        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        dept = Department(name="Engineering", level=1, status=1)
        await dept.save()

        response = await client.get(
            "/api/system/departments",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(d["name"] == "Engineering" for d in data)

        await dept.delete()
        await user.delete()

    async def test_get_department_tree(self, client: AsyncClient):
        """Test getting department tree."""
        from oa_vibe_api.db.models import Department

        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        parent = Department(name="Engineering", level=1, status=1)
        await parent.save()

        child = Department(name="Backend", parent_id=parent.id, level=2, status=1)
        await child.save()

        response = await client.get(
            "/api/system/departments/tree",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

        await child.delete()
        await parent.delete()
        await user.delete()

    async def test_unauthorized_access(self, client: AsyncClient):
        """Test accessing protected endpoint without token."""
        response = await client.get("/api/system/departments")

        assert response.status_code == 401


class TestLeaveRequestEndpoints:
    """Test leave request API endpoints."""

    async def test_create_leave_request(self, client: AsyncClient):
        """Test creating a leave request."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        start_date = date.today()
        end_date = date.today() + timedelta(days=1)

        response = await client.post(
            "/api/oa/leave-requests",
            json={
                "leave_type": "annual",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "reason": "Vacation",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["leave_type"] == "annual"
        assert data["status"] == "draft"
        assert data["user_id"] == user.id

        await user.delete()

    async def test_create_leave_request_invalid_dates(self, client: AsyncClient):
        """Test creating leave request with invalid dates."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        start_date = date.today() + timedelta(days=2)
        end_date = date.today()

        response = await client.post(
            "/api/oa/leave-requests",
            json={
                "leave_type": "annual",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "reason": "Vacation",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert "End date must be after start date" in response.json()["detail"]

        await user.delete()

    async def test_leave_request_workflow(self, client: AsyncClient):
        """Test complete leave request workflow."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        start_date = date.today()
        end_date = date.today() + timedelta(days=1)

        create_response = await client.post(
            "/api/oa/leave-requests",
            json={
                "leave_type": "annual",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "reason": "Vacation",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert create_response.status_code == 201
        leave_id = create_response.json()["id"]

        submit_response = await client.post(
            f"/api/oa/leave-requests/{leave_id}/submit",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert submit_response.status_code == 200
        assert submit_response.json()["status"] == "pending"

        approve_response = await client.post(
            f"/api/oa/leave-requests/{leave_id}/approve",
            json={"comment": "Approved"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert approve_response.status_code == 200
        assert approve_response.json()["status"] == "approved"

        await user.delete()

    async def test_reject_leave_request(self, client: AsyncClient):
        """Test rejecting a leave request."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        start_date = date.today()
        end_date = date.today() + timedelta(days=1)

        create_response = await client.post(
            "/api/oa/leave-requests",
            json={
                "leave_type": "annual",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "reason": "Vacation",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        leave_id = create_response.json()["id"]

        await client.post(
            f"/api/oa/leave-requests/{leave_id}/submit",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        reject_response = await client.post(
            f"/api/oa/leave-requests/{leave_id}/reject",
            json={"comment": "Not enough leave balance"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert reject_response.status_code == 200
        assert reject_response.json()["status"] == "rejected"

        await user.delete()

    async def test_cancel_leave_request(self, client: AsyncClient):
        """Test cancelling a leave request."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        start_date = date.today()
        end_date = date.today() + timedelta(days=1)

        create_response = await client.post(
            "/api/oa/leave-requests",
            json={
                "leave_type": "annual",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "reason": "Vacation",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        leave_id = create_response.json()["id"]

        cancel_response = await client.post(
            f"/api/oa/leave-requests/{leave_id}/cancel",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert cancel_response.status_code == 200
        assert cancel_response.json()["status"] == "cancelled"

        await user.delete()


class TestUserEndpoints:
    """Test user API endpoints."""

    async def test_get_current_user(self, client: AsyncClient):
        """Test getting current user info."""
        user = await create_test_user()
        access_token = create_access_token({"sub": str(user.id), "username": user.username})

        response = await client.get(
            "/api/system/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user.username
        assert data["real_name"] == "Test User"

        await user.delete()

    async def test_list_users(self, client: AsyncClient):
        """Test listing users."""
        admin_user = await create_test_user(username="admin")
        access_token = create_access_token({"sub": str(admin_user.id), "username": admin_user.username})

        response = await client.get(
            "/api/system/users",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        await admin_user.delete()
