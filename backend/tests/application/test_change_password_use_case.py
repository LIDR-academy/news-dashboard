"""Tests for ChangePasswordUseCase."""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.application.use_cases.user_use_cases.change_password_use_case import ChangePasswordUseCase
from src.domain.entities.user import User
from src.domain.exceptions.user import UserNotFoundError, InvalidCredentialsError
from datetime import datetime


@pytest.fixture
def mock_user_repository():
    """Mock user repository."""
    return AsyncMock()


@pytest.fixture
def change_password_use_case(mock_user_repository):
    """ChangePasswordUseCase instance with mocked repository."""
    return ChangePasswordUseCase(mock_user_repository)


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        id="user123",
        email="test@example.com",
        username="testuser",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK",  # hashed "password123"
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.mark.asyncio
@patch('src.application.use_cases.user_use_cases.change_password_use_case.verify_password')
@patch('src.application.use_cases.user_use_cases.change_password_use_case.get_password_hash')
async def test_change_password_success(mock_get_password_hash, mock_verify_password, change_password_use_case, mock_user_repository, sample_user):
    """Test successful password change."""
    # Arrange
    user_id = "user123"
    current_password = "password123"
    new_password = "newpassword456"
    hashed_new_password = "$2b$12$NewHashedPassword"
    
    # Mock the security functions
    mock_verify_password.return_value = True
    mock_get_password_hash.return_value = hashed_new_password
    
    updated_user = User(
        id=user_id,
        email=sample_user.email,
        username=sample_user.username,
        hashed_password=hashed_new_password,
        is_active=sample_user.is_active,
        created_at=sample_user.created_at,
        updated_at=datetime.utcnow()
    )
    
    mock_user_repository.get_by_id.return_value = sample_user
    mock_user_repository.update_user_password.return_value = updated_user

    # Act
    result = await change_password_use_case.execute(
        user_id=user_id,
        current_password=current_password,
        new_password=new_password
    )

    # Assert
    assert result.hashed_password == hashed_new_password
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user_password.assert_called_once_with(user_id, hashed_new_password)
    mock_verify_password.assert_called_once_with(current_password, sample_user.hashed_password)
    mock_get_password_hash.assert_called_once_with(new_password)


@pytest.mark.asyncio
async def test_change_password_user_not_found(change_password_use_case, mock_user_repository):
    """Test change password when user not found."""
    # Arrange
    user_id = "nonexistent"
    current_password = "password123"
    new_password = "newpassword456"
    
    mock_user_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(UserNotFoundError):
        await change_password_use_case.execute(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password
        )

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user_password.assert_not_called()


@pytest.mark.asyncio
async def test_change_password_invalid_current_password(change_password_use_case, mock_user_repository, sample_user):
    """Test change password with invalid current password."""
    # Arrange
    user_id = "user123"
    current_password = "wrongpassword"
    new_password = "newpassword456"
    
    mock_user_repository.get_by_id.return_value = sample_user

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await change_password_use_case.execute(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password
        )

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user_password.assert_not_called()


@pytest.mark.asyncio
async def test_change_password_empty_current_password(change_password_use_case, mock_user_repository, sample_user):
    """Test change password with empty current password."""
    # Arrange
    user_id = "user123"
    current_password = ""
    new_password = "newpassword456"
    
    mock_user_repository.get_by_id.return_value = sample_user

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await change_password_use_case.execute(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password
        )

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user_password.assert_not_called()


@pytest.mark.asyncio
async def test_change_password_empty_new_password(change_password_use_case, mock_user_repository, sample_user):
    """Test change password with empty new password."""
    # Arrange
    user_id = "user123"
    current_password = "password123"
    new_password = ""
    
    mock_user_repository.get_by_id.return_value = sample_user

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await change_password_use_case.execute(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password
        )

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user_password.assert_not_called()
