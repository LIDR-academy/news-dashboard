"""Update user use case."""

from typing import Optional

from src.application.ports.repositories import UserRepositoryPort
from src.domain.entities.user import User
from src.domain.exceptions.user import UserNotFoundError, UserAlreadyExistsError


class UpdateUserUseCase:
    """Use case for updating user profile information."""

    def __init__(self, user_repository: UserRepositoryPort):
        """Initialize the use case with user repository."""
        self._user_repository = user_repository

    async def execute(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None
    ) -> User:
        """
        Update user profile information.
        
        Args:
            user_id: The ID of the user to update
            username: New username (optional)
            email: New email (optional)
            
        Returns:
            Updated user entity
            
        Raises:
            UserNotFoundError: If user doesn't exist
            UserAlreadyExistsError: If email or username already exists
        """
        # Get existing user
        existing_user = await self._user_repository.get_by_id(user_id)
        if not existing_user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        # Check if email is being changed and if it already exists
        if email and email != existing_user.email:
            existing_user_by_email = await self._user_repository.get_by_email(email)
            if existing_user_by_email:
                raise UserAlreadyExistsError(f"User with email {email} already exists")

        # Check if username is being changed and if it already exists
        if username and username != existing_user.username:
            existing_user_by_username = await self._user_repository.get_by_username(username)
            if existing_user_by_username:
                raise UserAlreadyExistsError(f"User with username {username} already exists")

        # Update user fields
        update_data = {}
        if username is not None:
            update_data['username'] = username
        if email is not None:
            update_data['email'] = email

        # Update user in repository
        updated_user = await self._user_repository.update_user(user_id, update_data)
        return updated_user
