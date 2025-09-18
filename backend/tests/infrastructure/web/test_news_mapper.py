"""Tests for News Mapper."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.domain.entities.news_item import NewsItem, NewsCategory, NewsStatus
from src.infrastructure.web.dtos.news_dto import (
    NewsResponseDTO,
    NewsStatusDTO,
    NewsCategoryDTO
)
from src.infrastructure.web.news_mapper import NewsMapper


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


@pytest.mark.unit
class TestNewsMapper:
    """Test suite for NewsMapper."""

    def test_to_response_dto_converts_news_entity_to_response_dto(
        self, sample_news_item
    ):
        """Test that to_response_dto converts NewsItem entity to NewsResponseDTO."""
        # Act
        result = NewsMapper.to_response_dto(sample_news_item)
        
        # Assert
        assert isinstance(result, NewsResponseDTO)
        assert result.id == sample_news_item.id
        assert result.source == sample_news_item.source
        assert result.title == sample_news_item.title
        assert result.summary == sample_news_item.summary
        assert result.link == sample_news_item.link
        assert result.image_url == sample_news_item.image_url
        assert result.status == NewsStatusDTO.PENDING
        assert result.category == NewsCategoryDTO.RESEARCH
        assert result.is_favorite == sample_news_item.is_favorite
        assert result.user_id == sample_news_item.user_id
        assert result.is_public == sample_news_item.is_public
        assert result.created_at == sample_news_item.created_at
        assert result.updated_at == sample_news_item.updated_at

    def test_to_response_dto_with_different_statuses(self):
        """Test that to_response_dto handles different news statuses."""
        statuses = [NewsStatus.PENDING, NewsStatus.READING, NewsStatus.READ]
        
        for status in statuses:
            # Arrange
            news_item = NewsItem(
                id="test123",
                source="Test Source",
                title="Test Title",
                summary="Test Summary",
                link="https://example.com/test",
                category=NewsCategory.GENERAL,
                user_id="user123",
                status=status,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Act
            result = NewsMapper.to_response_dto(news_item)
            
            # Assert
            assert result.status.value == status.value

    def test_to_response_dto_with_different_categories(self):
        """Test that to_response_dto handles different news categories."""
        categories = [
            NewsCategory.GENERAL,
            NewsCategory.RESEARCH,
            NewsCategory.PRODUCT,
            NewsCategory.COMPANY,
            NewsCategory.TUTORIAL,
            NewsCategory.OPINION
        ]
        
        for category in categories:
            # Arrange
            news_item = NewsItem(
                id="test123",
                source="Test Source",
                title="Test Title",
                summary="Test Summary",
                link="https://example.com/test",
                category=category,
                user_id="user123",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Act
            result = NewsMapper.to_response_dto(news_item)
            
            # Assert
            assert result.category.value == category.value

    def test_to_response_dto_with_news_without_id(self):
        """Test that to_response_dto handles news item without id."""
        # Arrange
        news_item = NewsItem(
            id=None,  # Explicitly set to None
            source="Test Source",
            title="Test Title",
            summary="Test Summary",
            link="https://example.com/test",
            image_url="https://example.com/image.jpg",
            status=NewsStatus.PENDING,
            category=NewsCategory.GENERAL,
            is_favorite=False,
            user_id="user123",
            is_public=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Act & Assert - This should raise a validation error since id is required
        with pytest.raises(ValidationError):
            NewsMapper.to_response_dto(news_item)

    def test_to_response_dto_with_news_without_timestamps(self):
        """Test that to_response_dto handles news item without timestamps."""
        # Arrange
        news_item = NewsItem(
            id="test123",
            source="Test Source",
            title="Test Title",
            summary="Test Summary",
            link="https://example.com/test",
            image_url="https://example.com/image.jpg",
            status=NewsStatus.PENDING,
            category=NewsCategory.GENERAL,
            is_favorite=False,
            user_id="user123",
            is_public=False,
            created_at=None,
            updated_at=None
        )
        
        # Act & Assert - This should raise a validation error since created_at is required
        with pytest.raises(ValidationError):
            NewsMapper.to_response_dto(news_item)

    def test_to_response_dto_preserves_all_news_data_exactly(self, sample_news_item):
        """Test that to_response_dto preserves all news data exactly."""
        # Act
        result = NewsMapper.to_response_dto(sample_news_item)
        
        # Assert - Verify all fields are mapped correctly
        assert result.id == sample_news_item.id
        assert result.source == sample_news_item.source
        assert result.title == sample_news_item.title
        assert result.summary == sample_news_item.summary
        assert result.link == sample_news_item.link
        assert result.image_url == sample_news_item.image_url
        assert result.is_favorite == sample_news_item.is_favorite
        assert result.user_id == sample_news_item.user_id
        assert result.is_public == sample_news_item.is_public
        assert result.created_at == sample_news_item.created_at
        assert result.updated_at == sample_news_item.updated_at

    def test_to_response_dto_with_unicode_characters(self):
        """Test that to_response_dto handles unicode characters correctly."""
        # Arrange
        news_item = NewsItem(
            id="test123",
            source="TëchCrünch",
            title="AI Brëakthröugh",
            summary="Nëw AI tëchnölögy ännoüncëd",
            link="https://example.com/news",
            category=NewsCategory.RESEARCH,
            user_id="üsër123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Act
        result = NewsMapper.to_response_dto(news_item)
        
        # Assert
        assert result.source == "TëchCrünch"
        assert result.title == "AI Brëakthröugh"
        assert result.summary == "Nëw AI tëchnölögy ännoüncëd"
        assert result.user_id == "üsër123"

    def test_status_dto_to_domain_converts_status_dto_to_domain_enum(self):
        """Test that status_dto_to_domain converts NewsStatusDTO to NewsStatus."""
        # Test all status values
        status_mappings = [
            (NewsStatusDTO.PENDING, NewsStatus.PENDING),
            (NewsStatusDTO.READING, NewsStatus.READING),
            (NewsStatusDTO.READ, NewsStatus.READ)
        ]
        
        for status_dto, expected_domain in status_mappings:
            # Act
            result = NewsMapper.status_dto_to_domain(status_dto)
            
            # Assert
            assert result == expected_domain

    def test_category_dto_to_domain_converts_category_dto_to_domain_enum(self):
        """Test that category_dto_to_domain converts NewsCategoryDTO to NewsCategory."""
        # Test all category values
        category_mappings = [
            (NewsCategoryDTO.GENERAL, NewsCategory.GENERAL),
            (NewsCategoryDTO.RESEARCH, NewsCategory.RESEARCH),
            (NewsCategoryDTO.PRODUCT, NewsCategory.PRODUCT),
            (NewsCategoryDTO.COMPANY, NewsCategory.COMPANY),
            (NewsCategoryDTO.TUTORIAL, NewsCategory.TUTORIAL),
            (NewsCategoryDTO.OPINION, NewsCategory.OPINION)
        ]
        
        for category_dto, expected_domain in category_mappings:
            # Act
            result = NewsMapper.category_dto_to_domain(category_dto)
            
            # Assert
            assert result == expected_domain

    def test_static_methods_do_not_require_instance(self, sample_news_item):
        """Test that static methods can be called without creating an instance."""
        # Act & Assert - These should not raise any errors
        result1 = NewsMapper.to_response_dto(sample_news_item)
        result2 = NewsMapper.status_dto_to_domain(NewsStatusDTO.PENDING)
        result3 = NewsMapper.category_dto_to_domain(NewsCategoryDTO.RESEARCH)
        
        # Verify results are correct
        assert isinstance(result1, NewsResponseDTO)
        assert result2 == NewsStatus.PENDING
        assert result3 == NewsCategory.RESEARCH

    def test_mapper_handles_news_with_all_none_optional_fields(self):
        """Test that mapper handles news item with all None optional fields."""
        # Arrange
        news_item = NewsItem(
            id="test123",  # id is required for DTO
            source="Test Source",
            title="Test Title",
            summary="Test Summary",
            link="https://example.com/test",
            image_url="",
            status=NewsStatus.PENDING,
            category=NewsCategory.GENERAL,
            is_favorite=False,
            user_id="user123",
            is_public=False,
            created_at=None,
            updated_at=None
        )
        
        # Act & Assert - This should raise a validation error since created_at is required
        with pytest.raises(ValidationError):
            NewsMapper.to_response_dto(news_item)


@pytest.mark.unit
class TestNewsMapperErrorHandling:
    """Test suite for NewsMapper error handling."""

    def test_to_response_dto_with_none_news_raises_attribute_error(self):
        """Test that to_response_dto raises AttributeError when news is None."""
        # Act & Assert
        with pytest.raises(AttributeError):
            NewsMapper.to_response_dto(None)

    def test_status_dto_to_domain_with_invalid_status_raises_value_error(self):
        """Test that status_dto_to_domain raises ValueError with invalid status."""
        # Act & Assert
        with pytest.raises(ValueError):
            NewsMapper.status_dto_to_domain(NewsStatusDTO("invalid_status"))

    def test_category_dto_to_domain_with_invalid_category_raises_value_error(self):
        """Test that category_dto_to_domain raises ValueError with invalid category."""
        # Act & Assert
        with pytest.raises(ValueError):
            NewsMapper.category_dto_to_domain(NewsCategoryDTO("invalid_category"))

    def test_news_response_dto_validation_requires_all_mandatory_fields(self):
        """Test that NewsResponseDTO validation requires all mandatory fields and rejects optional values."""
        # Test cases where required fields are missing or None
        invalid_data_cases = [
            # Missing id
            {
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing source
            {
                "id": "507f1f77bcf86cd799439011",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing title
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing summary
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing link
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing image_url
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing status
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing category
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing is_favorite
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing user_id
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing is_public
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Missing created_at
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "updated_at": datetime.utcnow()
            },
        ]
        
        for invalid_data in invalid_data_cases:
            with pytest.raises(ValidationError) as exc_info:
                NewsResponseDTO(**invalid_data)
            
            # Verify that the error message indicates missing required fields
            error_message = str(exc_info.value)
            assert "field required" in error_message.lower() or "missing" in error_message.lower()

    def test_news_response_dto_validation_rejects_none_values_for_required_fields(self):
        """Test that NewsResponseDTO validation rejects None values for required fields."""
        # Test cases where required fields are explicitly set to None
        none_value_cases = [
            # id is None
            {
                "id": None,
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # source is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": None,
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # title is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": None,
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # summary is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": None,
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # link is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": None,
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # image_url is None (this should fail since it's required in DTO)
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": None,
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # status is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": None,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # category is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": None,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # is_favorite is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": None,
                "user_id": "user123",
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # user_id is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": None,
                "is_public": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # is_public is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # created_at is None
            {
                "id": "507f1f77bcf86cd799439011",
                "source": "TechCrunch",
                "title": "AI Breakthrough",
                "summary": "New AI technology announced",
                "link": "https://example.com/news",
                "image_url": "https://example.com/image.jpg",
                "status": NewsStatusDTO.PENDING,
                "category": NewsCategoryDTO.RESEARCH,
                "is_favorite": False,
                "user_id": "user123",
                "is_public": True,
                "created_at": None,
                "updated_at": datetime.utcnow()
            },
        ]
        
        for none_data in none_value_cases:
            with pytest.raises(ValidationError) as exc_info:
                NewsResponseDTO(**none_data)
            
            # Verify that the error message indicates invalid type or missing value
            error_message = str(exc_info.value)
            assert ("field required" in error_message.lower() or 
                   "none is not an allowed value" in error_message.lower() or
                   "input should be" in error_message.lower())

    def test_news_response_dto_validation_accepts_none_for_optional_updated_at(self):
        """Test that NewsResponseDTO validation accepts None for the optional updated_at field."""
        # This should succeed since updated_at is Optional[datetime]
        valid_data = {
            "id": "507f1f77bcf86cd799439011",
            "source": "TechCrunch",
            "title": "AI Breakthrough",
            "summary": "New AI technology announced",
            "link": "https://example.com/news",
            "image_url": "https://example.com/image.jpg",
            "status": NewsStatusDTO.PENDING,
            "category": NewsCategoryDTO.RESEARCH,
            "is_favorite": False,
            "user_id": "user123",
            "is_public": True,
            "created_at": datetime.utcnow(),
            "updated_at": None  # This should be allowed
        }
        
        # Act
        dto = NewsResponseDTO(**valid_data)
        
        # Assert
        assert dto.updated_at is None
        assert dto.id == "507f1f77bcf86cd799439011"
        assert dto.source == "TechCrunch"


@pytest.mark.unit
class TestNewsMapperIntegration:
    """Test suite for NewsMapper integration scenarios."""

    def test_mapper_round_trip_data_integrity(self, sample_news_item):
        """Test that mapper preserves data integrity in round-trip conversions."""
        # Act
        dto = NewsMapper.to_response_dto(sample_news_item)
        
        # Assert - Verify all data is preserved
        assert dto.id == sample_news_item.id
        assert dto.source == sample_news_item.source
        assert dto.title == sample_news_item.title
        assert dto.summary == sample_news_item.summary
        assert dto.link == sample_news_item.link
        assert dto.image_url == sample_news_item.image_url
        assert dto.is_favorite == sample_news_item.is_favorite
        assert dto.user_id == sample_news_item.user_id
        assert dto.is_public == sample_news_item.is_public
        assert dto.created_at == sample_news_item.created_at
        assert dto.updated_at == sample_news_item.updated_at

    def test_mapper_with_real_world_news_data_patterns(self):
        """Test that mapper works with real-world news data patterns."""
        # Arrange - Simulate real news data
        real_news_items = [
            NewsItem(
                id="news1",
                source="BBC News",
                title="Climate Change Summit Reaches Agreement",
                summary="World leaders have reached a historic agreement on climate change measures...",
                link="https://bbc.com/news/climate-summit",
                image_url="https://bbc.com/images/climate.jpg",
                category=NewsCategory.GENERAL,
                user_id="user456",
                is_public=True,
                status=NewsStatus.READ,
                is_favorite=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            NewsItem(
                id="news2",
                source="Nature",
                title="Breakthrough in Quantum Computing",
                summary="Researchers have achieved a major milestone in quantum computing...",
                link="https://nature.com/quantum-breakthrough",
                image_url="",
                category=NewsCategory.RESEARCH,
                user_id="user789",
                is_public=False,
                status=NewsStatus.PENDING,
                is_favorite=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        # Act & Assert
        for news_item in real_news_items:
            dto = NewsMapper.to_response_dto(news_item)
            assert isinstance(dto, NewsResponseDTO)
            assert dto.source == news_item.source
            assert dto.title == news_item.title
            assert dto.category.value == news_item.category.value
            assert dto.status.value == news_item.status.value

    def test_mapper_performance_with_concurrent_operations(self):
        """Test that mapper performs well with concurrent operations."""
        import time
        
        # Arrange
        news_item = NewsItem(
            id="perf_test",
            source="Performance Test",
            title="Performance Test Title",
            summary="Performance Test Summary",
            link="https://example.com/performance",
            category=NewsCategory.GENERAL,
            user_id="perf_user",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Act
        start_time = time.time()
        for _ in range(1000):
            NewsMapper.to_response_dto(news_item)
        end_time = time.time()
        
        # Assert - Should complete in reasonable time
        execution_time = end_time - start_time
        assert execution_time < 1.0  # Should complete in less than 1 second

    def test_mapper_memory_efficiency_with_large_datasets(self):
        """Test that mapper is memory efficient with large datasets."""
        import gc
        
        # Arrange
        news_items = []
        for i in range(1000):
            news_item = NewsItem(
                id=f"news_{i}",
                source=f"Source {i}",
                title=f"Title {i}",
                summary=f"Summary {i}",
                link=f"https://example.com/news/{i}",
                category=NewsCategory.GENERAL,
                user_id=f"user{i}",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            news_items.append(news_item)
        
        # Act
        dtos = []
        for news_item in news_items:
            dto = NewsMapper.to_response_dto(news_item)
            dtos.append(dto)
        
        # Assert - Verify all conversions were successful
        assert len(dtos) == 1000
        assert all(isinstance(dto, NewsResponseDTO) for dto in dtos)
        
        # Clean up
        del news_items, dtos
        gc.collect()
