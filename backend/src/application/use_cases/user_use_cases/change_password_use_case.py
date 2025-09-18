"""Change password use case."""

from src.application.ports.repositories import UserRepositoryPort
from src.domain.entities.user import User
from src.domain.exceptions.user import UserNotFoundError, InvalidCredentialsError
from src.infrastructure.web.security import verify_password, get_password_hash


class ChangePasswordUseCase:
    """Use case for changing user password."""

    def __init__(self, user_repository: UserRepositoryPort):
        """Initialize the use case with user repository."""
        self._user_repository = user_repository

    async def execute(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> User:
        """
        Change user password.
        
        Args:
            user_id: The ID of the user
            current_password: Current password for verification
            new_password: New password to set
            
        Returns:
            Updated user entity
            
        Raises:
            UserNotFoundError: If user doesn't exist
            InvalidCredentialsError: If current password is incorrect
        """
        # Get existing user
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsError("Current password is incorrect")

        # Hash new password
        hashed_new_password = get_password_hash(new_password)

        # Update password in repository
        updated_user = await self._user_repository.update_user_password(user_id, hashed_new_password)
        return updated_user
