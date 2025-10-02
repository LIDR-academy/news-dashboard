"""Tests for user profile routes."""

import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime

from src.domain.entities.user import User
from src.domain.exceptions.user import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidProfileDataError,
    PasswordChangeError,
    CurrentPasswordMismatchError
)


@pytest.fixture
def test_app():
    """Create FastAPI test application."""
    from fastapi import FastAPI
    from src.infrastructure.web.routers.users import router
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    return app


@pytest.fixture 
def client(test_app):
    """Create test client."""
    return TestClient(test_app)


class TestUserProfileRoutes:
    """Test cases for user profile routes."""

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(
            id="user123",
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @pytest.fixture
    def current_user_dict(self):
        """Create current user dict for testing."""
        return {
            "id": "user123",
            "email": "test@example.com",
            "username": "testuser",
            "is_active": True
        }

    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers for testing."""
        return {"Authorization": "Bearer valid_token"}

    def test_update_profile_success(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test successful profile update."""
        # Arrange
        update_data = {
            "email": "newemail@example.com",
            "username": "newusername"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_profile_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = sample_user
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_update_profile_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == "user123"
        assert response_data["email"] == "test@example.com"
        assert response_data["username"] == "testuser"

    def test_update_profile_email_only(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test profile update with email only."""
        # Arrange
        update_data = {"email": "newemail@example.com"}

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_profile_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = sample_user
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_update_profile_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["email"] == "test@example.com"

    def test_update_profile_username_only(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test profile update with username only."""
        # Arrange
        update_data = {"username": "newusername"}

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_profile_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = sample_user
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_update_profile_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["username"] == "testuser"

    def test_update_profile_no_data(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test profile update with no data provided."""
        # Arrange
        update_data = {}

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "No profile data provided for update" in response.json()["detail"]

    def test_update_profile_user_not_found(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test profile update when user not found."""
        # Arrange
        update_data = {"email": "newemail@example.com"}

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_profile_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = UserNotFoundError("user123")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_update_profile_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]

    def test_update_profile_email_already_exists(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test profile update when email already exists."""
        # Arrange
        update_data = {"email": "existing@example.com"}

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_profile_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = UserAlreadyExistsError("User with this email already exists")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_update_profile_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "User with this email already exists" in response.json()["detail"]

    def test_update_profile_invalid_data(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test profile update with invalid data."""
        # Arrange
        update_data = {"email": "invalid-email"}

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_profile_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = InvalidProfileDataError("Invalid email format")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_update_profile_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_profile_unauthorized(self, test_app, client: TestClient):
        """Test profile update without authentication."""
        # Arrange
        update_data = {"email": "newemail@example.com"}

        # Act
        response = client.put("/api/v1/users/me", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_success(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test successful password change."""
        # Arrange
        password_data = {
            "current_password": "currentpass123",
            "new_password": "newpass123"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = True
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["message"] == "Password changed successfully"
        assert response_data["success"] is True

    def test_change_password_incorrect_current(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test password change with incorrect current password."""
        # Arrange
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpass123"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = CurrentPasswordMismatchError("Current password is incorrect")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Current password is incorrect" in response.json()["detail"]

    def test_change_password_too_short(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test password change with password too short."""
        # Arrange
        password_data = {
            "current_password": "currentpass123",
            "new_password": "123"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = PasswordChangeError("New password must be at least 6 characters long")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_change_password_user_not_found(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test password change when user not found."""
        # Arrange
        password_data = {
            "current_password": "currentpass123",
            "new_password": "newpass123"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = UserNotFoundError("user123")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]

    def test_change_password_unauthorized(self, test_app, client: TestClient):
        """Test password change without authentication."""
        # Arrange
        password_data = {
            "current_password": "currentpass123",
            "new_password": "newpass123"
        }

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_validation_error(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test password change with validation error."""
        # Arrange
        password_data = {
            "current_password": "",  # Empty current password
            "new_password": "newpass123"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_change_password_failure(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test password change when use case returns False."""
        # Arrange
        password_data = {
            "current_password": "currentpass123",
            "new_password": "newpass123"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = False
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to change password" in response.json()["detail"]

    def test_update_profile_internal_error(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test profile update with internal server error."""
        # Arrange
        update_data = {"email": "newemail@example.com"}

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_update_profile_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = Exception("Database connection failed")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_update_profile_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to update profile" in response.json()["detail"]

    def test_change_password_internal_error(self, test_app, client: TestClient, sample_user, current_user_dict, auth_headers):
        """Test password change with internal server error."""
        # Arrange
        password_data = {
            "current_password": "currentpass123",
            "new_password": "newpass123"
        }

        # Mock dependencies
        from src.infrastructure.web.dependencies import get_current_active_user, get_change_password_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = Exception("Database connection failed")
        
        # Override dependencies
        test_app.dependency_overrides[get_current_active_user] = lambda: current_user_dict
        test_app.dependency_overrides[get_change_password_use_case] = lambda: mock_use_case

        # Act
        response = client.put("/api/v1/users/me/password", json=password_data, headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to change password" in response.json()["detail"]
