"""Tests for user profile use cases."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.application.use_cases.user_use_cases.update_user_use_case import (
    UpdateUserProfileUseCase,
    ChangePasswordUseCase
)
from src.domain.entities.user import User
from src.domain.exceptions.user import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidProfileDataError,
    PasswordChangeError,
    CurrentPasswordMismatchError
)


class TestUpdateUserProfileUseCase:
    """Test cases for UpdateUserProfileUseCase."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock user repository."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_repository):
        """Create UpdateUserProfileUseCase instance."""
        return UpdateUserProfileUseCase(mock_repository)

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

    @pytest.mark.asyncio
    async def test_update_profile_success_email_only(self, use_case, mock_repository, sample_user):
        """Test successful profile update with email only."""
        # Arrange
        new_email = "newemail@example.com"
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.find_by_email.return_value = None  # No existing user with new email
        mock_repository.update.return_value = sample_user

        # Act
        result = await use_case.execute(user_id="user123", email=new_email)

        # Assert
        assert result == sample_user
        mock_repository.find_by_id.assert_called_once_with("user123")
        mock_repository.find_by_email.assert_called_once_with(new_email)
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_profile_success_username_only(self, use_case, mock_repository, sample_user):
        """Test successful profile update with username only."""
        # Arrange
        new_username = "newusername"
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.find_by_username.return_value = None  # No existing user with new username
        mock_repository.update.return_value = sample_user

        # Act
        result = await use_case.execute(user_id="user123", username=new_username)

        # Assert
        assert result == sample_user
        mock_repository.find_by_id.assert_called_once_with("user123")
        mock_repository.find_by_username.assert_called_once_with(new_username)
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_profile_success_both_fields(self, use_case, mock_repository, sample_user):
        """Test successful profile update with both email and username."""
        # Arrange
        new_email = "newemail@example.com"
        new_username = "newusername"
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.find_by_email.return_value = None
        mock_repository.find_by_username.return_value = None
        mock_repository.update.return_value = sample_user

        # Act
        result = await use_case.execute(user_id="user123", email=new_email, username=new_username)

        # Assert
        assert result == sample_user
        mock_repository.find_by_id.assert_called_once_with("user123")
        mock_repository.find_by_email.assert_called_once_with(new_email)
        mock_repository.find_by_username.assert_called_once_with(new_username)
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_profile_user_not_found(self, use_case, mock_repository):
        """Test profile update when user doesn't exist."""
        # Arrange
        mock_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await use_case.execute(user_id="nonexistent", email="new@example.com")

    @pytest.mark.asyncio
    async def test_update_profile_email_already_exists(self, use_case, mock_repository, sample_user):
        """Test profile update when email already exists."""
        # Arrange
        existing_user = User(id="other123", email="existing@example.com", username="other")
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.find_by_email.return_value = existing_user

        # Act & Assert
        with pytest.raises(UserAlreadyExistsError, match="User with this email already exists"):
            await use_case.execute(user_id="user123", email="existing@example.com")

    @pytest.mark.asyncio
    async def test_update_profile_username_already_exists(self, use_case, mock_repository, sample_user):
        """Test profile update when username already exists."""
        # Arrange
        existing_user = User(id="other123", email="other@example.com", username="existing")
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.find_by_username.return_value = existing_user

        # Act & Assert
        with pytest.raises(UserAlreadyExistsError, match="User with this username already exists"):
            await use_case.execute(user_id="user123", username="existing")

    @pytest.mark.asyncio
    async def test_update_profile_invalid_email(self, use_case, mock_repository, sample_user):
        """Test profile update with invalid email format."""
        # Arrange
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.find_by_email.return_value = None  # No existing user with this email

        # Act & Assert
        with pytest.raises(InvalidProfileDataError):
            await use_case.execute(user_id="user123", email="invalid-email")

    @pytest.mark.asyncio
    async def test_update_profile_empty_username(self, use_case, mock_repository, sample_user):
        """Test profile update with empty username."""
        # Arrange
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.find_by_username.return_value = None  # No existing user with this username

        # Act & Assert
        with pytest.raises(InvalidProfileDataError):
            await use_case.execute(user_id="user123", username="")

    @pytest.mark.asyncio
    async def test_update_profile_same_email_no_conflict(self, use_case, mock_repository, sample_user):
        """Test profile update with same email (no conflict)."""
        # Arrange
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.update.return_value = sample_user

        # Act
        result = await use_case.execute(user_id="user123", email=sample_user.email)

        # Assert
        assert result == sample_user
        mock_repository.find_by_id.assert_called_once_with("user123")
        # Should not check for email conflict since it's the same email
        mock_repository.find_by_email.assert_not_called()
        mock_repository.update.assert_called_once()


class TestChangePasswordUseCase:
    """Test cases for ChangePasswordUseCase."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock user repository."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_repository):
        """Create ChangePasswordUseCase instance."""
        return ChangePasswordUseCase(mock_repository)

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(
            id="user123",
            email="test@example.com",
            username="testuser",
            hashed_password="$2b$12$hashedpassword",  # Mock hashed password
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @pytest.mark.asyncio
    async def test_change_password_success(self, use_case, mock_repository, sample_user):
        """Test successful password change."""
        # Arrange
        current_password = "currentpass123"
        new_password = "newpass123"
        mock_repository.find_by_id.return_value = sample_user
        mock_repository.update.return_value = sample_user
        mock_repository.update_password.return_value = sample_user

        # Mock the verify_password function to return True
        with pytest.MonkeyPatch().context() as m:
            m.setattr("src.application.use_cases.user_use_cases.update_user_use_case.verify_password", 
                     lambda pwd, hashed: pwd == current_password)
            m.setattr("src.application.use_cases.user_use_cases.update_user_use_case.get_password_hash", 
                     lambda pwd: f"hashed_{pwd}")

            # Act
            result = await use_case.execute(
                user_id="user123",
                current_password=current_password,
                new_password=new_password
            )

        # Assert
        assert result is True
        mock_repository.find_by_id.assert_called_once_with("user123")
        mock_repository.update_password.assert_called_once_with("user123", "hashed_newpass123")

    @pytest.mark.asyncio
    async def test_change_password_user_not_found(self, use_case, mock_repository):
        """Test password change when user doesn't exist."""
        # Arrange
        mock_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await use_case.execute(
                user_id="nonexistent",
                current_password="currentpass",
                new_password="newpass"
            )

    @pytest.mark.asyncio
    async def test_change_password_incorrect_current_password(self, use_case, mock_repository, sample_user):
        """Test password change with incorrect current password."""
        # Arrange
        mock_repository.find_by_id.return_value = sample_user

        # Mock the verify_password function to return False
        with pytest.MonkeyPatch().context() as m:
            m.setattr("src.application.use_cases.user_use_cases.update_user_use_case.verify_password", 
                     lambda pwd, hashed: False)

            # Act & Assert
            with pytest.raises(CurrentPasswordMismatchError, match="Current password is incorrect"):
                await use_case.execute(
                    user_id="user123",
                    current_password="wrongpassword",
                    new_password="newpass123"
                )

    @pytest.mark.asyncio
    async def test_change_password_too_short(self, use_case, mock_repository, sample_user):
        """Test password change with password too short."""
        # Arrange
        current_password = "currentpass123"
        new_password = "123"  # Too short
        mock_repository.find_by_id.return_value = sample_user

        # Mock the verify_password function to return True
        with pytest.MonkeyPatch().context() as m:
            m.setattr("src.application.use_cases.user_use_cases.update_user_use_case.verify_password", 
                     lambda pwd, hashed: pwd == current_password)

            # Act & Assert
            with pytest.raises(PasswordChangeError, match="New password must be at least 6 characters long"):
                await use_case.execute(
                    user_id="user123",
                    current_password=current_password,
                    new_password=new_password
                )

    @pytest.mark.asyncio
    async def test_change_password_empty_new_password(self, use_case, mock_repository, sample_user):
        """Test password change with empty new password."""
        # Arrange
        current_password = "currentpass123"
        new_password = ""
        mock_repository.find_by_id.return_value = sample_user

        # Mock the verify_password function to return True
        with pytest.MonkeyPatch().context() as m:
            m.setattr("src.application.use_cases.user_use_cases.update_user_use_case.verify_password", 
                     lambda pwd, hashed: pwd == current_password)

            # Act & Assert
            with pytest.raises(PasswordChangeError, match="New password must be at least 6 characters long"):
                await use_case.execute(
                    user_id="user123",
                    current_password=current_password,
                    new_password=new_password
                )
