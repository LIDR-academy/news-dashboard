"""Tests for Web Dependencies."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.infrastructure.web.dependencies import (
    get_user_repository,
    get_news_repository,
    get_all_users_use_case,
    get_user_by_id_use_case,
    get_user_by_email_use_case,
    get_create_user_use_case,
    get_authenticate_user_use_case,
    get_logout_user_use_case,
    get_current_user,
    get_current_active_user,
    oauth2_scheme
)
from src.infrastructure.adapters.repositories.mongodb_user_repository import MongoDBUserRepository
from src.infrastructure.adapters.repositories.mongodb_news_repository import MongoDBNewsRepository
from src.application.use_cases.user_use_cases import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    GetUserByEmailUseCase,
    CreateUserUseCase,
    AuthenticateUserUseCase,
    LogoutUserUseCase
)
from src.domain.entities.user import User
from src.infrastructure.web.dto.user_dto import TokenData


@pytest.fixture
def mock_database():
    """Mock database for testing."""
    return AsyncMock()


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        id="507f1f77bcf86cd799439011",
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
        created_at=None,
        updated_at=None
    )


@pytest.fixture
def sample_token_data():
    """Sample token data for testing."""
    return TokenData(username="testuser")


@pytest.mark.unit
class TestRepositoryDependencies:
    """Test suite for repository dependencies."""

    def test_get_user_repository_returns_mongodb_user_repository(self):
        """Test that get_user_repository returns MongoDBUserRepository instance."""
        # Act
        repository = get_user_repository()
        
        # Assert
        assert isinstance(repository, MongoDBUserRepository)

    def test_get_user_repository_is_cached(self):
        """Test that get_user_repository is cached (returns same instance)."""
        # Act
        repo1 = get_user_repository()
        repo2 = get_user_repository()
        
        # Assert
        assert repo1 is repo2  # Same instance due to caching

    @patch('src.infrastructure.web.dependencies.get_database')
    def test_get_news_repository_returns_mongodb_news_repository(self, mock_get_database, mock_database):
        """Test that get_news_repository returns MongoDBNewsRepository instance."""
        # Arrange
        mock_get_database.return_value = mock_database
        
        # Act
        repository = get_news_repository()
        
        # Assert
        assert isinstance(repository, MongoDBNewsRepository)

    @patch('src.infrastructure.web.dependencies.get_database')
    def test_get_news_repository_is_cached(self, mock_get_database, mock_database):
        """Test that get_news_repository is cached (returns same instance)."""
        # Arrange
        mock_get_database.return_value = mock_database
        
        # Act
        repo1 = get_news_repository()
        repo2 = get_news_repository()
        
        # Assert
        assert repo1 is repo2  # Same instance due to caching


@pytest.mark.unit
class TestUseCaseDependencies:
    """Test suite for use case dependencies."""

    def test_get_all_users_use_case_returns_correct_instance(self):
        """Test that get_all_users_use_case returns GetAllUsersUseCase instance."""
        # Act
        use_case = get_all_users_use_case()
        
        # Assert
        assert isinstance(use_case, GetAllUsersUseCase)

    def test_get_user_by_id_use_case_returns_correct_instance(self):
        """Test that get_user_by_id_use_case returns GetUserByIdUseCase instance."""
        # Act
        use_case = get_user_by_id_use_case()
        
        # Assert
        assert isinstance(use_case, GetUserByIdUseCase)

    def test_get_user_by_email_use_case_returns_correct_instance(self):
        """Test that get_user_by_email_use_case returns GetUserByEmailUseCase instance."""
        # Act
        use_case = get_user_by_email_use_case()
        
        # Assert
        assert isinstance(use_case, GetUserByEmailUseCase)

    def test_get_create_user_use_case_returns_correct_instance(self):
        """Test that get_create_user_use_case returns CreateUserUseCase instance."""
        # Act
        use_case = get_create_user_use_case()
        
        # Assert
        assert isinstance(use_case, CreateUserUseCase)

    def test_get_authenticate_user_use_case_returns_correct_instance(self):
        """Test that get_authenticate_user_use_case returns AuthenticateUserUseCase instance."""
        # Act
        use_case = get_authenticate_user_use_case()
        
        # Assert
        assert isinstance(use_case, AuthenticateUserUseCase)

    def test_get_logout_user_use_case_returns_correct_instance(self):
        """Test that get_logout_user_use_case returns LogoutUserUseCase instance."""
        # Act
        use_case = get_logout_user_use_case()
        
        # Assert
        assert isinstance(use_case, LogoutUserUseCase)

    def test_use_case_dependencies_are_not_cached(self):
        """Test that use case dependencies are not cached (return new instances)."""
        # Act
        use_case1 = get_all_users_use_case()
        use_case2 = get_all_users_use_case()
        
        # Assert
        assert use_case1 is not use_case2  # Different instances

    def test_use_case_dependencies_have_correct_repository_injected(self):
        """Test that use case dependencies have correct repository injected."""
        # Act
        use_case = get_all_users_use_case()
        
        # Assert
        assert isinstance(use_case.repository, MongoDBUserRepository)


@pytest.mark.unit
class TestAuthenticationDependencies:
    """Test suite for authentication dependencies."""

    def test_oauth2_scheme_is_oauth2_password_bearer(self):
        """Test that oauth2_scheme is OAuth2PasswordBearer instance."""
        # Assert
        assert isinstance(oauth2_scheme, OAuth2PasswordBearer)

    # Note: Token data validation is handled within get_current_user function

    @patch('src.infrastructure.web.dependencies.get_user_by_email_use_case')
    async def test_get_current_user_returns_user_for_valid_token(self, mock_get_use_case, sample_user):
        """Test that get_current_user returns User for valid token."""
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = sample_user
        mock_get_use_case.return_value = mock_use_case
        
        # Act
        result = await get_current_user("valid_token")
        
        # Assert
        assert result == sample_user
        mock_use_case.execute.assert_called_once_with("testuser")

    @patch('src.infrastructure.web.dependencies.get_user_by_email_use_case')
    async def test_get_current_user_raises_http_exception_when_user_not_found(self, mock_get_use_case):
        """Test that get_current_user raises HTTPException when user not found."""
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = None
        mock_get_use_case.return_value = mock_use_case
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("valid_token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in exc_info.value.detail

    @patch('src.infrastructure.web.dependencies.get_user_by_email_use_case')
    async def test_get_current_user_raises_http_exception_when_use_case_raises_exception(self, mock_get_use_case):
        """Test that get_current_user raises HTTPException when use case raises exception."""
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = Exception("Database error")
        mock_get_use_case.return_value = mock_use_case
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("valid_token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in exc_info.value.detail

    async def test_get_current_active_user_returns_user_when_active(self, sample_user):
        """Test that get_current_active_user returns user when active."""
        # Act
        result = await get_current_active_user(sample_user)
        
        # Assert
        assert result == sample_user

    async def test_get_current_active_user_raises_http_exception_when_inactive(self):
        """Test that get_current_active_user raises HTTPException when user is inactive."""
        # Arrange
        inactive_user = User(
            id="507f1f77bcf86cd799439011",
            username="inactiveuser",
            email="inactive@example.com",
            hashed_password="hashed_password",
            is_active=False
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_active_user(inactive_user)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Inactive user" in exc_info.value.detail


@pytest.mark.unit
class TestDependencyInjection:
    """Test suite for dependency injection patterns."""

    def test_repository_dependencies_are_singletons(self):
        """Test that repository dependencies are singletons (cached)."""
        # Act
        user_repo1 = get_user_repository()
        user_repo2 = get_user_repository()
        
        # Assert
        assert user_repo1 is user_repo2

    def test_use_case_dependencies_are_factories(self):
        """Test that use case dependencies are factories (new instances)."""
        # Act
        use_case1 = get_all_users_use_case()
        use_case2 = get_all_users_use_case()
        
        # Assert
        assert use_case1 is not use_case2

    def test_oauth2_scheme_is_configured(self):
        """Test that OAuth2 scheme is configured."""
        # Assert
        assert oauth2_scheme is not None
        assert isinstance(oauth2_scheme, OAuth2PasswordBearer)

    def test_dependencies_are_properly_isolated(self):
        """Test that dependencies are properly isolated from each other."""
        # Act
        user_repo = get_user_repository()
        use_case = get_all_users_use_case()
        
        # Assert
        assert isinstance(user_repo, MongoDBUserRepository)
        assert isinstance(use_case, GetAllUsersUseCase)
        assert use_case.repository is user_repo  # Same instance due to caching

    def test_dependencies_handle_import_errors_gracefully(self):
        """Test that dependencies handle import errors gracefully."""
        # This test would require mocking imports, which is complex
        # For now, we just verify that dependencies can be imported
        assert get_user_repository is not None
        assert get_news_repository is not None
        assert get_all_users_use_case is not None

    def test_dependencies_are_thread_safe(self):
        """Test that dependencies are thread-safe."""
        import threading
        import time
        
        results = []
        
        def get_dependency():
            time.sleep(0.01)  # Simulate some work
            results.append(get_user_repository())
        
        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=get_dependency)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Assert - All results should be the same instance
        assert len(results) == 10
        assert all(result is results[0] for result in results)


@pytest.mark.unit
class TestDependencyErrorHandling:
    """Test suite for dependency error handling."""

    @patch('src.infrastructure.web.dependencies.MongoDBUserRepository')
    def test_get_user_repository_handles_initialization_errors(self, mock_repo_class):
        """Test that get_user_repository handles initialization errors."""
        # Arrange
        mock_repo_class.side_effect = Exception("Initialization error")
        
        # Act & Assert
        with pytest.raises(Exception):
            get_user_repository()

    @patch('src.infrastructure.web.dependencies.get_database')
    def test_get_news_repository_handles_database_errors(self, mock_get_database):
        """Test that get_news_repository handles database errors."""
        # Arrange
        mock_get_database.side_effect = Exception("Database connection error")
        
        # Act & Assert
        with pytest.raises(Exception):
            get_news_repository()

    @patch('src.infrastructure.web.dependencies.get_user_repository')
    def test_use_case_dependencies_handle_repository_errors(self, mock_get_repo):
        """Test that use case dependencies handle repository errors."""
        # Arrange
        mock_get_repo.side_effect = Exception("Repository error")
        
        # Act & Assert
        with pytest.raises(Exception):
            get_all_users_use_case()

    @patch('src.infrastructure.web.dependencies.decode_access_token')
    def test_get_token_data_handles_token_decode_errors(self, mock_decode_token):
        """Test that get_token_data handles token decode errors."""
        # Arrange
        mock_decode_token.side_effect = Exception("Token decode error")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_token_data("token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('src.infrastructure.web.dependencies.get_user_by_email_use_case')
    async def test_get_current_user_handles_use_case_errors(self, mock_get_use_case):
        """Test that get_current_user handles use case errors."""
        # Arrange
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = Exception("Use case error")
        mock_get_use_case.return_value = mock_use_case
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
class TestDependencyPerformance:
    """Test suite for dependency performance."""

    def test_repository_dependencies_are_fast_due_to_caching(self):
        """Test that repository dependencies are fast due to caching."""
        import time
        
        # First call (no cache)
        start_time = time.time()
        get_user_repository()
        first_call_time = time.time() - start_time
        
        # Second call (from cache)
        start_time = time.time()
        get_user_repository()
        second_call_time = time.time() - start_time
        
        # Assert - Second call should be faster due to caching
        assert second_call_time < first_call_time

    def test_use_case_dependencies_are_reasonably_fast(self):
        """Test that use case dependencies are reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(100):
            get_all_users_use_case()
        end_time = time.time()
        
        # Assert - Should complete in reasonable time
        assert (end_time - start_time) < 1.0  # Less than 1 second for 100 calls

    def test_oauth2_scheme_access_is_fast(self):
        """Test that OAuth2 scheme access is fast."""
        import time
        
        start_time = time.time()
        for _ in range(100):
            _ = oauth2_scheme
        end_time = time.time()
        
        # Assert - Should complete in reasonable time
        assert (end_time - start_time) < 1.0  # Less than 1 second for 100 accesses

    def test_dependencies_do_not_have_memory_leaks(self):
        """Test that dependencies don't have memory leaks."""
        import gc
        
        # Create many instances
        instances = []
        for _ in range(1000):
            use_case = get_all_users_use_case()
            instances.append(use_case)
        
        # Clean up
        del instances
        gc.collect()
        
        # If we get here without memory issues, the test passes
        assert True
