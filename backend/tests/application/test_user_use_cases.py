"""Tests for User use cases."""

import pytest
from unittest.mock import AsyncMock

from src.domain.entities.user import User
from src.domain.exceptions.user import UserNotFoundError, InvalidUserDataError, UserAlreadyExistsError
from src.application.use_cases.user_use_cases import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    GetUserByEmailUseCase,
    CreateUserUseCase,
    AuthenticateUserUseCase,
    LogoutUserUseCase
)


@pytest.mark.service
@pytest.mark.unit
class TestGetAllUsersUseCase:
    """Test suite for GetAllUsersUseCase."""

    async def test_execute_returns_all_users_from_repository(self, mock_user_repository, test_users_list):
        """Test that execute returns all users from repository."""
        # Arrange
        mock_user_repository.find_all.return_value = test_users_list
        use_case = GetAllUsersUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute()
        
        # Assert
        assert result == test_users_list
        mock_user_repository.find_all.assert_called_once_with(100)  # Default limit

    async def test_execute_with_custom_limit_passes_limit_to_repository(self, mock_user_repository, test_users_list):
        """Test that execute passes custom limit to repository."""
        # Arrange
        custom_limit = 50
        expected_users = test_users_list[:2]  # Simulate limited results
        mock_user_repository.find_all.return_value = expected_users
        use_case = GetAllUsersUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(custom_limit)
        
        # Assert
        assert result == expected_users
        mock_user_repository.find_all.assert_called_once_with(custom_limit)

    async def test_execute_returns_empty_list_when_no_users_exist(self, mock_user_repository):
        """Test that execute returns empty list when no users exist."""
        # Arrange
        mock_user_repository.find_all.return_value = []
        use_case = GetAllUsersUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute()
        
        # Assert
        assert result == []
        mock_user_repository.find_all.assert_called_once_with(100)

    async def test_execute_propagates_repository_exceptions(self, mock_user_repository):
        """Test that execute propagates repository exceptions."""
        # Arrange
        repository_error = Exception("Database connection failed")
        mock_user_repository.find_all.side_effect = repository_error
        use_case = GetAllUsersUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute()
        
        assert str(exc_info.value) == "Database connection failed"


@pytest.mark.service
@pytest.mark.unit
class TestGetUserByIdUseCase:
    """Test suite for GetUserByIdUseCase."""

    async def test_execute_returns_user_when_found(self, mock_user_repository, user_entity_with_id):
        """Test that execute returns user when found by ID."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        mock_user_repository.find_by_id.return_value = user_entity_with_id
        use_case = GetUserByIdUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(user_id)
        
        # Assert
        assert result == user_entity_with_id
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    async def test_execute_raises_user_not_found_error_when_user_not_found(self, mock_user_repository):
        """Test that execute raises UserNotFoundError when user not found."""
        # Arrange
        user_id = "nonexistent_id"
        mock_user_repository.find_by_id.return_value = None
        use_case = GetUserByIdUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(UserNotFoundError) as exc_info:
            await use_case.execute(user_id)
        
        assert exc_info.value.entity_id == user_id
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    async def test_execute_propagates_repository_exceptions(self, mock_user_repository):
        """Test that execute propagates repository exceptions."""
        # Arrange
        user_id = "test_id"
        repository_error = Exception("Database error")
        mock_user_repository.find_by_id.side_effect = repository_error
        use_case = GetUserByIdUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(user_id)
        
        assert str(exc_info.value) == "Database error"


@pytest.mark.service
@pytest.mark.unit
class TestGetUserByEmailUseCase:
    """Test suite for GetUserByEmailUseCase."""

    async def test_execute_returns_user_when_found_by_email(self, mock_user_repository, user_entity_with_id):
        """Test that execute returns user when found by email."""
        # Arrange
        email = "test@example.com"
        mock_user_repository.find_by_email.return_value = user_entity_with_id
        use_case = GetUserByEmailUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(email)
        
        # Assert
        assert result == user_entity_with_id
        mock_user_repository.find_by_email.assert_called_once_with(email)

    async def test_execute_raises_user_not_found_error_when_user_not_found(self, mock_user_repository):
        """Test that execute raises UserNotFoundError with email identifier when user not found."""
        # Arrange
        email = "nonexistent@example.com"
        mock_user_repository.find_by_email.return_value = None
        use_case = GetUserByEmailUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(UserNotFoundError) as exc_info:
            await use_case.execute(email)
        
        assert exc_info.value.entity_id == f"email:{email}"
        mock_user_repository.find_by_email.assert_called_once_with(email)

    async def test_execute_propagates_repository_exceptions(self, mock_user_repository):
        """Test that execute propagates repository exceptions."""
        # Arrange
        email = "test@example.com"
        repository_error = Exception("Database connection failed")
        mock_user_repository.find_by_email.side_effect = repository_error
        use_case = GetUserByEmailUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(email)
        
        assert str(exc_info.value) == "Database connection failed"


@pytest.mark.service
@pytest.mark.unit
class TestCreateUserUseCase:
    """Test suite for CreateUserUseCase."""

    async def test_execute_creates_user_successfully_when_data_valid_and_unique(self, mock_user_repository, user_entity_with_id):
        """Test that execute creates user successfully with valid and unique data."""
        # Arrange
        email = "test@example.com"
        username = "testuser"
        hashed_password = "hashed123"
        
        # Mock repository to return None for uniqueness checks
        mock_user_repository.find_by_email.return_value = None
        mock_user_repository.find_by_username.return_value = None
        mock_user_repository.create.return_value = user_entity_with_id
        
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(email, username, hashed_password)
        
        # Assert
        assert result == user_entity_with_id
        mock_user_repository.find_by_email.assert_called_once_with(email)
        mock_user_repository.find_by_username.assert_called_once_with(username)
        mock_user_repository.create.assert_called_once()
        
        # Verify the User entity passed to create
        created_user = mock_user_repository.create.call_args[0][0]
        assert created_user.email == email
        assert created_user.username == username
        assert created_user.hashed_password == hashed_password

    async def test_execute_raises_invalid_user_data_error_when_domain_validation_fails(self, mock_user_repository):
        """Test that execute raises InvalidUserDataError when domain validation fails."""
        # Arrange
        invalid_email = ""  # Invalid email that will trigger domain validation
        username = "testuser"
        hashed_password = "hashed123"
        
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(InvalidUserDataError) as exc_info:
            await use_case.execute(invalid_email, username, hashed_password)
        
        assert "User email cannot be empty" in str(exc_info.value)
        # Repository methods should not be called if validation fails
        mock_user_repository.find_by_email.assert_not_called()
        mock_user_repository.find_by_username.assert_not_called()
        mock_user_repository.create.assert_not_called()

    async def test_execute_raises_user_already_exists_error_when_email_exists(self, mock_user_repository, user_entity_with_id):
        """Test that execute raises UserAlreadyExistsError when email already exists."""
        # Arrange
        email = "existing@example.com"
        username = "testuser"
        hashed_password = "hashed123"
        
        # Mock repository to return existing user for email
        mock_user_repository.find_by_email.return_value = user_entity_with_id
        
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            await use_case.execute(email, username, hashed_password)
        
        assert "User with this email already exists" in str(exc_info.value)
        mock_user_repository.find_by_email.assert_called_once_with(email)
        mock_user_repository.find_by_username.assert_not_called()
        mock_user_repository.create.assert_not_called()

    async def test_execute_raises_user_already_exists_error_when_username_exists(self, mock_user_repository, user_entity_with_id):
        """Test that execute raises UserAlreadyExistsError when username already exists."""
        # Arrange
        email = "test@example.com"
        username = "existing_user"
        hashed_password = "hashed123"
        
        # Mock repository to return None for email but existing user for username
        mock_user_repository.find_by_email.return_value = None
        mock_user_repository.find_by_username.return_value = user_entity_with_id
        
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            await use_case.execute(email, username, hashed_password)
        
        assert "User with this username already exists" in str(exc_info.value)
        mock_user_repository.find_by_email.assert_called_once_with(email)
        mock_user_repository.find_by_username.assert_called_once_with(username)
        mock_user_repository.create.assert_not_called()

    @pytest.mark.parametrize("invalid_email", ["", "   ", "invalid.email"])
    async def test_execute_raises_invalid_user_data_error_for_various_invalid_emails(self, invalid_email, mock_user_repository):
        """Test execute raises InvalidUserDataError for various invalid email formats."""
        # Arrange
        username = "testuser"
        hashed_password = "hashed123"
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(InvalidUserDataError):
            await use_case.execute(invalid_email, username, hashed_password)

    @pytest.mark.parametrize("invalid_username", ["", "   "])
    async def test_execute_raises_invalid_user_data_error_for_invalid_usernames(self, invalid_username, mock_user_repository):
        """Test execute raises InvalidUserDataError for invalid usernames."""
        # Arrange
        email = "test@example.com"
        hashed_password = "hashed123"
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(InvalidUserDataError):
            await use_case.execute(email, invalid_username, hashed_password)

    async def test_execute_propagates_repository_exceptions_from_uniqueness_checks(self, mock_user_repository):
        """Test that execute propagates repository exceptions from uniqueness checks."""
        # Arrange
        email = "test@example.com"
        username = "testuser"
        hashed_password = "hashed123"
        
        repository_error = Exception("Database connection failed")
        mock_user_repository.find_by_email.side_effect = repository_error
        
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(email, username, hashed_password)
        
        assert str(exc_info.value) == "Database connection failed"

    async def test_execute_propagates_repository_exceptions_from_create(self, mock_user_repository):
        """Test that execute propagates repository exceptions from create operation."""
        # Arrange
        email = "test@example.com"
        username = "testuser"
        hashed_password = "hashed123"
        
        mock_user_repository.find_by_email.return_value = None
        mock_user_repository.find_by_username.return_value = None
        
        repository_error = Exception("Database insert failed")
        mock_user_repository.create.side_effect = repository_error
        
        use_case = CreateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(email, username, hashed_password)
        
        assert str(exc_info.value) == "Database insert failed"


@pytest.mark.service
@pytest.mark.unit
class TestAuthenticateUserUseCase:
    """Test suite for AuthenticateUserUseCase."""

    async def test_execute_returns_user_when_found_by_username(self, mock_user_repository, user_entity_with_id):
        """Test that execute returns user when found by username."""
        # Arrange
        username = "testuser"
        mock_user_repository.find_by_username.return_value = user_entity_with_id
        use_case = AuthenticateUserUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(username)
        
        # Assert
        assert result == user_entity_with_id
        mock_user_repository.find_by_username.assert_called_once_with(username)
        mock_user_repository.find_by_email.assert_not_called()

    async def test_execute_falls_back_to_email_when_username_not_found(self, mock_user_repository, user_entity_with_id):
        """Test that execute falls back to email lookup when username not found."""
        # Arrange
        username_or_email = "test@example.com"
        mock_user_repository.find_by_username.return_value = None
        mock_user_repository.find_by_email.return_value = user_entity_with_id
        use_case = AuthenticateUserUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(username_or_email)
        
        # Assert
        assert result == user_entity_with_id
        mock_user_repository.find_by_username.assert_called_once_with(username_or_email)
        mock_user_repository.find_by_email.assert_called_once_with(username_or_email)

    async def test_execute_returns_none_when_user_not_found_by_username_or_email(self, mock_user_repository):
        """Test that execute returns None when user not found by username or email."""
        # Arrange
        username_or_email = "nonexistent"
        mock_user_repository.find_by_username.return_value = None
        mock_user_repository.find_by_email.return_value = None
        use_case = AuthenticateUserUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(username_or_email)
        
        # Assert
        assert result is None
        mock_user_repository.find_by_username.assert_called_once_with(username_or_email)
        mock_user_repository.find_by_email.assert_called_once_with(username_or_email)

    async def test_execute_handles_email_as_username_parameter(self, mock_user_repository, user_entity_with_id):
        """Test that execute correctly handles email passed as username parameter."""
        # Arrange
        email = "test@example.com"
        # Username lookup fails, email lookup succeeds
        mock_user_repository.find_by_username.return_value = None
        mock_user_repository.find_by_email.return_value = user_entity_with_id
        use_case = AuthenticateUserUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(email)
        
        # Assert
        assert result == user_entity_with_id
        mock_user_repository.find_by_username.assert_called_once_with(email)
        mock_user_repository.find_by_email.assert_called_once_with(email)

    async def test_execute_propagates_repository_exceptions_from_username_lookup(self, mock_user_repository):
        """Test that execute propagates repository exceptions from username lookup."""
        # Arrange
        username = "testuser"
        repository_error = Exception("Database connection failed")
        mock_user_repository.find_by_username.side_effect = repository_error
        use_case = AuthenticateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(username)
        
        assert str(exc_info.value) == "Database connection failed"

    async def test_execute_propagates_repository_exceptions_from_email_lookup(self, mock_user_repository):
        """Test that execute propagates repository exceptions from email lookup."""
        # Arrange
        username = "testuser"
        mock_user_repository.find_by_username.return_value = None
        
        repository_error = Exception("Database connection failed")
        mock_user_repository.find_by_email.side_effect = repository_error
        use_case = AuthenticateUserUseCase(mock_user_repository)
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(username)
        
        assert str(exc_info.value) == "Database connection failed"

    @pytest.mark.parametrize("identifier,expected_username_call,expected_email_call", [
        ("plainusername", True, True),  # Both lookups when username fails
        ("test@example.com", True, True),  # Email format still tries username first
        ("user123", True, True),  # Username format still tries both
    ])
    async def test_execute_lookup_strategy_with_various_identifiers(
        self, identifier, expected_username_call, expected_email_call, mock_user_repository
    ):
        """Test the lookup strategy with various identifier formats."""
        # Arrange
        mock_user_repository.find_by_username.return_value = None
        mock_user_repository.find_by_email.return_value = None
        use_case = AuthenticateUserUseCase(mock_user_repository)
        
        # Act
        result = await use_case.execute(identifier)
        
        # Assert
        assert result is None
        
        if expected_username_call:
            mock_user_repository.find_by_username.assert_called_once_with(identifier)
        else:
            mock_user_repository.find_by_username.assert_not_called()
            
        if expected_email_call:
            mock_user_repository.find_by_email.assert_called_once_with(identifier)
        else:
            mock_user_repository.find_by_email.assert_not_called()


@pytest.mark.service
@pytest.mark.unit
class TestUserUseCasesIntegration:
    """Integration tests for user use cases interaction."""

    def test_use_cases_can_be_instantiated_with_same_repository(self, mock_user_repository):
        """Test that multiple use cases can share the same repository instance."""
        # Arrange & Act
        get_all = GetAllUsersUseCase(mock_user_repository)
        get_by_id = GetUserByIdUseCase(mock_user_repository)
        get_by_email = GetUserByEmailUseCase(mock_user_repository)
        create_user = CreateUserUseCase(mock_user_repository)
        authenticate = AuthenticateUserUseCase(mock_user_repository)
        
        # Assert
        assert get_all.user_repository is mock_user_repository
        assert get_by_id.user_repository is mock_user_repository
        assert get_by_email.user_repository is mock_user_repository
        assert create_user.user_repository is mock_user_repository
        assert authenticate.user_repository is mock_user_repository

    async def test_create_and_get_user_workflow(self, mock_user_repository, user_entity_with_id):
        """Test a typical create then get user workflow."""
        # Arrange
        email = "test@example.com"
        username = "testuser"
        hashed_password = "hashed123"
        
        # Setup mocks for create use case
        mock_user_repository.find_by_email.return_value = None
        mock_user_repository.find_by_username.return_value = None
        mock_user_repository.create.return_value = user_entity_with_id
        
        create_use_case = CreateUserUseCase(mock_user_repository)
        get_use_case = GetUserByIdUseCase(mock_user_repository)
        
        # Act - Create user
        created_user = await create_use_case.execute(email, username, hashed_password)
        
        # Reset mock for get operation
        mock_user_repository.reset_mock()
        mock_user_repository.find_by_id.return_value = created_user
        
        # Act - Get user
        retrieved_user = await get_use_case.execute(created_user.id)
        
        # Assert
        assert retrieved_user == created_user
        mock_user_repository.find_by_id.assert_called_once_with(created_user.id)


@pytest.mark.service
@pytest.mark.unit
class TestLogoutUserUseCase:
    """Test suite for LogoutUserUseCase."""

    @pytest.mark.asyncio
    async def test_execute_returns_true_when_user_exists(self, mock_user_repository, user_entity_with_id):
        """Test that execute returns True when user exists."""
        # Arrange
        user_id = "507f1f77bcf86cd799439011"
        mock_user_repository.find_by_id.return_value = user_entity_with_id
        use_case = LogoutUserUseCase(mock_user_repository)

        # Act
        result = await use_case.execute(user_id)

        # Assert
        assert result is True
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_execute_raises_user_not_found_error_when_user_does_not_exist(self, mock_user_repository):
        """Test that execute raises UserNotFoundError when user does not exist."""
        # Arrange
        user_id = "nonexistent_id"
        mock_user_repository.find_by_id.return_value = None
        use_case = LogoutUserUseCase(mock_user_repository)

        # Act & Assert
        with pytest.raises(UserNotFoundError) as exc_info:
            await use_case.execute(user_id)

        assert exc_info.value.entity_id == user_id
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_execute_propagates_repository_exceptions(self, mock_user_repository):
        """Test that execute propagates repository exceptions."""
        # Arrange
        user_id = "test_id"
        repository_error = Exception("Database connection failed")
        mock_user_repository.find_by_id.side_effect = repository_error
        use_case = LogoutUserUseCase(mock_user_repository)

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(user_id)

        assert str(exc_info.value) == "Database connection failed"
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_execute_validates_user_exists_before_returning_success(self, mock_user_repository, user_entity_with_id):
        """Test that execute validates user exists before returning success."""
        # Arrange
        user_id = user_entity_with_id.id
        mock_user_repository.find_by_id.return_value = user_entity_with_id
        use_case = LogoutUserUseCase(mock_user_repository)

        # Act
        result = await use_case.execute(user_id)

        # Assert
        assert result is True
        # Verify that repository was called to validate user existence
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    @pytest.mark.parametrize("user_id", [
        "507f1f77bcf86cd799439011",  # Valid ObjectId format
        "123456789012345678901234",  # Another valid format
        "simple_string_id",          # String ID
    ])
    @pytest.mark.asyncio
    async def test_execute_works_with_various_user_id_formats(self, user_id, mock_user_repository, user_entity_with_id):
        """Test that execute works with various user ID formats."""
        # Arrange
        user_entity_with_id.id = user_id  # Set the ID to match
        mock_user_repository.find_by_id.return_value = user_entity_with_id
        use_case = LogoutUserUseCase(mock_user_repository)

        # Act
        result = await use_case.execute(user_id)

        # Assert
        assert result is True
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_execute_handles_inactive_user_successfully(self, mock_user_repository, user_entity_with_id):
        """Test that execute handles inactive user successfully."""
        # Arrange
        user_id = user_entity_with_id.id
        user_entity_with_id.is_active = False  # Inactive user
        mock_user_repository.find_by_id.return_value = user_entity_with_id
        use_case = LogoutUserUseCase(mock_user_repository)

        # Act
        result = await use_case.execute(user_id)

        # Assert
        assert result is True  # Should still allow logout even for inactive users
        mock_user_repository.find_by_id.assert_called_once_with(user_id)

    def test_constructor_injection_pattern(self, mock_user_repository):
        """Test that LogoutUserUseCase follows constructor injection pattern."""
        # Arrange & Act
        use_case = LogoutUserUseCase(mock_user_repository)

        # Assert
        assert use_case.user_repository is mock_user_repository
        assert hasattr(use_case, 'execute')
        assert callable(use_case.execute)

    def test_execute_is_async_method(self, mock_user_repository):
        """Test that execute method is properly async."""
        # Arrange
        use_case = LogoutUserUseCase(mock_user_repository)

        # Act & Assert
        import inspect
        assert inspect.iscoroutinefunction(use_case.execute)

    def test_use_case_can_be_instantiated_with_different_repositories(self, mock_user_repository):
        """Test that LogoutUserUseCase can be instantiated with different repository instances."""
        # Arrange
        another_mock_repository = AsyncMock()

        # Act
        use_case_1 = LogoutUserUseCase(mock_user_repository)
        use_case_2 = LogoutUserUseCase(another_mock_repository)

        # Assert
        assert use_case_1.user_repository is mock_user_repository
        assert use_case_2.user_repository is another_mock_repository
        assert use_case_1.user_repository is not use_case_2.user_repository