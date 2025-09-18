"""Tests for profile DTOs."""

import pytest
from pydantic import ValidationError
from src.infrastructure.web.dto.user_dto import UserUpdate, ChangePasswordRequest


class TestUserUpdate:
    """Tests for UserUpdate DTO."""

    def test_user_update_valid_data(self):
        """Test UserUpdate with valid data."""
        # Arrange & Act
        user_update = UserUpdate(
            username="newusername",
            email="newemail@example.com",
            is_active=True
        )

        # Assert
        assert user_update.username == "newusername"
        assert user_update.email == "newemail@example.com"
        assert user_update.is_active is True

    def test_user_update_partial_data(self):
        """Test UserUpdate with partial data."""
        # Arrange & Act
        user_update = UserUpdate(username="newusername")

        # Assert
        assert user_update.username == "newusername"
        assert user_update.email is None
        assert user_update.is_active is None

    def test_user_update_empty_data(self):
        """Test UserUpdate with no data."""
        # Arrange & Act
        user_update = UserUpdate()

        # Assert
        assert user_update.username is None
        assert user_update.email is None
        assert user_update.is_active is None

    def test_user_update_invalid_email(self):
        """Test UserUpdate with invalid email."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(email="invalid-email")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "value_error"

    def test_user_update_valid_email(self):
        """Test UserUpdate with valid email."""
        # Arrange & Act
        user_update = UserUpdate(email="valid@example.com")

        # Assert
        assert user_update.email == "valid@example.com"

    def test_user_update_boolean_is_active(self):
        """Test UserUpdate with boolean is_active."""
        # Arrange & Act
        user_update_active = UserUpdate(is_active=True)
        user_update_inactive = UserUpdate(is_active=False)

        # Assert
        assert user_update_active.is_active is True
        assert user_update_inactive.is_active is False


class TestChangePasswordRequest:
    """Tests for ChangePasswordRequest DTO."""

    def test_change_password_request_valid_data(self):
        """Test ChangePasswordRequest with valid data."""
        # Arrange & Act
        password_request = ChangePasswordRequest(
            current_password="oldpassword",
            new_password="newpassword123",
            confirm_password="newpassword123"
        )

        # Assert
        assert password_request.current_password == "oldpassword"
        assert password_request.new_password == "newpassword123"
        assert password_request.confirm_password == "newpassword123"

    def test_change_password_request_empty_current_password(self):
        """Test ChangePasswordRequest with empty current password."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ChangePasswordRequest(
                current_password="",
                new_password="newpassword123",
                confirm_password="newpassword123"
            )

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("current_password",)

    def test_change_password_request_short_new_password(self):
        """Test ChangePasswordRequest with short new password."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ChangePasswordRequest(
                current_password="oldpassword",
                new_password="123",
                confirm_password="123"
            )

        errors = exc_info.value.errors()
        # Both new_password and confirm_password will have validation errors
        assert len(errors) == 2
        # Check that both fields have validation errors
        error_locs = [error["loc"] for error in errors]
        assert ("new_password",) in error_locs
        assert ("confirm_password",) in error_locs

    def test_change_password_request_empty_confirm_password(self):
        """Test ChangePasswordRequest with empty confirm password."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ChangePasswordRequest(
                current_password="oldpassword",
                new_password="newpassword123",
                confirm_password=""
            )

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("confirm_password",)

    def test_change_password_request_minimum_length_password(self):
        """Test ChangePasswordRequest with minimum length password."""
        # Arrange & Act
        password_request = ChangePasswordRequest(
            current_password="oldpass",
            new_password="123456",  # Exactly 6 characters
            confirm_password="123456"
        )

        # Assert
        assert password_request.new_password == "123456"
        assert password_request.confirm_password == "123456"

    def test_change_password_request_missing_fields(self):
        """Test ChangePasswordRequest with missing required fields."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ChangePasswordRequest(
                current_password="oldpassword"
                # Missing new_password and confirm_password
            )

        errors = exc_info.value.errors()
        assert len(errors) == 2
        error_locs = [error["loc"] for error in errors]
        assert ("new_password",) in error_locs
        assert ("confirm_password",) in error_locs

    def test_change_password_request_all_fields_required(self):
        """Test that all fields are required in ChangePasswordRequest."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ChangePasswordRequest()

        errors = exc_info.value.errors()
        assert len(errors) == 3
        error_locs = [error["loc"] for error in errors]
        assert ("current_password",) in error_locs
        assert ("new_password",) in error_locs
        assert ("confirm_password",) in error_locs
