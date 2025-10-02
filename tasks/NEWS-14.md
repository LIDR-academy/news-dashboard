# NEWS-14: Implement User Profile Section (Backend)

## Overview
This ticket implements the backend functionality for user profile management, including profile updates and password changes. The implementation follows the existing hexagonal architecture patterns and extends the current user management system.

## Current State Analysis
- ✅ User entity exists with basic fields (id, email, username, hashed_password, is_active, created_at, updated_at)
- ✅ User repository with MongoDB adapter implemented
- ✅ Basic user use cases (create, read, authenticate, logout)
- ✅ User DTOs and mappers for basic operations
- ✅ Authentication and authorization system
- ❌ **Missing**: Update user profile functionality
- ❌ **Missing**: Change password functionality
- ❌ **Missing**: Profile-specific DTOs and routes

## Implementation Plan

### Step 1: Extend Domain Entity (if needed)
**File**: `backend/src/domain/entities/user.py`

**Actions**:
- Review current User entity fields
- Add any additional profile fields if required (e.g., first_name, last_name, bio, avatar_url)
- Add business methods for profile updates
- Ensure validation logic in `__post_init__` covers new fields

**Business Methods to Add**:
```python
def update_profile(self, email: str = None, username: str = None, **kwargs) -> None:
    """Update user profile information."""
    
def change_password(self, new_hashed_password: str) -> None:
    """Change user password."""
```

### Step 2: Create Domain Exceptions
**File**: `backend/src/domain/exceptions/user.py`

**Actions**:
- Add new exceptions for profile operations:
  - `ProfileUpdateError`: For profile update failures
  - `PasswordChangeError`: For password change failures
  - `InvalidProfileDataError`: For invalid profile data

**Exception Examples**:
```python
class ProfileUpdateError(DomainException):
    """Raised when profile update fails."""
    pass

class PasswordChangeError(DomainException):
    """Raised when password change fails."""
    pass

class InvalidProfileDataError(ValidationError):
    """Raised when profile data is invalid."""
    pass
```

### Step 3: Create Profile Update Use Cases
**File**: `backend/src/application/use_cases/user_use_cases/update_user_use_case.py`

**Actions**:
- Create `UpdateUserProfileUseCase` class
- Create `ChangePasswordUseCase` class
- Follow existing use case patterns with dependency injection
- Implement proper validation and error handling
- Ensure business rules are enforced

**Use Case Structure**:
```python
class UpdateUserProfileUseCase:
    """Use case for updating user profile."""
    
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str, **profile_data) -> User:
        """Execute the profile update use case."""
        # 1. Validate user exists
        # 2. Validate new data
        # 3. Check for conflicts (email/username uniqueness)
        # 4. Update user entity
        # 5. Persist changes
        # 6. Return updated user

class ChangePasswordUseCase:
    """Use case for changing user password."""
    
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Execute the password change use case."""
        # 1. Validate user exists
        # 2. Verify current password
        # 3. Validate new password
        # 4. Hash new password
        # 5. Update user entity
        # 6. Persist changes
```

### Step 4: Create Profile DTOs
**File**: `backend/src/infrastructure/web/dto/user_dto.py`

**Actions**:
- Add `UserProfileUpdateRequest` DTO
- Add `ChangePasswordRequest` DTO
- Add `UserProfileResponse` DTO (if different from existing UserResponse)
- Include proper validation rules and field constraints

**DTO Examples**:
```python
class UserProfileUpdateRequest(BaseModel):
    """DTO for updating user profile."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    # Add other profile fields as needed
    
    class Config:
        json_schema_extra = {"example": {"email": "new@example.com", "username": "newusername"}}

class ChangePasswordRequest(BaseModel):
    """DTO for changing password."""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)
    
    class Config:
        json_schema_extra = {"example": {"current_password": "oldpass", "new_password": "newpass123"}}
```

### Step 5: Extend User Mapper
**File**: `backend/src/infrastructure/web/mappers.py`

**Actions**:
- Add methods for converting profile update requests to domain entities
- Add methods for handling partial updates
- Ensure proper mapping between DTOs and domain entities

**Mapper Methods**:
```python
@staticmethod
def from_profile_update_request(user: User, request: UserProfileUpdateRequest) -> User:
    """Convert profile update request to updated user entity."""
    
@staticmethod
def to_profile_response(user: User) -> UserProfileResponse:
    """Convert user entity to profile response DTO."""
```

### Step 6: Create Profile Routes
**File**: `backend/src/infrastructure/web/routers/users.py`

**Actions**:
- Add `PUT /users/me` endpoint for profile updates
- Add `PUT /users/me/password` endpoint for password changes
- Implement proper authentication and authorization
- Add comprehensive error handling and HTTP status codes
- Follow existing route patterns and security practices

**Route Examples**:
```python
@router.put("/users/me", response_model=UserResponse)
async def update_user_profile(
    profile_data: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    update_profile_use_case: UpdateUserProfileUseCase = Depends(get_update_profile_use_case)
):
    """Update current user's profile."""
    # Implementation with proper error handling

@router.put("/users/me/password", response_model=dict)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    change_password_use_case: ChangePasswordUseCase = Depends(get_change_password_use_case)
):
    """Change current user's password."""
    # Implementation with proper error handling
```

### Step 7: Update Dependencies
**File**: `backend/src/infrastructure/web/dependencies.py`

**Actions**:
- Add dependency injection functions for new use cases:
  - `get_update_profile_use_case()`
  - `get_change_password_use_case()`
- Follow existing dependency injection patterns
- Use `@lru_cache()` for singleton repositories

**Dependency Functions**:
```python
def get_update_profile_use_case(
    user_repository: UserRepositoryPort = Depends(get_user_repository)
) -> UpdateUserProfileUseCase:
    """Get update profile use case instance."""
    return UpdateUserProfileUseCase(user_repository)

def get_change_password_use_case(
    user_repository: UserRepositoryPort = Depends(get_user_repository)
) -> ChangePasswordUseCase:
    """Get change password use case instance."""
    return ChangePasswordUseCase(user_repository)
```

### Step 8: Update Use Cases Package
**File**: `backend/src/application/use_cases/user_use_cases/__init__.py`

**Actions**:
- Import new use cases
- Add to `__all__` list for proper exports
- Ensure all use cases are accessible

### Step 9: Create Comprehensive Tests
**Files**: 
- `backend/tests/application/test_user_profile_use_cases.py`
- `backend/tests/infrastructure/web/test_user_profile_routes.py`

**Test Coverage**:
- Unit tests for use cases (success and failure scenarios)
- Integration tests for routes
- Test authentication and authorization
- Test validation and error handling
- Test business rule enforcement
- Test edge cases and security scenarios

**Test Scenarios**:
- Profile update with valid data
- Profile update with invalid data
- Profile update with duplicate email/username
- Password change with correct current password
- Password change with incorrect current password
- Unauthorized access attempts
- Non-existent user scenarios

### Step 10: Update API Documentation
**Actions**:
- Ensure all new endpoints are properly documented
- Add OpenAPI examples for request/response DTOs
- Document error responses and status codes
- Update API documentation with new profile endpoints

## Security Considerations

1. **Authentication**: All profile endpoints must require valid JWT token
2. **Authorization**: Users can only update their own profile
3. **Password Security**: 
   - Verify current password before allowing change
   - Hash new passwords using secure hashing
   - Enforce password complexity rules
4. **Data Validation**: 
   - Validate all input data
   - Prevent SQL injection and XSS attacks
   - Sanitize user inputs
5. **Rate Limiting**: Consider rate limiting for password change endpoints

## Error Handling

1. **Domain Exceptions**: Use domain-specific exceptions for business rule violations
2. **HTTP Status Codes**: Map domain exceptions to appropriate HTTP status codes
3. **Error Messages**: Provide clear, user-friendly error messages
4. **Logging**: Log security-relevant events (password changes, profile updates)

## API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| PUT | `/users/me` | Update user profile | Yes |
| PUT | `/users/me/password` | Change user password | Yes |
| GET | `/users/me` | Get current user profile | Yes |

## Dependencies

- Existing user repository and entity
- Existing authentication system
- Existing DTO and mapper patterns
- MongoDB database connection
- Password hashing utilities

## Acceptance Criteria

1. ✅ Users can update their profile information (email, username, etc.)
2. ✅ Users can change their password with current password verification
3. ✅ All endpoints require authentication
4. ✅ Users can only update their own profile
5. ✅ Proper validation and error handling
6. ✅ Comprehensive test coverage
7. ✅ Follows existing architectural patterns
8. ✅ API documentation is updated
9. ✅ Security best practices are implemented

## Implementation Order

1. Domain layer (entities, exceptions)
2. Application layer (use cases)
3. Infrastructure layer (DTOs, mappers, routes, dependencies)
4. Tests
5. Documentation

This plan ensures a complete, secure, and maintainable implementation of the user profile section backend functionality.
