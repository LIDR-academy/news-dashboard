"""Tests for News Item domain entity."""

import pytest
from datetime import datetime

from src.domain.entities.news_item import NewsItem, NewsCategory, NewsStatus


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


@pytest.mark.domain
@pytest.mark.unit
class TestNewsItemEntity:
    """Test suite for NewsItem domain entity."""

    def test_news_item_creation_with_valid_data_succeeds(self):
        """Test that news item creation succeeds with valid data."""
        # Act
        news_item = NewsItem(
            source="TechCrunch",
            title="AI Breakthrough",
            summary="New AI technology announced",
            link="https://example.com/news",
            category=NewsCategory.RESEARCH,
            user_id="user123"
        )
        
        # Assert
        assert news_item.source == "TechCrunch"
        assert news_item.title == "AI Breakthrough"
        assert news_item.summary == "New AI technology announced"
        assert news_item.link == "https://example.com/news"
        assert news_item.category == NewsCategory.RESEARCH
        assert news_item.user_id == "user123"
        assert news_item.is_public is True  # Default value
        assert news_item.status == NewsStatus.PENDING  # Default value
        assert news_item.is_favorite is False  # Default value

    def test_news_item_creation_with_all_fields_succeeds(self, sample_news_item):
        """Test that news item creation succeeds with all fields."""
        # Assert
        assert sample_news_item.id == "507f1f77bcf86cd799439011"
        assert sample_news_item.source == "TechCrunch"
        assert sample_news_item.title == "AI Breakthrough"
        assert sample_news_item.summary == "New AI technology announced"
        assert sample_news_item.link == "https://example.com/news"
        assert sample_news_item.image_url == "https://example.com/image.jpg"
        assert sample_news_item.category == NewsCategory.RESEARCH
        assert sample_news_item.user_id == "user123"
        assert sample_news_item.is_public is True
        assert sample_news_item.status == NewsStatus.PENDING
        assert sample_news_item.is_favorite is False

    def test_news_item_creation_with_invalid_source_raises_value_error(self):
        """Test that news item creation raises ValueError with invalid source."""
        # Test cases for invalid source
        invalid_sources = ["", "   ", None]
        
        for invalid_source in invalid_sources:
            with pytest.raises(ValueError) as exc_info:
                NewsItem(
                    source=invalid_source,
                    title="AI Breakthrough",
                    summary="New AI technology announced",
                    link="https://example.com/news",
                    category=NewsCategory.RESEARCH,
                    user_id="user123"
                )
            assert "News source cannot be empty" in str(exc_info.value)

    def test_news_item_creation_with_invalid_title_raises_value_error(self):
        """Test that news item creation raises ValueError with invalid title."""
        # Test cases for invalid title
        invalid_titles = ["", "   ", None]
        
        for invalid_title in invalid_titles:
            with pytest.raises(ValueError) as exc_info:
                NewsItem(
                    source="TechCrunch",
                    title=invalid_title,
                    summary="New AI technology announced",
                    link="https://example.com/news",
                    category=NewsCategory.RESEARCH,
                    user_id="user123"
                )
            assert "News title cannot be empty" in str(exc_info.value)

    def test_news_item_creation_with_invalid_summary_raises_value_error(self):
        """Test that news item creation raises ValueError with invalid summary."""
        # Test cases for invalid summary
        invalid_summaries = ["", "   ", None]
        
        for invalid_summary in invalid_summaries:
            with pytest.raises(ValueError) as exc_info:
                NewsItem(
                    source="TechCrunch",
                    title="AI Breakthrough",
                    summary=invalid_summary,
                    link="https://example.com/news",
                    category=NewsCategory.RESEARCH,
                    user_id="user123"
                )
            assert "News summary cannot be empty" in str(exc_info.value)

    def test_news_item_creation_with_invalid_link_raises_value_error(self):
        """Test that news item creation raises ValueError with invalid link."""
        # Test cases for invalid link
        invalid_links = ["", "   ", None]
        
        for invalid_link in invalid_links:
            with pytest.raises(ValueError) as exc_info:
                NewsItem(
                    source="TechCrunch",
                    title="AI Breakthrough",
                    summary="New AI technology announced",
                    link=invalid_link,
                    category=NewsCategory.RESEARCH,
                    user_id="user123"
                )
            assert "News link cannot be empty" in str(exc_info.value)

    def test_news_item_creation_with_invalid_user_id_raises_value_error(self):
        """Test that news item creation raises ValueError with invalid user_id."""
        # Test cases for invalid user_id
        invalid_user_ids = ["", "   ", None]
        
        for invalid_user_id in invalid_user_ids:
            with pytest.raises(ValueError) as exc_info:
                NewsItem(
                    source="TechCrunch",
                    title="AI Breakthrough",
                    summary="New AI technology announced",
                    link="https://example.com/news",
                    category=NewsCategory.RESEARCH,
                    user_id=invalid_user_id
                )
            assert "User ID cannot be empty" in str(exc_info.value)

    def test_news_item_creation_with_invalid_category_raises_value_error(self):
        """Test that news item creation raises ValueError with invalid category."""
        with pytest.raises(ValueError) as exc_info:
            NewsItem(
                source="TechCrunch",
                title="AI Breakthrough",
                summary="New AI technology announced",
                link="https://example.com/news",
                category="invalid_category",
                user_id="user123"
            )
        assert "Invalid news category" in str(exc_info.value)

    def test_news_item_creation_with_invalid_status_raises_value_error(self):
        """Test that news item creation raises ValueError with invalid status."""
        with pytest.raises(ValueError) as exc_info:
            NewsItem(
                source="TechCrunch",
                title="AI Breakthrough",
                summary="New AI technology announced",
                link="https://example.com/news",
                category=NewsCategory.RESEARCH,
                user_id="user123",
                status="invalid_status"
            )
        assert "Invalid news status" in str(exc_info.value)

    def test_mark_as_reading_sets_status_to_reading(self, sample_news_item):
        """Test that mark_as_reading sets status to READING."""
        # Act
        sample_news_item.mark_as_reading()
        
        # Assert
        assert sample_news_item.status == NewsStatus.READING
        assert sample_news_item.updated_at is not None

    def test_mark_as_reading_raises_error_when_already_read(self, sample_news_item):
        """Test that mark_as_reading raises error when already read."""
        # Arrange
        sample_news_item.status = NewsStatus.READ
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            sample_news_item.mark_as_reading()
        assert "Cannot mark a read item as reading" in str(exc_info.value)

    def test_mark_as_read_sets_status_to_read(self, sample_news_item):
        """Test that mark_as_read sets status to READ."""
        # Act
        sample_news_item.mark_as_read()
        
        # Assert
        assert sample_news_item.status == NewsStatus.READ
        assert sample_news_item.updated_at is not None

    def test_mark_as_pending_sets_status_to_pending(self, sample_news_item):
        """Test that mark_as_pending sets status to PENDING."""
        # Arrange
        sample_news_item.status = NewsStatus.READ
        
        # Act
        sample_news_item.mark_as_pending()
        
        # Assert
        assert sample_news_item.status == NewsStatus.PENDING
        assert sample_news_item.updated_at is not None

    def test_toggle_favorite_toggles_favorite_status(self, sample_news_item):
        """Test that toggle_favorite toggles the favorite status."""
        # Initial state
        assert sample_news_item.is_favorite is False
        
        # Act - Toggle to True
        sample_news_item.toggle_favorite()
        
        # Assert
        assert sample_news_item.is_favorite is True
        assert sample_news_item.updated_at is not None
        
        # Act - Toggle back to False
        sample_news_item.toggle_favorite()
        
        # Assert
        assert sample_news_item.is_favorite is False

    def test_set_public_sets_public_visibility(self, sample_news_item):
        """Test that set_public sets the public visibility."""
        # Act
        sample_news_item.set_public(False)
        
        # Assert
        assert sample_news_item.is_public is False
        assert sample_news_item.updated_at is not None
        
        # Act
        sample_news_item.set_public(True)
        
        # Assert
        assert sample_news_item.is_public is True

    def test_update_category_updates_news_category(self, sample_news_item):
        """Test that update_category updates the news category."""
        # Act
        sample_news_item.update_category(NewsCategory.PRODUCT)
        
        # Assert
        assert sample_news_item.category == NewsCategory.PRODUCT
        assert sample_news_item.updated_at is not None

    def test_update_category_raises_error_with_invalid_category(self, sample_news_item):
        """Test that update_category raises error with invalid category."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            sample_news_item.update_category("invalid_category")
        assert "Invalid news category" in str(exc_info.value)

    def test_update_status_updates_news_status(self, sample_news_item):
        """Test that update_status updates the news status."""
        # Act
        sample_news_item.update_status(NewsStatus.READ)
        
        # Assert
        assert sample_news_item.status == NewsStatus.READ
        assert sample_news_item.updated_at is not None

    def test_update_status_raises_error_with_invalid_status(self, sample_news_item):
        """Test that update_status raises error with invalid status."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            sample_news_item.update_status("invalid_status")
        assert "Invalid news status" in str(exc_info.value)

    def test_can_be_accessed_by_returns_true_for_public_news(self, sample_news_item):
        """Test that can_be_accessed_by returns True for public news."""
        # Arrange
        sample_news_item.is_public = True
        
        # Act
        result = sample_news_item.can_be_accessed_by("different_user")
        
        # Assert
        assert result is True

    def test_can_be_accessed_by_returns_true_for_owner(self, sample_news_item):
        """Test that can_be_accessed_by returns True for owner."""
        # Arrange
        sample_news_item.is_public = False
        
        # Act
        result = sample_news_item.can_be_accessed_by("user123")
        
        # Assert
        assert result is True

    def test_can_be_accessed_by_returns_false_for_private_news_and_non_owner(self, sample_news_item):
        """Test that can_be_accessed_by returns False for private news and non-owner."""
        # Arrange
        sample_news_item.is_public = False
        
        # Act
        result = sample_news_item.can_be_accessed_by("different_user")
        
        # Assert
        assert result is False

    def test_news_item_handles_unicode_characters(self):
        """Test that news item handles unicode characters correctly."""
        # Act
        news_item = NewsItem(
            source="TëchCrünch",
            title="AI Brëakthröugh",
            summary="Nëw AI tëchnölögy ännoüncëd",
            link="https://example.com/news",
            category=NewsCategory.RESEARCH,
            user_id="üsër123"
        )
        
        # Assert
        assert news_item.source == "TëchCrünch"
        assert news_item.title == "AI Brëakthröugh"
        assert news_item.summary == "Nëw AI tëchnölögy ännoüncëd"
        assert news_item.user_id == "üsër123"

    def test_news_item_validation_in_post_init_called_on_creation(self):
        """Test that news item validation in __post_init__ is called on creation."""
        # This test verifies that validation is called during object creation
        with pytest.raises(ValueError):
            NewsItem(
                source="",  # Invalid source
                title="Valid Title",
                summary="Valid Summary",
                link="https://example.com/news",
                category=NewsCategory.RESEARCH,
                user_id="user123"
            )

    def test_news_item_business_methods_do_not_affect_other_fields(self, sample_news_item):
        """Test that business methods don't affect other fields."""
        # Store original values
        original_source = sample_news_item.source
        original_title = sample_news_item.title
        original_summary = sample_news_item.summary
        original_link = sample_news_item.link
        original_user_id = sample_news_item.user_id
        
        # Act - Call business methods
        sample_news_item.mark_as_reading()
        sample_news_item.toggle_favorite()
        sample_news_item.set_public(False)
        sample_news_item.update_category(NewsCategory.PRODUCT)
        
        # Assert - Other fields should remain unchanged
        assert sample_news_item.source == original_source
        assert sample_news_item.title == original_title
        assert sample_news_item.summary == original_summary
        assert sample_news_item.link == original_link
        assert sample_news_item.user_id == original_user_id

    def test_news_item_equality_comparison(self):
        """Test that news items can be compared for equality."""
        # Arrange
        news_item1 = NewsItem(
            source="TechCrunch",
            title="AI Breakthrough",
            summary="New AI technology announced",
            link="https://example.com/news",
            category=NewsCategory.RESEARCH,
            user_id="user123"
        )
        
        news_item2 = NewsItem(
            source="TechCrunch",
            title="AI Breakthrough",
            summary="New AI technology announced",
            link="https://example.com/news",
            category=NewsCategory.RESEARCH,
            user_id="user123"
        )
        
        # Assert
        assert news_item1 == news_item2

    def test_news_item_inequality_comparison(self):
        """Test that news items can be compared for inequality."""
        # Arrange
        news_item1 = NewsItem(
            source="TechCrunch",
            title="AI Breakthrough",
            summary="New AI technology announced",
            link="https://example.com/news",
            category=NewsCategory.RESEARCH,
            user_id="user123"
        )
        
        news_item2 = NewsItem(
            source="BBC News",
            title="Different Title",
            summary="Different summary",
            link="https://example.com/different",
            category=NewsCategory.GENERAL,
            user_id="user456"
        )
        
        # Assert
        assert news_item1 != news_item2

    def test_news_item_string_representation_includes_key_info(self, sample_news_item):
        """Test that news item string representation includes key information."""
        # Act
        str_repr = str(sample_news_item)
        
        # Assert
        assert "AI Breakthrough" in str_repr
        assert "TechCrunch" in str_repr

    def test_news_item_repr_representation_includes_key_info(self, sample_news_item):
        """Test that news item repr representation includes key information."""
        # Act
        repr_str = repr(sample_news_item)
        
        # Assert
        assert "NewsItem" in repr_str
        assert "AI Breakthrough" in repr_str

    def test_news_item_dataclass_field_assignment(self, sample_news_item):
        """Test that news item dataclass fields can be assigned."""
        # Act
        sample_news_item.source = "New Source"
        sample_news_item.title = "New Title"
        
        # Assert
        assert sample_news_item.source == "New Source"
        assert sample_news_item.title == "New Title"

    def test_news_item_validation_combinations(self):
        """Test various combinations of validation scenarios."""
        # Test valid combination
        valid_news = NewsItem(
            source="Valid Source",
            title="Valid Title",
            summary="Valid Summary",
            link="https://example.com/valid",
            category=NewsCategory.RESEARCH,
            user_id="valid_user"
        )
        assert valid_news.source == "Valid Source"
        
        # Test invalid combinations
        invalid_combinations = [
            ("", "Valid Title", "Valid Summary", "https://example.com/valid", NewsCategory.RESEARCH, "valid_user"),
            ("Valid Source", "", "Valid Summary", "https://example.com/valid", NewsCategory.RESEARCH, "valid_user"),
            ("Valid Source", "Valid Title", "", "https://example.com/valid", NewsCategory.RESEARCH, "valid_user"),
            ("Valid Source", "Valid Title", "Valid Summary", "", NewsCategory.RESEARCH, "valid_user"),
            ("Valid Source", "Valid Title", "Valid Summary", "https://example.com/valid", NewsCategory.RESEARCH, ""),
        ]
        
        for source, title, summary, link, category, user_id in invalid_combinations:
            with pytest.raises(ValueError):
                NewsItem(
                    source=source,
                    title=title,
                    summary=summary,
                    link=link,
                    category=category,
                    user_id=user_id
                )
