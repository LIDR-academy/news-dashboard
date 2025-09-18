"""Tests for UpdateUserUseCase."""

import pytest
from unittest.mock import AsyncMock, Mock
from src.application.use_cases.user_use_cases.update_user_use_case import UpdateUserUseCase
from src.domain.entities.user import User
from src.domain.exceptions.user import UserNotFoundError, UserAlreadyExistsError
from datetime import datetime


@pytest.fixture
def mock_user_repository():
    """Mock user repository."""
    return AsyncMock()


@pytest.fixture
def update_user_use_case(mock_user_repository):
    """UpdateUserUseCase instance with mocked repository."""
    return UpdateUserUseCase(mock_user_repository)


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


@pytest.mark.asyncio
async def test_update_user_username_success(update_user_use_case, mock_user_repository, sample_user):
    """Test successful username update."""
    # Arrange
    user_id = "user123"
    new_username = "newusername"
    updated_user = User(
        id=user_id,
        email=sample_user.email,
        username=new_username,
        hashed_password=sample_user.hashed_password,
        is_active=sample_user.is_active,
        created_at=sample_user.created_at,
        updated_at=datetime.utcnow()
    )
    
    mock_user_repository.get_by_id.return_value = sample_user
    mock_user_repository.get_by_username.return_value = None  # No existing user with new username
    mock_user_repository.update_user.return_value = updated_user

    # Act
    result = await update_user_use_case.execute(
        user_id=user_id,
        username=new_username
    )

    # Assert
    assert result.username == new_username
    assert result.email == sample_user.email
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_username.assert_called_once_with(new_username)
    mock_user_repository.update_user.assert_called_once_with(user_id, {'username': new_username})


@pytest.mark.asyncio
async def test_update_user_email_success(update_user_use_case, mock_user_repository, sample_user):
    """Test successful email update."""
    # Arrange
    user_id = "user123"
    new_email = "newemail@example.com"
    updated_user = User(
        id=user_id,
        email=new_email,
        username=sample_user.username,
        hashed_password=sample_user.hashed_password,
        is_active=sample_user.is_active,
        created_at=sample_user.created_at,
        updated_at=datetime.utcnow()
    )
    
    mock_user_repository.get_by_id.return_value = sample_user
    mock_user_repository.get_by_email.return_value = None  # No existing user with new email
    mock_user_repository.update_user.return_value = updated_user

    # Act
    result = await update_user_use_case.execute(
        user_id=user_id,
        email=new_email
    )

    # Assert
    assert result.email == new_email
    assert result.username == sample_user.username
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_email.assert_called_once_with(new_email)
    mock_user_repository.update_user.assert_called_once_with(user_id, {'email': new_email})


@pytest.mark.asyncio
async def test_update_user_not_found(update_user_use_case, mock_user_repository):
    """Test update user when user not found."""
    # Arrange
    user_id = "nonexistent"
    mock_user_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(UserNotFoundError):
        await update_user_use_case.execute(
            user_id=user_id,
            username="newusername"
        )

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_email_already_exists(update_user_use_case, mock_user_repository, sample_user):
    """Test update user when email already exists."""
    # Arrange
    user_id = "user123"
    existing_email = "existing@example.com"
    existing_user = User(
        id="other_user",
        email=existing_email,
        username="otheruser",
        hashed_password="hashed_password",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    mock_user_repository.get_by_id.return_value = sample_user
    mock_user_repository.get_by_email.return_value = existing_user

    # Act & Assert
    with pytest.raises(UserAlreadyExistsError):
        await update_user_use_case.execute(
            user_id=user_id,
            email=existing_email
        )

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_email.assert_called_once_with(existing_email)
    mock_user_repository.update_user.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_username_already_exists(update_user_use_case, mock_user_repository, sample_user):
    """Test update user when username already exists."""
    # Arrange
    user_id = "user123"
    existing_username = "existinguser"
    existing_user = User(
        id="other_user",
        email="other@example.com",
        username=existing_username,
        hashed_password="hashed_password",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    mock_user_repository.get_by_id.return_value = sample_user
    mock_user_repository.get_by_username.return_value = existing_user

    # Act & Assert
    with pytest.raises(UserAlreadyExistsError):
        await update_user_use_case.execute(
            user_id=user_id,
            username=existing_username
        )

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_by_username.assert_called_once_with(existing_username)
    mock_user_repository.update_user.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_no_changes(update_user_use_case, mock_user_repository, sample_user):
    """Test update user with no changes."""
    # Arrange
    user_id = "user123"
    mock_user_repository.get_by_id.return_value = sample_user
    mock_user_repository.update_user.return_value = sample_user

    # Act
    result = await update_user_use_case.execute(
        user_id=user_id,
        username=sample_user.username,
        email=sample_user.email
    )

    # Assert
    assert result == sample_user
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    # Should not check for existing users if values are the same
    mock_user_repository.get_by_email.assert_not_called()
    mock_user_repository.get_by_username.assert_not_called()
    # The use case passes the values even if they're the same
    mock_user_repository.update_user.assert_called_once_with(user_id, {'username': sample_user.username, 'email': sample_user.email})
