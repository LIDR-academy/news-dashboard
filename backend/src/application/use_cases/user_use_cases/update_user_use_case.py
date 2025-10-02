"""User profile update use cases."""

from typing import Optional

from src.domain.entities.user import User
from src.domain.exceptions.user import (
    UserNotFoundError, 
    InvalidProfileDataError, 
    UserAlreadyExistsError,
    PasswordChangeError,
    CurrentPasswordMismatchError
)
from src.application.ports.repositories import UserRepositoryPort
from src.infrastructure.web.security import verify_password, get_password_hash


class UpdateUserProfileUseCase:
    """Use case for updating user profile."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self, user_id: str, email: Optional[str] = None, username: Optional[str] = None) -> User:
        """Execute the profile update use case.
        
        Args:
            user_id: ID of the user to update
            email: New email (optional)
            username: New username (optional)
            
        Returns:
            User: Updated user entity
            
        Raises:
            UserNotFoundError: If user doesn't exist
            InvalidProfileDataError: If profile data is invalid
            UserAlreadyExistsError: If email or username already exists
        """
        # 1. Validate user exists
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        # 2. Check for email conflicts if email is being updated
        if email is not None and email != user.email:
            existing_user = await self.user_repository.find_by_email(email)
            if existing_user:
                raise UserAlreadyExistsError("User with this email already exists")

        # 3. Check for username conflicts if username is being updated
        if username is not None and username != user.username:
            existing_user = await self.user_repository.find_by_username(username)
            if existing_user:
                raise UserAlreadyExistsError("User with this username already exists")

        # 4. Update user entity
        try:
            user.update_profile(email=email, username=username)
        except ValueError as e:
            raise InvalidProfileDataError(str(e))

        # 5. Persist changes
        updated_user = await self.user_repository.update(user)
        return updated_user


class ChangePasswordUseCase:
    """Use case for changing user password."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Execute the password change use case.
        
        Args:
            user_id: ID of the user changing password
            current_password: Current password for verification
            new_password: New password to set
            
        Returns:
            bool: True if password change successful
            
        Raises:
            UserNotFoundError: If user doesn't exist
            CurrentPasswordMismatchError: If current password doesn't match
            PasswordChangeError: If password change fails
        """
        # 1. Validate user exists
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        # 2. Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise CurrentPasswordMismatchError("Current password is incorrect")

        # 3. Validate new password
        if not new_password or len(new_password.strip()) < 6:
            raise PasswordChangeError("New password must be at least 6 characters long")

        # 4. Hash new password
        try:
            new_hashed_password = get_password_hash(new_password)
        except Exception as e:
            raise PasswordChangeError(f"Failed to hash new password: {str(e)}")

        # 5. Update password using specific repository method
        try:
            await self.user_repository.update_password(user_id, new_hashed_password)
        except ValueError as e:
            raise PasswordChangeError(str(e))

        return True
