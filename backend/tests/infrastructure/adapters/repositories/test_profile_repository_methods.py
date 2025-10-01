"""Tests for new profile repository methods."""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime
from bson import ObjectId
from src.infrastructure.adapters.repositories.mongodb_user_repository import MongoDBUserRepository
from src.domain.entities.user import User


@pytest.fixture
def mock_collection():
    """Mock collection."""
    return AsyncMock()


@pytest.fixture
def mock_database(mock_collection):
    """Mock database."""
    mock_db = Mock()
    # Make the database subscriptable to return the mock collection
    mock_db.__getitem__ = Mock(return_value=mock_collection)
    return mock_db


@pytest.fixture
def user_repository(mock_database, mock_collection):
    """User repository with mocked dependencies."""
    with patch('src.infrastructure.adapters.repositories.mongodb_user_repository.get_database', return_value=mock_database):
        repository = MongoDBUserRepository()
        # Collection is already set via mock_database["users"]
        return repository


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        id="507f1f77bcf86cd799439011",
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_document():
    """Sample MongoDB document."""
    return {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": "hashed_password",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


class TestUpdateUserMethod:
    """Tests for update_user method."""

    @pytest.mark.asyncio
    async def test_update_user_success(self, user_repository, mock_collection, sample_document):
        """Test successful user update."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        user_data = {"username": "newusername", "email": "newemail@example.com"}
        
        updated_document = {
            **sample_document,
            "username": "newusername",
            "email": "newemail@example.com",
            "updated_at": datetime.utcnow()
        }
        
        mock_collection.update_one.return_value = Mock(modified_count=1)
        mock_collection.find_one.return_value = updated_document

        # Act
        result = await user_repository.update_user(user_id, user_data)

        # Assert
        assert result.username == "newusername"
        assert result.email == "newemail@example.com"
        mock_collection.update_one.assert_called_once()
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_not_found_after_update(self, user_repository, mock_collection):
        """Test update user when user not found after update."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        user_data = {"username": "newusername"}
        
        mock_collection.update_one.return_value = Mock(modified_count=1)
        mock_collection.find_one.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="not found after update"):
            await user_repository.update_user(user_id, user_data)

    @pytest.mark.asyncio
    async def test_update_user_empty_id(self, user_repository):
        """Test update user with empty user ID."""
        # Arrange
        user_id = ""
        user_data = {"username": "newusername"}

        # Act & Assert
        with pytest.raises(ValueError, match="User ID is required"):
            await user_repository.update_user(user_id, user_data)

    @pytest.mark.asyncio
    async def test_update_user_adds_timestamp(self, user_repository, mock_collection, sample_document):
        """Test that update_user adds updated_at timestamp."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        user_data = {"username": "newusername"}
        
        updated_document = {
            **sample_document,
            "username": "newusername",
            "updated_at": datetime.utcnow()
        }
        
        mock_collection.update_one.return_value = Mock(modified_count=1)
        mock_collection.find_one.return_value = updated_document

        # Act
        await user_repository.update_user(user_id, user_data)

        # Assert
        call_args = mock_collection.update_one.call_args
        update_data = call_args[0][1]["$set"]
        assert "updated_at" in update_data
        assert update_data["username"] == "newusername"


class TestUpdateUserPasswordMethod:
    """Tests for update_user_password method."""

    @pytest.mark.asyncio
    async def test_update_user_password_success(self, user_repository, mock_collection, sample_document):
        """Test successful password update."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        hashed_password = "new_hashed_password"
        
        updated_document = {
            **sample_document,
            "hashed_password": hashed_password,
            "updated_at": datetime.utcnow()
        }
        
        mock_collection.update_one.return_value = Mock(modified_count=1)
        mock_collection.find_one.return_value = updated_document

        # Act
        result = await user_repository.update_user_password(user_id, hashed_password)

        # Assert
        assert result.hashed_password == hashed_password
        mock_collection.update_one.assert_called_once()
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_password_not_found_after_update(self, user_repository, mock_collection):
        """Test password update when user not found after update."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        hashed_password = "new_hashed_password"
        
        mock_collection.update_one.return_value = Mock(modified_count=1)
        mock_collection.find_one.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="not found after password update"):
            await user_repository.update_user_password(user_id, hashed_password)

    @pytest.mark.asyncio
    async def test_update_user_password_empty_id(self, user_repository):
        """Test password update with empty user ID."""
        # Arrange
        user_id = ""
        hashed_password = "new_hashed_password"

        # Act & Assert
        with pytest.raises(ValueError, match="User ID is required"):
            await user_repository.update_user_password(user_id, hashed_password)

    @pytest.mark.asyncio
    async def test_update_user_password_adds_timestamp(self, user_repository, mock_collection, sample_document):
        """Test that update_user_password adds updated_at timestamp."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        hashed_password = "new_hashed_password"
        
        updated_document = {
            **sample_document,
            "hashed_password": hashed_password,
            "updated_at": datetime.utcnow()
        }
        
        mock_collection.update_one.return_value = Mock(modified_count=1)
        mock_collection.find_one.return_value = updated_document

        # Act
        await user_repository.update_user_password(user_id, hashed_password)

        # Assert
        call_args = mock_collection.update_one.call_args
        update_data = call_args[0][1]["$set"]
        assert "updated_at" in update_data
        assert update_data["hashed_password"] == hashed_password


class TestAliasMethods:
    """Tests for alias methods."""

    @pytest.mark.asyncio
    async def test_get_by_id_alias(self, user_repository, mock_collection, sample_document):
        """Test get_by_id alias method."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        mock_collection.find_one.return_value = sample_document

        # Act
        result = await user_repository.get_by_id(user_id)

        # Assert
        assert result is not None
        assert result.username == "testuser"
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_email_alias(self, user_repository, mock_collection, sample_document):
        """Test get_by_email alias method."""
        # Arrange
        email = "test@example.com"
        mock_collection.find_one.return_value = sample_document

        # Act
        result = await user_repository.get_by_email(email)

        # Assert
        assert result is not None
        assert result.email == "test@example.com"
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_username_alias(self, user_repository, mock_collection, sample_document):
        """Test get_by_username alias method."""
        # Arrange
        username = "testuser"
        mock_collection.find_one.return_value = sample_document

        # Act
        result = await user_repository.get_by_username(username)

        # Assert
        assert result is not None
        assert result.username == "testuser"
        mock_collection.find_one.assert_called_once()
