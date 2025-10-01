"""Tests for profile endpoints - Fixed version."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.infrastructure.web.routers.users import router
from src.domain.entities.user import User
from datetime import datetime


@pytest.fixture
def test_app():
    """Create FastAPI test application."""
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    yield app
    # Clean up dependency overrides after each test
    app.dependency_overrides.clear()


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


@pytest.mark.api
@pytest.mark.unit
class TestUpdateProfileEndpoint:
    """Tests for PUT /users/me endpoint."""

    def test_update_profile_success(self, test_app, sample_user):
        """Test successful profile update."""
        from src.infrastructure.web.dependencies import get_current_user, get_update_user_use_case
        
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
        test_app.dependency_overrides[get_current_user] = lambda: sample_user
        test_app.dependency_overrides[get_update_user_use_case] = lambda: mock_use_case
        
        test_client = TestClient(test_app)
        
        update_data = {
            "username": "newusername",
            "email": "newemail@example.com"
        }

        # Act
        response = test_client.put("/api/v1/users/me", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "newemail@example.com"
        mock_use_case.execute.assert_called_once_with(
            user_id="user123",
            username="newusername",
            email="newemail@example.com"
        )

    def test_update_profile_user_not_found(self, test_app, sample_user):
        """Test profile update when user not found."""
        from src.infrastructure.web.dependencies import get_current_user, get_update_user_use_case
        from src.domain.exceptions.user import UserNotFoundError
        
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = UserNotFoundError("User not found")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_user] = lambda: sample_user
        test_app.dependency_overrides[get_update_user_use_case] = lambda: mock_use_case
        
        test_client = TestClient(test_app)
        
        update_data = {"username": "newusername"}

        # Act
        response = test_client.put("/api/v1/users/me", json=update_data)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_update_profile_unauthorized(self, test_app):
        """Test profile update without authentication."""
        test_client = TestClient(test_app)
        
        update_data = {"username": "newusername"}

        # Act
        response = test_client.put("/api/v1/users/me", json=update_data)

        # Assert
        assert response.status_code == 401


@pytest.mark.api
@pytest.mark.unit
class TestChangePasswordEndpoint:
    """Tests for PUT /users/me/password endpoint."""

    def test_change_password_success(self, test_app, sample_user):
        """Test successful password change."""
        from src.infrastructure.web.dependencies import get_current_user, get_change_password_use_case
        
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
        test_app.dependency_overrides[get_current_user] = lambda: sample_user
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case
        
        test_client = TestClient(test_app)
        
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

    def test_change_password_mismatch(self, test_app, sample_user):
        """Test password change with mismatched passwords."""
        from src.infrastructure.web.dependencies import get_current_user, get_change_password_use_case
        
        # Arrange - Mock use case (shouldn't be called due to early validation)
        mock_use_case = AsyncMock()
        
        # Override dependencies to simulate authenticated user
        test_app.dependency_overrides[get_current_user] = lambda: sample_user
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case
        
        test_client = TestClient(test_app)
        
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
        assert "do not match" in data["detail"].lower()
        # Use case should not be called due to validation error
        mock_use_case.execute.assert_not_called()

    def test_change_password_invalid_current(self, test_app, sample_user):
        """Test password change with invalid current password."""
        from src.infrastructure.web.dependencies import get_current_user, get_change_password_use_case
        from src.domain.exceptions.user import InvalidCredentialsError
        
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = InvalidCredentialsError("Current password is incorrect")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_user] = lambda: sample_user
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case
        
        test_client = TestClient(test_app)
        
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = test_client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "credential" in data["detail"].lower() or "password" in data["detail"].lower()

    def test_change_password_unauthorized(self, test_app):
        """Test password change without authentication."""
        test_client = TestClient(test_app)
        
        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        # Act
        response = test_client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == 401
