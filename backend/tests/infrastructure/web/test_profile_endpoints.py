"""Tests for profile endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.main import app
from src.domain.entities.user import User
from datetime import datetime

client = TestClient(app)


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        id="user123",
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def auth_headers():
    """Mock authentication headers."""
    return {"Authorization": "Bearer mock_token"}


class TestUpdateProfileEndpoint:
    """Tests for PUT /users/me endpoint."""

    @patch('src.infrastructure.web.dependencies.get_current_active_user')
    @patch('src.infrastructure.web.dependencies.get_update_user_use_case')
    async def test_update_profile_success(self, mock_use_case, mock_current_user, sample_user, auth_headers):
        """Test successful profile update."""
        # Arrange
        mock_current_user.return_value = {"id": "user123", "email": "test@example.com", "username": "testuser", "is_active": True}
        mock_use_case_instance = AsyncMock()
        mock_use_case.return_value = mock_use_case_instance
        
        updated_user = User(
            id="user123",
            email="newemail@example.com",
            username="newusername",
            hashed_password="hashed_password",
            is_active=True,
            created_at=sample_user.created_at,
            updated_at=datetime.utcnow()
        )
        mock_use_case_instance.execute.return_value = updated_user

        update_data = {
            "username": "newusername",
            "email": "newemail@example.com"
        }

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "newemail@example.com"
        mock_use_case_instance.execute.assert_called_once_with(
            user_id="user123",
            username="newusername",
            email="newemail@example.com"
        )

    @patch('src.infrastructure.web.dependencies.get_current_active_user')
    @patch('src.infrastructure.web.dependencies.get_update_user_use_case')
    async def test_update_profile_user_not_found(self, mock_use_case, mock_current_user, auth_headers):
        """Test profile update when user not found."""
        # Arrange
        mock_current_user.return_value = {"id": "user123", "email": "test@example.com", "username": "testuser", "is_active": True}
        mock_use_case_instance = AsyncMock()
        mock_use_case.return_value = mock_use_case_instance
        mock_use_case_instance.execute.side_effect = Exception("User not found")

        update_data = {"username": "newusername"}

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == 500

    @patch('src.infrastructure.web.dependencies.get_current_active_user')
    async def test_update_profile_unauthorized(self, mock_current_user):
        """Test profile update without authentication."""
        # Arrange
        mock_current_user.side_effect = Exception("Unauthorized")

        update_data = {"username": "newusername"}

        # Act
        response = client.put("/api/v1/users/me", json=update_data)

        # Assert
        assert response.status_code == 401


class TestChangePasswordEndpoint:
    """Tests for PUT /users/me/password endpoint."""

    @patch('src.infrastructure.web.dependencies.get_current_active_user')
    @patch('src.infrastructure.web.dependencies.get_change_password_use_case')
    async def test_change_password_success(self, mock_use_case, mock_current_user, auth_headers):
        """Test successful password change."""
        # Arrange
        mock_current_user.return_value = {"id": "user123", "email": "test@example.com", "username": "testuser", "is_active": True}
        mock_use_case_instance = AsyncMock()
        mock_use_case.return_value = mock_use_case_instance
        mock_use_case_instance.execute.return_value = None

        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Password changed successfully"
        mock_use_case_instance.execute.assert_called_once_with(
            user_id="user123",
            current_password="oldpassword",
            new_password="newpassword123"
        )

    @patch('src.infrastructure.web.dependencies.get_current_active_user')
    @patch('src.infrastructure.web.dependencies.get_change_password_use_case')
    async def test_change_password_mismatch(self, mock_use_case, mock_current_user, auth_headers):
        """Test password change with mismatched passwords."""
        # Arrange
        mock_current_user.return_value = {"id": "user123", "email": "test@example.com", "username": "testuser", "is_active": True}

        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "differentpassword"
        }

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "do not match" in data["detail"]

    @patch('src.infrastructure.web.dependencies.get_current_active_user')
    @patch('src.infrastructure.web.dependencies.get_change_password_use_case')
    async def test_change_password_invalid_current(self, mock_use_case, mock_current_user, auth_headers):
        """Test password change with invalid current password."""
        # Arrange
        mock_current_user.return_value = {"id": "user123", "email": "test@example.com", "username": "testuser", "is_active": True}
        mock_use_case_instance = AsyncMock()
        mock_use_case.return_value = mock_use_case_instance
        mock_use_case_instance.execute.side_effect = Exception("Invalid credentials")

        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == 500

    @patch('src.infrastructure.web.dependencies.get_current_active_user')
    async def test_change_password_unauthorized(self, mock_current_user):
        """Test password change without authentication."""
        # Arrange
        mock_current_user.side_effect = Exception("Unauthorized")

        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == 401
