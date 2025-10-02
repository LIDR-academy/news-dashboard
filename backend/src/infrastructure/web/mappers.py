"""Mappers for converting between domain entities and DTOs."""

from typing import List, Optional

from src.domain.entities.user import User
from src.infrastructure.web.dto.user_dto import UserResponse, UserProfileUpdateRequest


class UserMapper:
    """Mapper for User entities and DTOs."""

    @staticmethod
    def to_response(user: User) -> UserResponse:
        """Convert User entity to UserResponse DTO."""
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    @staticmethod
    def to_response_list(users: List[User]) -> List[UserResponse]:
        """Convert list of User entities to list of UserResponse DTOs."""
        return [UserMapper.to_response(user) for user in users]

    @staticmethod
    def from_profile_update_request(user: User, request: UserProfileUpdateRequest) -> User:
        """Convert profile update request to updated user entity.
        
        Args:
            user: Current user entity
            request: Profile update request DTO
            
        Returns:
            User: Updated user entity with new profile data
        """
        # Create a copy of the user entity
        updated_user = User(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
        # Update only the fields that are provided in the request
        if request.email is not None:
            updated_user.email = request.email
        if request.username is not None:
            updated_user.username = request.username
            
        return updated_user

    @staticmethod
    def extract_profile_update_data(request: UserProfileUpdateRequest) -> dict:
        """Extract profile update data from request DTO.
        
        Args:
            request: Profile update request DTO
            
        Returns:
            dict: Dictionary with only non-None values for profile update
        """
        update_data = {}
        if request.email is not None:
            update_data['email'] = request.email
        if request.username is not None:
            update_data['username'] = request.username
        return update_data