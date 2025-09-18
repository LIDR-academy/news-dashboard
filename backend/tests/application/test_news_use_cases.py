"""Tests for News use cases."""

import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from src.domain.entities.news_item import NewsItem, NewsCategory, NewsStatus
from src.domain.exceptions.news_exceptions import (
    NewsNotFoundException,
    UnauthorizedNewsAccessException,
    DuplicateNewsException
)
from src.application.use_cases.news.create_news_use_case import CreateNewsUseCase
from src.application.use_cases.news.get_public_news_use_case import GetPublicNewsUseCase
from src.application.use_cases.news.get_user_news_use_case import GetUserNewsUseCase
from src.application.use_cases.news.toggle_favorite_use_case import ToggleFavoriteUseCase
from src.application.use_cases.news.update_news_status_use_case import UpdateNewsStatusUseCase


@pytest.fixture
def mock_news_repository():
    """Mock news repository for testing."""
    return AsyncMock()


@pytest.fixture
def sample_news_item():
    """Sample news item for testing."""
    return NewsItem(
        id="507f1f77bcf86cd799439011",
        source="TechCrunch",
        title="AI Breakthrough",
        summary="New AI technology announced",
        link="https://example.com/news",
        image_url="https://example.com/image.jpg",
        category=NewsCategory.RESEARCH,
        user_id="user123",
        is_public=True,
        status=NewsStatus.PENDING,
        is_favorite=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_news_list():
    """Sample list of news items for testing."""
    return [
        NewsItem(
            id="1",
            source="Source1",
            title="Title1",
            summary="Summary1",
            link="https://example.com/1",
            image_url="https://example.com/img1.jpg",
            category=NewsCategory.GENERAL,
            user_id="user1",
            is_public=True,
            status=NewsStatus.PENDING,
            is_favorite=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        NewsItem(
            id="2",
            source="Source2",
            title="Title2",
            summary="Summary2",
            link="https://example.com/2",
            image_url="https://example.com/img2.jpg",
            category=NewsCategory.RESEARCH,
            user_id="user2",
            is_public=False,
            status=NewsStatus.READ,
            is_favorite=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]


@pytest.mark.service
@pytest.mark.unit
class TestCreateNewsUseCase:
    """Test suite for CreateNewsUseCase."""

    async def test_execute_creates_news_successfully(
        self, mock_news_repository, sample_news_item
    ):
        """Test that execute creates news successfully."""
        # Arrange
        mock_news_repository.exists_by_link_and_user.return_value = False
        mock_news_repository.create.return_value = sample_news_item
        
        use_case = CreateNewsUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute(
            source="TechCrunch",
            title="AI Breakthrough",
            summary="New AI technology announced",
            link="https://example.com/news",
            image_url="https://example.com/image.jpg",
            category=NewsCategory.RESEARCH,
            user_id="user123",
            is_public=True
        )
        
        # Assert
        assert result == sample_news_item
        mock_news_repository.exists_by_link_and_user.assert_called_once_with(
            "https://example.com/news", "user123"
        )
        mock_news_repository.create.assert_called_once()

    async def test_execute_raises_duplicate_news_exception_when_link_exists(
        self, mock_news_repository
    ):
        """Test that execute raises DuplicateNewsException when link exists."""
        # Arrange
        mock_news_repository.exists_by_link_and_user.return_value = True
        
        use_case = CreateNewsUseCase(mock_news_repository)
        
        # Act & Assert
        with pytest.raises(DuplicateNewsException) as exc_info:
            await use_case.execute(
                source="TechCrunch",
                title="AI Breakthrough",
                summary="New AI technology announced",
                link="https://example.com/news",
                image_url="https://example.com/image.jpg",
                category=NewsCategory.RESEARCH,
                user_id="user123",
                is_public=True
            )
        
        assert "https://example.com/news" in str(exc_info.value)
        assert "user123" in str(exc_info.value)
        mock_news_repository.exists_by_link_and_user.assert_called_once_with(
            "https://example.com/news", "user123"
        )
        mock_news_repository.create.assert_not_called()

    async def test_execute_creates_news_with_default_values(
        self, mock_news_repository, sample_news_item
    ):
        """Test that execute creates news with default values."""
        # Arrange
        mock_news_repository.exists_by_link_and_user.return_value = False
        mock_news_repository.create.return_value = sample_news_item
        
        use_case = CreateNewsUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute(
            source="TechCrunch",
            title="AI Breakthrough",
            summary="New AI technology announced",
            link="https://example.com/news",
            image_url="https://example.com/image.jpg",
            category=NewsCategory.RESEARCH,
            user_id="user123",
            is_public=False  # Default value
        )
        
        # Assert
        assert result == sample_news_item
        mock_news_repository.create.assert_called_once()
        
        # Verify the created news item has correct default values
        created_news = mock_news_repository.create.call_args[0][0]
        assert created_news.status == NewsStatus.PENDING
        assert created_news.is_favorite is False
        assert created_news.is_public is False


@pytest.mark.service
@pytest.mark.unit
class TestGetPublicNewsUseCase:
    """Test suite for GetPublicNewsUseCase."""

    async def test_execute_returns_public_news_without_filters(
        self, mock_news_repository, sample_news_list
    ):
        """Test that execute returns public news without filters."""
        # Arrange
        mock_news_repository.get_public_news.return_value = sample_news_list
        use_case = GetPublicNewsUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute()
        
        # Assert
        assert result == sample_news_list
        mock_news_repository.get_public_news.assert_called_once_with(
            category=None,
            date_from=None,
            date_to=None,
            limit=100,
            offset=0
        )

    async def test_execute_returns_public_news_with_filters(
        self, mock_news_repository, sample_news_list
    ):
        """Test that execute returns public news with filters."""
        # Arrange
        mock_news_repository.get_public_news.return_value = sample_news_list
        use_case = GetPublicNewsUseCase(mock_news_repository)
        
        date_from = datetime(2024, 1, 1)
        date_to = datetime(2024, 12, 31)
        
        # Act
        result = await use_case.execute(
            category=NewsCategory.RESEARCH,
            date_from=date_from,
            date_to=date_to,
            limit=50,
            offset=10
        )
        
        # Assert
        assert result == sample_news_list
        mock_news_repository.get_public_news.assert_called_once_with(
            category=NewsCategory.RESEARCH,
            date_from=date_from,
            date_to=date_to,
            limit=50,
            offset=10
        )

    async def test_execute_returns_empty_list_when_no_public_news(
        self, mock_news_repository
    ):
        """Test that execute returns empty list when no public news."""
        # Arrange
        mock_news_repository.get_public_news.return_value = []
        use_case = GetPublicNewsUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute()
        
        # Assert
        assert result == []
        mock_news_repository.get_public_news.assert_called_once()


@pytest.mark.service
@pytest.mark.unit
class TestGetUserNewsUseCase:
    """Test suite for GetUserNewsUseCase."""

    async def test_execute_returns_combined_user_and_public_news(
        self, mock_news_repository, sample_news_list
    ):
        """Test that execute returns combined user and public news."""
        # Arrange
        user_news = [sample_news_list[0]]
        public_news = [sample_news_list[1]]
        
        mock_news_repository.get_by_user_id.return_value = user_news
        mock_news_repository.get_public_news.return_value = public_news
        
        use_case = GetUserNewsUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute(user_id="user123")
        
        # Assert
        assert len(result) == 2
        mock_news_repository.get_by_user_id.assert_called_once()
        mock_news_repository.get_public_news.assert_called_once()

    async def test_execute_filters_duplicate_links(
        self, mock_news_repository, sample_news_list
    ):
        """Test that execute filters duplicate links."""
        # Arrange
        user_news = [sample_news_list[0]]
        public_news = [sample_news_list[0]]  # Same link as user news
        
        mock_news_repository.get_by_user_id.return_value = user_news
        mock_news_repository.get_public_news.return_value = public_news
        
        use_case = GetUserNewsUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute(user_id="user123")
        
        # Assert
        assert len(result) == 1  # Duplicate filtered out
        assert result[0] == user_news[0]

    async def test_execute_applies_filters_to_both_queries(
        self, mock_news_repository, sample_news_list
    ):
        """Test that execute applies filters to both user and public queries."""
        # Arrange
        mock_news_repository.get_by_user_id.return_value = sample_news_list
        mock_news_repository.get_public_news.return_value = []
        
        use_case = GetUserNewsUseCase(mock_news_repository)
        
        date_from = datetime(2024, 1, 1)
        date_to = datetime(2024, 12, 31)
        
        # Act
        result = await use_case.execute(
            user_id="user123",
            status=NewsStatus.PENDING,
            category=NewsCategory.RESEARCH,
            is_favorite=True,
            date_from=date_from,
            date_to=date_to,
            limit=50,
            offset=10
        )
        
        # Assert
        mock_news_repository.get_by_user_id.assert_called_once_with(
            user_id="user123",
            status=NewsStatus.PENDING,
            category=NewsCategory.RESEARCH,
            is_favorite=True,
            date_from=date_from,
            date_to=date_to,
            limit=50,
            offset=10
        )
        mock_news_repository.get_public_news.assert_called_once_with(
            category=NewsCategory.RESEARCH,
            date_from=date_from,
            date_to=date_to,
            limit=50,
            offset=10
        )


@pytest.mark.service
@pytest.mark.unit
class TestToggleFavoriteUseCase:
    """Test suite for ToggleFavoriteUseCase."""

    async def test_execute_toggles_favorite_successfully(
        self, mock_news_repository, sample_news_item
    ):
        """Test that execute toggles favorite successfully."""
        # Arrange
        mock_news_repository.get_by_id.return_value = sample_news_item
        mock_news_repository.update.return_value = sample_news_item
        
        use_case = ToggleFavoriteUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute(
            news_id="507f1f77bcf86cd799439011",
            user_id="user123"
        )
        
        # Assert
        assert result == sample_news_item
        mock_news_repository.get_by_id.assert_called_once_with("507f1f77bcf86cd799439011")
        mock_news_repository.update.assert_called_once()
        
        # Verify toggle_favorite was called
        updated_news = mock_news_repository.update.call_args[0][0]
        assert updated_news.is_favorite is True  # Should be toggled

    async def test_execute_raises_news_not_found_exception(
        self, mock_news_repository
    ):
        """Test that execute raises NewsNotFoundException when news not found."""
        # Arrange
        mock_news_repository.get_by_id.return_value = None
        
        use_case = ToggleFavoriteUseCase(mock_news_repository)
        
        # Act & Assert
        with pytest.raises(NewsNotFoundException) as exc_info:
            await use_case.execute(
                news_id="nonexistent",
                user_id="user123"
            )
        
        assert "nonexistent" in str(exc_info.value)
        mock_news_repository.get_by_id.assert_called_once_with("nonexistent")
        mock_news_repository.update.assert_not_called()

    async def test_execute_raises_unauthorized_access_exception(
        self, mock_news_repository, sample_news_item
    ):
        """Test that execute raises UnauthorizedNewsAccessException for wrong user."""
        # Arrange
        mock_news_repository.get_by_id.return_value = sample_news_item
        
        use_case = ToggleFavoriteUseCase(mock_news_repository)
        
        # Act & Assert
        with pytest.raises(UnauthorizedNewsAccessException) as exc_info:
            await use_case.execute(
                news_id="507f1f77bcf86cd799439011",
                user_id="different_user"
            )
        
        assert "different_user" in str(exc_info.value)
        assert "507f1f77bcf86cd799439011" in str(exc_info.value)
        mock_news_repository.get_by_id.assert_called_once()
        mock_news_repository.update.assert_not_called()


@pytest.mark.service
@pytest.mark.unit
class TestUpdateNewsStatusUseCase:
    """Test suite for UpdateNewsStatusUseCase."""

    async def test_execute_updates_status_successfully(
        self, mock_news_repository, sample_news_item
    ):
        """Test that execute updates status successfully."""
        # Arrange
        mock_news_repository.get_by_id.return_value = sample_news_item
        mock_news_repository.update.return_value = sample_news_item
        
        use_case = UpdateNewsStatusUseCase(mock_news_repository)
        
        # Act
        result = await use_case.execute(
            news_id="507f1f77bcf86cd799439011",
            status=NewsStatus.READ,
            user_id="user123"
        )
        
        # Assert
        assert result == sample_news_item
        mock_news_repository.get_by_id.assert_called_once_with("507f1f77bcf86cd799439011")
        mock_news_repository.update.assert_called_once()
        
        # Verify update_status was called
        updated_news = mock_news_repository.update.call_args[0][0]
        assert updated_news.status == NewsStatus.READ

    async def test_execute_raises_news_not_found_exception(
        self, mock_news_repository
    ):
        """Test that execute raises NewsNotFoundException when news not found."""
        # Arrange
        mock_news_repository.get_by_id.return_value = None
        
        use_case = UpdateNewsStatusUseCase(mock_news_repository)
        
        # Act & Assert
        with pytest.raises(NewsNotFoundException) as exc_info:
            await use_case.execute(
                news_id="nonexistent",
                status=NewsStatus.READ,
                user_id="user123"
            )
        
        assert "nonexistent" in str(exc_info.value)
        mock_news_repository.get_by_id.assert_called_once_with("nonexistent")
        mock_news_repository.update.assert_not_called()

    async def test_execute_raises_unauthorized_access_exception(
        self, mock_news_repository, sample_news_item
    ):
        """Test that execute raises UnauthorizedNewsAccessException for wrong user."""
        # Arrange
        mock_news_repository.get_by_id.return_value = sample_news_item
        
        use_case = UpdateNewsStatusUseCase(mock_news_repository)
        
        # Act & Assert
        with pytest.raises(UnauthorizedNewsAccessException) as exc_info:
            await use_case.execute(
                news_id="507f1f77bcf86cd799439011",
                status=NewsStatus.READ,
                user_id="different_user"
            )
        
        assert "different_user" in str(exc_info.value)
        assert "507f1f77bcf86cd799439011" in str(exc_info.value)
        mock_news_repository.get_by_id.assert_called_once()
        mock_news_repository.update.assert_not_called()

    async def test_execute_updates_different_statuses(
        self, mock_news_repository, sample_news_item
    ):
        """Test that execute can update to different statuses."""
        # Arrange
        mock_news_repository.get_by_id.return_value = sample_news_item
        mock_news_repository.update.return_value = sample_news_item
        
        use_case = UpdateNewsStatusUseCase(mock_news_repository)
        
        # Test different status transitions
        statuses = [NewsStatus.PENDING, NewsStatus.READING, NewsStatus.READ]
        
        for status in statuses:
            # Act
            result = await use_case.execute(
                news_id="507f1f77bcf86cd799439011",
                status=status,
                user_id="user123"
            )
            
            # Assert
            assert result == sample_news_item
            updated_news = mock_news_repository.update.call_args[0][0]
            assert updated_news.status == status
