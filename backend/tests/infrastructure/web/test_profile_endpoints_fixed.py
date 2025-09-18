"""Tests for profile endpoints - Fixed version."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.main import app
from src.domain.entities.user import User
from datetime import datetime


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


class TestUpdateProfileEndpoint:
    """Tests for PUT /users/me endpoint."""

    def test_update_profile_success(self, sample_user):
        """Test successful profile update."""
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_user_use_case
        
        # Arrange
        updated_user = User(
            id="user123",
            email="newemail@example.com",
            username="newusername",
            hashed_password="hashed_password",
            is_active=True,
            created_at=sample_user.created_at,
            updated_at=datetime.utcnow()
        )
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = updated_user
        
        # Override dependencies
        app.dependency_overrides[get_current_active_user] = lambda: sample_user
        app.dependency_overrides[get_update_user_use_case] = lambda: mock_use_case
        
        test_client = TestClient(app)
        
        update_data = {
            "username": "newusername",
            "email": "newemail@example.com"
        }

        # Act
        response = test_client.put("/api/v1/users/me", json=update_data)

        # Assert
        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "newemail@example.com"
        mock_use_case.execute.assert_called_once_with(
            user_id="user123",
            username="newusername",
            email="newemail@example.com"
        )
        
        # Clean up
        app.dependency_overrides.clear()

    def test_update_profile_user_not_found(self):
        """Test profile update when user not found."""
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_user_use_case
        from src.domain.exceptions.user import UserNotFoundError
        
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = UserNotFoundError("User not found")
        
        # Override dependencies
        app.dependency_overrides[get_current_active_user] = lambda: User(id="user123", email="test@example.com", username="testuser", hashed_password="hashed", is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        app.dependency_overrides[get_update_user_use_case] = lambda: mock_use_case
        
        test_client = TestClient(app)
        
        update_data = {"username": "newusername"}

        # Act
        response = test_client.put("/api/v1/users/me", json=update_data)

        # Assert
        assert response.status_code == 500
        
        # Clean up
        app.dependency_overrides.clear()

    def test_update_profile_unauthorized(self):
        """Test profile update without authentication."""
        test_client = TestClient(app)
        
        update_data = {"username": "newusername"}

        # Act
        response = test_client.put("/api/v1/users/me", json=update_data)

        # Assert
        assert response.status_code == 401


class TestChangePasswordEndpoint:
    """Tests for PUT /users/me/password endpoint."""

    def test_change_password_success(self):
        """Test successful password change."""
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        from src.domain.entities.user import User
        
        # Arrange
        updated_user = User(
            id="user123",
            email="test@example.com",
            username="testuser",
            hashed_password="new_hashed_password",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = updated_user
        
        # Override dependencies
        app.dependency_overrides[get_current_active_user] = lambda: User(id="user123", email="test@example.com", username="testuser", hashed_password="hashed", is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case
        
        test_client = TestClient(app)
        
        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = test_client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Password changed successfully"
        mock_use_case.execute.assert_called_once_with(
            user_id="user123",
            current_password="oldpassword",
            new_password="newpassword123"
        )
        
        # Clean up
        app.dependency_overrides.clear()

    def test_change_password_mismatch(self):
        """Test password change with mismatched passwords."""
        test_client = TestClient(app)
        
        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "differentpassword"
        }

        # Act
        response = test_client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "Passwords do not match" in data["detail"]

    def test_change_password_invalid_current(self):
        """Test password change with invalid current password."""
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        from src.domain.exceptions.user import InvalidCredentialsError
        
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = InvalidCredentialsError("Current password is incorrect")
        
        # Override dependencies
        app.dependency_overrides[get_current_active_user] = lambda: User(id="user123", email="test@example.com", username="testuser", hashed_password="hashed", is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case
        
        test_client = TestClient(app)
        
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = test_client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == 500
        
        # Clean up
        app.dependency_overrides.clear()

    def test_change_password_unauthorized(self):
        """Test password change without authentication."""
        test_client = TestClient(app)
        
        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = test_client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == 401
