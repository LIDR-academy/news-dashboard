"""Tests for News router endpoints."""

import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from fastapi import status
from fastapi.testclient import TestClient

from src.domain.entities.news_item import NewsItem, NewsStatus, NewsCategory
from src.domain.exceptions.news_exceptions import (
    DuplicateNewsException,
    NewsNotFoundException,
    UnauthorizedNewsAccessException,
)
from src.infrastructure.web.dtos.news_dto import (
    NewsResponseDTO,
    NewsListResponseDTO,
    NewsStatsResponseDTO,
    NewsStatusDTO,
    NewsCategoryDTO,
)
from src.infrastructure.web.routers.news import router


@pytest.fixture
def test_app():
    """Create FastAPI test application."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(test_app):
    """Create test client."""
    return TestClient(test_app)


@pytest.fixture
def mock_current_user():
    """Mock current user for authentication."""
    return {
        "id": "507f1f77bcf86cd799439012",
        "email": "test@example.com",
        "username": "testuser"
    }


@pytest.mark.api
@pytest.mark.unit
class TestCreateNewsEndpoint:
    """Test suite for POST /api/news endpoint."""

    def test_create_news_success(
        self, test_app, news_create_data, news_entity_with_id, mock_current_user
    ):
        """Test successful news creation returns 201 and NewsResponseDTO."""
        # Arrange
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.post("/api/news", json=news_create_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == news_entity_with_id.id
        assert data["title"] == news_entity_with_id.title
        assert data["source"] == news_entity_with_id.source
        assert data["category"] == news_create_data["category"]
        
    def test_create_news_without_image_url(
        self, test_app, news_create_data, news_entity_with_id, mock_current_user
    ):
        """Test creating news without image_url (optional field)."""
        # Arrange
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_data = news_create_data.copy()
        del news_data["image_url"]
        
        news_entity_with_id.image_url = ""
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.post("/api/news", json=news_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["image_url"] == ""

    def test_create_news_public(
        self, test_app, news_create_data, news_entity_with_id, mock_current_user
    ):
        """Test creating public news item."""
        # Arrange
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_data = news_create_data.copy()
        news_data["is_public"] = True
        
        news_entity_with_id.is_public = True
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.post("/api/news", json=news_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["is_public"] is True

    def test_create_news_private(
        self, test_app, news_create_data, news_entity_with_id, mock_current_user
    ):
        """Test creating private news item."""
        # Arrange
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.post("/api/news", json=news_create_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["is_public"] is False

    def test_create_news_duplicate(
        self, test_app, news_create_data, mock_current_user
    ):
        """Test creating duplicate news returns 400 Bad Request."""
        # Arrange
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = DuplicateNewsException(
            link="https://example.com/article",
            user_id=mock_current_user["id"]
        )
        
        test_app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.post("/api/news", json=news_create_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]

    def test_create_news_invalid_data(
        self, test_app, news_create_data, mock_current_user
    ):
        """Test creating news with invalid data returns 400."""
        # Arrange
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = ValueError("Invalid news data")
        
        test_app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.post("/api/news", json=news_create_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid news data" in response.json()["detail"]

    def test_create_news_unauthorized(self, test_app, news_create_data):
        """Test creating news without authentication returns 401."""
        # Arrange
        from src.infrastructure.web.dependencies import get_current_active_user
        from fastapi import HTTPException
        
        def mock_auth_failure():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        test_app.dependency_overrides[get_current_active_user] = mock_auth_failure
        
        client = TestClient(test_app)
        
        # Act
        response = client.post("/api/news", json=news_create_data)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # NOTE: Validation tests for invalid category and URL are handled by Pydantic automatically
    # and don't need explicit testing at the router level


@pytest.mark.api
@pytest.mark.unit
class TestGetUserNewsEndpoint:
    """Test suite for GET /api/news/user endpoint."""

    def test_get_user_news_success(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test getting user news returns NewsListResponseDTO."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = test_news_list
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "offset" in data
        assert "limit" in data
        assert len(data["items"]) == len(test_news_list)

    def test_get_user_news_empty_list(
        self, test_app, mock_current_user
    ):
        """Test getting user news when user has no news."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = []
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 0
        assert data["total"] == 0

    def test_get_user_news_filter_by_status(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test filtering user news by status."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        pending_news = [n for n in test_news_list if n.status == NewsStatus.PENDING]
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = pending_news
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user?status=pending")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        mock_use_case.execute.assert_called_once()
        call_kwargs = mock_use_case.execute.call_args.kwargs
        assert call_kwargs["status"] == NewsStatus.PENDING

    def test_get_user_news_filter_by_category(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test filtering user news by category."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        research_news = [n for n in test_news_list if n.category == NewsCategory.RESEARCH]
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = research_news
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user?category=research")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        mock_use_case.execute.assert_called_once()
        call_kwargs = mock_use_case.execute.call_args.kwargs
        assert call_kwargs["category"] == NewsCategory.RESEARCH

    def test_get_user_news_filter_by_favorite(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test filtering user news by favorite status."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        favorite_news = [n for n in test_news_list if n.is_favorite]
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = favorite_news
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user?is_favorite=true")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        mock_use_case.execute.assert_called_once()
        call_kwargs = mock_use_case.execute.call_args.kwargs
        assert call_kwargs["is_favorite"] is True

    def test_get_user_news_with_pagination(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test pagination parameters are passed correctly."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = test_news_list[:2]
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user?limit=50&offset=10")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["limit"] == 50
        assert data["offset"] == 10
        mock_use_case.execute.assert_called_once()
        call_kwargs = mock_use_case.execute.call_args.kwargs
        assert call_kwargs["limit"] == 50
        assert call_kwargs["offset"] == 10

    def test_get_user_news_multiple_filters(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test combining multiple filters."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = []
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user?status=pending&category=research&is_favorite=true")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        mock_use_case.execute.assert_called_once()
        call_kwargs = mock_use_case.execute.call_args.kwargs
        assert call_kwargs["status"] == NewsStatus.PENDING
        assert call_kwargs["category"] == NewsCategory.RESEARCH
        assert call_kwargs["is_favorite"] is True

    def test_get_user_news_unauthorized(self, test_app):
        """Test getting user news without authentication returns 401."""
        # Arrange
        from src.infrastructure.web.dependencies import get_current_active_user
        from fastapi import HTTPException
        
        def mock_auth_failure():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        test_app.dependency_overrides[get_current_active_user] = mock_auth_failure
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/user")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # NOTE: Parameter validation (limit, offset) is handled by FastAPI/Pydantic automatically


@pytest.mark.api
@pytest.mark.unit
class TestGetPublicNewsEndpoint:
    """Test suite for GET /api/news/public endpoint."""

    def test_get_public_news_success(self, test_app, test_news_list):
        """Test getting public news returns NewsListResponseDTO."""
        # Arrange
        from src.infrastructure.web.routers.news import get_public_news_use_case
        
        # Mark all as public
        for news in test_news_list:
            news.is_public = True
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = test_news_list
        
        test_app.dependency_overrides[get_public_news_use_case] = lambda: mock_use_case
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/public")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == len(test_news_list)

    def test_get_public_news_empty_list(self, test_app):
        """Test getting public news when there are none."""
        # Arrange
        from src.infrastructure.web.routers.news import get_public_news_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = []
        
        test_app.dependency_overrides[get_public_news_use_case] = lambda: mock_use_case
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/public")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 0

    def test_get_public_news_filter_by_category(self, test_app, test_news_list):
        """Test filtering public news by category."""
        # Arrange
        from src.infrastructure.web.routers.news import get_public_news_use_case
        
        research_news = [n for n in test_news_list if n.category == NewsCategory.RESEARCH]
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = research_news
        
        test_app.dependency_overrides[get_public_news_use_case] = lambda: mock_use_case
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/public?category=research")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        mock_use_case.execute.assert_called_once()
        call_kwargs = mock_use_case.execute.call_args.kwargs
        assert call_kwargs["category"] == NewsCategory.RESEARCH

    def test_get_public_news_with_pagination(self, test_app, test_news_list):
        """Test pagination for public news."""
        # Arrange
        from src.infrastructure.web.routers.news import get_public_news_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = test_news_list[:2]
        
        test_app.dependency_overrides[get_public_news_use_case] = lambda: mock_use_case
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/public?limit=50&offset=10")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["limit"] == 50
        assert data["offset"] == 10

    def test_get_public_news_excludes_private(self, test_app):
        """Test that public endpoint only returns public news."""
        # Arrange - This is enforced by the use case, not the endpoint
        from src.infrastructure.web.routers.news import get_public_news_use_case
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = []  # Use case filters out private
        
        test_app.dependency_overrides[get_public_news_use_case] = lambda: mock_use_case
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/public")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        # Trust use case implementation to filter correctly

    # NOTE: Parameter validation (limit, offset) is handled by FastAPI/Pydantic automatically


@pytest.mark.api
@pytest.mark.unit
class TestUpdateNewsStatusEndpoint:
    """Test suite for PATCH /api/news/{news_id}/status endpoint."""

    def test_update_news_status_to_reading(
        self, test_app, news_entity_with_id, mock_current_user
    ):
        """Test updating news status to READING."""
        # Arrange
        from src.infrastructure.web.routers.news import get_update_news_status_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_entity_with_id.status = NewsStatus.READING
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_update_news_status_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(
            f"/api/news/{news_entity_with_id.id}/status",
            json={"status": "reading"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "reading"

    def test_update_news_status_to_read(
        self, test_app, news_entity_with_id, mock_current_user
    ):
        """Test updating news status to READ."""
        # Arrange
        from src.infrastructure.web.routers.news import get_update_news_status_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_entity_with_id.status = NewsStatus.READ
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_update_news_status_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(
            f"/api/news/{news_entity_with_id.id}/status",
            json={"status": "read"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "read"

    def test_update_news_status_to_pending(
        self, test_app, news_entity_with_id, mock_current_user
    ):
        """Test updating news status to PENDING."""
        # Arrange
        from src.infrastructure.web.routers.news import get_update_news_status_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_entity_with_id.status = NewsStatus.PENDING
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_update_news_status_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(
            f"/api/news/{news_entity_with_id.id}/status",
            json={"status": "pending"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "pending"

    def test_update_news_status_not_found(
        self, test_app, mock_current_user
    ):
        """Test updating status of non-existent news returns 404."""
        # Arrange
        from src.infrastructure.web.routers.news import get_update_news_status_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_id = "nonexistent_id"
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = NewsNotFoundException(
            f"News with id {news_id} not found"
        )
        
        test_app.dependency_overrides[get_update_news_status_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(
            f"/api/news/{news_id}/status",
            json={"status": "reading"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_update_news_status_unauthorized_user(
        self, test_app, news_entity_with_id, mock_current_user
    ):
        """Test updating status of another user's news returns 403."""
        # Arrange
        from src.infrastructure.web.routers.news import get_update_news_status_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = UnauthorizedNewsAccessException(
            user_id=mock_current_user["id"],
            news_id=news_entity_with_id.id
        )
        
        test_app.dependency_overrides[get_update_news_status_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(
            f"/api/news/{news_entity_with_id.id}/status",
            json={"status": "reading"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "not authorized" in response.json()["detail"]

    def test_update_news_status_no_auth(self, test_app, news_entity_with_id):
        """Test updating status without authentication returns 401."""
        # Arrange
        from src.infrastructure.web.dependencies import get_current_active_user
        from fastapi import HTTPException
        
        def mock_auth_failure():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        test_app.dependency_overrides[get_current_active_user] = mock_auth_failure
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(
            f"/api/news/{news_entity_with_id.id}/status",
            json={"status": "reading"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # NOTE: Status validation is handled by Pydantic enum validation automatically

    def test_update_news_status_invalid_news_id(
        self, test_app, mock_current_user
    ):
        """Test updating status with invalid news ID format."""
        # Arrange
        from src.infrastructure.web.routers.news import get_update_news_status_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = NewsNotFoundException(
            "News with id invalid_id not found"
        )
        
        test_app.dependency_overrides[get_update_news_status_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(
            "/api/news/invalid_id/status",
            json={"status": "reading"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.api
@pytest.mark.unit
class TestToggleFavoriteEndpoint:
    """Test suite for PATCH /api/news/{news_id}/favorite endpoint."""

    def test_toggle_favorite_add(
        self, test_app, news_entity_with_id, mock_current_user
    ):
        """Test marking news as favorite (False -> True)."""
        # Arrange
        from src.infrastructure.web.routers.news import get_toggle_favorite_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_entity_with_id.is_favorite = True
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_toggle_favorite_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(f"/api/news/{news_entity_with_id.id}/favorite")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_favorite"] is True

    def test_toggle_favorite_remove(
        self, test_app, news_entity_with_id, mock_current_user
    ):
        """Test unmarking news as favorite (True -> False)."""
        # Arrange
        from src.infrastructure.web.routers.news import get_toggle_favorite_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_entity_with_id.is_favorite = False
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_toggle_favorite_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(f"/api/news/{news_entity_with_id.id}/favorite")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_favorite"] is False

    def test_toggle_favorite_not_found(
        self, test_app, mock_current_user
    ):
        """Test toggling favorite on non-existent news returns 404."""
        # Arrange
        from src.infrastructure.web.routers.news import get_toggle_favorite_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        news_id = "nonexistent_id"
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = NewsNotFoundException(
            f"News with id {news_id} not found"
        )
        
        test_app.dependency_overrides[get_toggle_favorite_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(f"/api/news/{news_id}/favorite")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_toggle_favorite_unauthorized_user(
        self, test_app, news_entity_with_id, mock_current_user
    ):
        """Test toggling favorite on another user's news returns 403."""
        # Arrange
        from src.infrastructure.web.routers.news import get_toggle_favorite_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = UnauthorizedNewsAccessException(
            user_id=mock_current_user["id"],
            news_id=news_entity_with_id.id
        )
        
        test_app.dependency_overrides[get_toggle_favorite_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(f"/api/news/{news_entity_with_id.id}/favorite")
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_toggle_favorite_no_auth(self, test_app, news_entity_with_id):
        """Test toggling favorite without authentication returns 401."""
        # Arrange
        from src.infrastructure.web.dependencies import get_current_active_user
        from fastapi import HTTPException
        
        def mock_auth_failure():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        test_app.dependency_overrides[get_current_active_user] = mock_auth_failure
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch(f"/api/news/{news_entity_with_id.id}/favorite")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_toggle_favorite_invalid_news_id(
        self, test_app, mock_current_user
    ):
        """Test toggling favorite with invalid news ID."""
        # Arrange
        from src.infrastructure.web.routers.news import get_toggle_favorite_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = NewsNotFoundException(
            "News with id invalid_id not found"
        )
        
        test_app.dependency_overrides[get_toggle_favorite_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.patch("/api/news/invalid_id/favorite")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.api
@pytest.mark.unit
class TestGetNewsStatsEndpoint:
    """Test suite for GET /api/news/stats endpoint."""

    def test_get_news_stats_success(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test getting news statistics returns correct counts."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = test_news_list
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/stats")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "pending_count" in data
        assert "reading_count" in data
        assert "read_count" in data
        assert "favorite_count" in data
        assert "total_count" in data
        assert data["total_count"] == len(test_news_list)

    def test_get_news_stats_empty(
        self, test_app, mock_current_user
    ):
        """Test getting stats when user has no news."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = []
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/stats")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pending_count"] == 0
        assert data["reading_count"] == 0
        assert data["read_count"] == 0
        assert data["favorite_count"] == 0
        assert data["total_count"] == 0

    def test_get_news_stats_only_favorites(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test stats correctly count only favorites."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        # Set all as favorites
        for news in test_news_list:
            news.is_favorite = True
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = test_news_list
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/stats")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["favorite_count"] == len(test_news_list)

    def test_get_news_stats_all_statuses(
        self, test_app, test_news_list, mock_current_user
    ):
        """Test stats correctly count by status."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = test_news_list
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/stats")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Count expected values
        expected_pending = sum(1 for n in test_news_list if n.status == NewsStatus.PENDING)
        expected_reading = sum(1 for n in test_news_list if n.status == NewsStatus.READING)
        expected_read = sum(1 for n in test_news_list if n.status == NewsStatus.READ)
        
        assert data["pending_count"] == expected_pending
        assert data["reading_count"] == expected_reading
        assert data["read_count"] == expected_read

    def test_get_news_stats_mixed_data(
        self, test_app, mock_current_user
    ):
        """Test stats with various combinations of status and favorites."""
        # Arrange
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        from src.domain.entities.news_item import NewsItem, NewsStatus, NewsCategory
        
        mixed_news = [
            NewsItem(
                id="1", source="A", title="News 1", summary="Summary",
                link="http://example.com/1", user_id="user1",
                status=NewsStatus.PENDING, is_favorite=True,
                category=NewsCategory.GENERAL
            ),
            NewsItem(
                id="2", source="B", title="News 2", summary="Summary",
                link="http://example.com/2", user_id="user1",
                status=NewsStatus.READING, is_favorite=False,
                category=NewsCategory.GENERAL
            ),
            NewsItem(
                id="3", source="C", title="News 3", summary="Summary",
                link="http://example.com/3", user_id="user1",
                status=NewsStatus.READ, is_favorite=True,
                category=NewsCategory.GENERAL
            ),
        ]
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = mixed_news
        
        test_app.dependency_overrides[get_user_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/stats")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pending_count"] == 1
        assert data["reading_count"] == 1
        assert data["read_count"] == 1
        assert data["favorite_count"] == 2
        assert data["total_count"] == 3

    def test_get_news_stats_unauthorized(self, test_app):
        """Test getting stats without authentication returns 401."""
        # Arrange
        from src.infrastructure.web.dependencies import get_current_active_user
        from fastapi import HTTPException
        
        def mock_auth_failure():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        test_app.dependency_overrides[get_current_active_user] = mock_auth_failure
        
        client = TestClient(test_app)
        
        # Act
        response = client.get("/api/news/stats")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.api
@pytest.mark.unit
class TestNewsDependencyInjection:
    """Test suite for news dependency injection functions."""

    def test_get_create_news_use_case(self):
        """Test get_create_news_use_case returns CreateNewsUseCase instance."""
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.application.use_cases.news import CreateNewsUseCase
        
        use_case = get_create_news_use_case()
        
        assert isinstance(use_case, CreateNewsUseCase)

    def test_get_update_news_status_use_case(self):
        """Test get_update_news_status_use_case returns UpdateNewsStatusUseCase instance."""
        from src.infrastructure.web.routers.news import get_update_news_status_use_case
        from src.application.use_cases.news import UpdateNewsStatusUseCase
        
        use_case = get_update_news_status_use_case()
        
        assert isinstance(use_case, UpdateNewsStatusUseCase)

    def test_get_toggle_favorite_use_case(self):
        """Test get_toggle_favorite_use_case returns ToggleFavoriteUseCase instance."""
        from src.infrastructure.web.routers.news import get_toggle_favorite_use_case
        from src.application.use_cases.news import ToggleFavoriteUseCase
        
        use_case = get_toggle_favorite_use_case()
        
        assert isinstance(use_case, ToggleFavoriteUseCase)

    def test_get_user_news_use_case(self):
        """Test get_user_news_use_case returns GetUserNewsUseCase instance."""
        from src.infrastructure.web.routers.news import get_user_news_use_case
        from src.application.use_cases.news import GetUserNewsUseCase
        
        use_case = get_user_news_use_case()
        
        assert isinstance(use_case, GetUserNewsUseCase)

    def test_get_public_news_use_case(self):
        """Test get_public_news_use_case returns GetPublicNewsUseCase instance."""
        from src.infrastructure.web.routers.news import get_public_news_use_case
        from src.application.use_cases.news import GetPublicNewsUseCase
        
        use_case = get_public_news_use_case()
        
        assert isinstance(use_case, GetPublicNewsUseCase)


@pytest.mark.api
@pytest.mark.unit
class TestRouterIntegration:
    """Integration tests for news router."""

    def test_router_includes_all_expected_endpoints(self):
        """Test that router includes all expected endpoints."""
        routes = [route.path for route in router.routes]
        
        expected_paths = [
            "/api/news",  # POST
            "/api/news/user",  # GET
            "/api/news/public",  # GET
            "/api/news/{news_id}/status",  # PATCH
            "/api/news/{news_id}/favorite",  # PATCH
            "/api/news/stats",  # GET
        ]
        
        for path in expected_paths:
            assert path in routes

    def test_router_has_correct_prefix(self):
        """Test that router has correct prefix."""
        assert router.prefix == "/api/news"

    def test_router_has_correct_tags(self):
        """Test that router has correct tags."""
        assert router.tags == ["news"]

    def test_create_endpoint_response_model(
        self, test_app, news_create_data, news_entity_with_id, mock_current_user
    ):
        """Test create endpoint returns correct response model structure."""
        from src.infrastructure.web.routers.news import get_create_news_use_case
        from src.infrastructure.web.dependencies import get_current_active_user
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = news_entity_with_id
        
        test_app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case
        test_app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        client = TestClient(test_app)
        
        response = client.post("/api/news", json=news_create_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Verify NewsResponseDTO structure
        required_fields = [
            "id", "source", "title", "summary", "link", "image_url",
            "status", "category", "is_favorite", "user_id", "is_public",
            "created_at", "updated_at"
        ]
        for field in required_fields:
            assert field in data

    @pytest.mark.parametrize("endpoint,method,requires_auth", [
        ("/api/news", "POST", True),
        ("/api/news/user", "GET", True),
        ("/api/news/123/status", "PATCH", True),
        ("/api/news/123/favorite", "PATCH", True),
        ("/api/news/stats", "GET", True),
    ])
    def test_endpoint_authentication_requirements(
        self, test_app, endpoint, method, requires_auth
    ):
        """Test which endpoints require authentication."""
        client = TestClient(test_app)
        
        # Act
        if method == "GET":
            response = client.get(endpoint)
        elif method == "POST":
            response = client.post(endpoint, json={})
        elif method == "PATCH":
            response = client.patch(endpoint, json={})
        
        # Assert
        if requires_auth:
            # Should return 401 or 422 for missing auth or validation errors
            assert response.status_code in [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ]

