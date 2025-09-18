# Backend Implementation Plan: Logout Endpoint (NEWS-1)

## Overview

This plan outlines the implementation of a `POST /api/v1/auth/logout` endpoint following the hexagonal architecture pattern established in the codebase. The implementation will be consistent with existing authentication patterns while addressing the specific requirements of token handling and security.

## Current Authentication Analysis

### Existing Structure
- **JWT-based authentication** using jose library
- **Stateless tokens** with expiration (30 minutes default)
- **No token blacklisting mechanism** currently exists
- **Dependency injection pattern** with `@lru_cache()` for repositories
- **Use case pattern** with constructor injection and single `execute` method
- **Clear separation** between domain, application, and infrastructure layers

### Authentication Flow
1. Login creates JWT token with user email as subject (`sub`)
2. Protected endpoints use `get_current_active_user` dependency
3. Token validation through `decode_access_token` function
4. No server-side token storage or tracking

## Implementation Plan

### 1. Decision: Token Invalidation Strategy

**Recommendation: Simple Success Response (No Blacklisting)**

**Rationale:**
- Current architecture uses **stateless JWT tokens**
- Adding token blacklisting would require:
  - New repository for blacklisted tokens
  - Database storage for token tracking
  - Performance overhead for every request validation
  - Complexity in token cleanup (expired tokens)
- **Frontend already handles token removal** from local storage
- **Short token expiration** (30 minutes) limits security risk
- Follows **KISS principle** and maintains stateless architecture

**Alternative Considered:**
Token blacklisting with MongoDB storage was considered but rejected due to architectural complexity and minimal security benefit given short token expiration.

### 2. Use Case Implementation

**File:** `/backend/src/application/use_cases/user_use_cases.py`

Add `LogoutUserUseCase` class:

```python
class LogoutUserUseCase:
    """Use case for user logout."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> bool:
        """Execute the logout use case.

        Args:
            user_id: ID of the user logging out

        Returns:
            bool: True if logout successful

        Raises:
            UserNotFoundError: If user doesn't exist
        """
        # Verify user exists (business rule validation)
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        # In stateless JWT implementation, logout is just a success confirmation
        # The actual token invalidation happens client-side
        return True
```

**Key Design Decisions:**
- **Validates user existence** as business rule
- **Returns boolean** for consistency with other use cases
- **Raises domain exception** for non-existent users
- **Documents the stateless approach** in docstring

### 3. Web Layer Updates

#### 3.1 Dependencies (`/backend/src/infrastructure/web/dependencies.py`)

Add dependency injection for logout use case:

```python
# Add import
from src.application.use_cases.user_use_cases import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    GetUserByEmailUseCase,
    CreateUserUseCase,
    AuthenticateUserUseCase,
    LogoutUserUseCase  # Add this import
)

# Add dependency function
def get_logout_user_use_case() -> LogoutUserUseCase:
    """Get logout user use case."""
    return LogoutUserUseCase(get_user_repository())
```

#### 3.2 DTO Updates (`/backend/src/infrastructure/web/dto/user_dto.py`)

Add logout response DTO:

```python
class LogoutResponse(BaseModel):
    """DTO for logout response."""
    message: str
    success: bool
```

#### 3.3 Router Implementation (`/backend/src/infrastructure/web/routers/users.py`)

Add logout endpoint:

```python
# Add imports
from src.application.use_cases.user_use_cases import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    CreateUserUseCase,
    AuthenticateUserUseCase,
    LogoutUserUseCase  # Add this import
)
from src.infrastructure.web.dto.user_dto import UserCreate, UserResponse, Token, LogoutResponse  # Add LogoutResponse
from src.infrastructure.web.dependencies import (
    get_all_users_use_case,
    get_user_by_id_use_case,
    get_create_user_use_case,
    get_authenticate_user_use_case,
    get_current_active_user,
    get_logout_user_use_case  # Add this import
)

# Add endpoint
@router.post("/auth/logout", response_model=LogoutResponse)
async def logout(
    current_user: dict = Depends(get_current_active_user),
    logout_use_case: LogoutUserUseCase = Depends(get_logout_user_use_case)
):
    """Logout user and invalidate session."""
    try:
        success = await logout_use_case.execute(current_user["id"])
        return LogoutResponse(
            message="Successfully logged out",
            success=success
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )
```

## 4. Security Considerations

### Current Security Model
- **Stateless JWT tokens** with client-side storage
- **Short expiration times** (30 minutes) limit exposure
- **HTTPS enforcement** recommended for production

### Logout Security
- **Server validates user** before confirming logout
- **Client responsible** for token removal
- **Token remains valid** until expiration (acceptable risk)
- **User confirmation** provided for successful logout

### Recommendations
1. **Frontend must clear token** from storage immediately
2. **Monitor token expiration** times in production
3. **Consider refresh tokens** for longer sessions if needed
4. **Implement rate limiting** on auth endpoints

## 5. Error Handling

### HTTP Status Codes
- **200 OK**: Successful logout
- **401 Unauthorized**: Invalid/expired token
- **404 Not Found**: User not found
- **500 Internal Server Error**: Unexpected errors

### Exception Mapping
- `UserNotFoundError` → 404 Not Found
- `JWTError` → 401 Unauthorized (handled by auth middleware)
- `Exception` → 500 Internal Server Error

## 6. Testing Strategy

### Unit Tests
- **Use case testing**: Verify business logic and error handling
- **Router testing**: HTTP status codes and response format
- **Dependency injection**: Verify proper wiring

### Integration Tests
- **Full logout flow**: From request to response
- **Authentication integration**: With protected endpoints
- **Error scenarios**: Invalid tokens, missing users

### Test Files to Create/Update
- `tests/unit/test_user_use_cases.py` - Add logout use case tests
- `tests/integration/test_auth_endpoints.py` - Add logout endpoint tests

## 7. Files to Modify

### Modified Files
1. `/backend/src/application/use_cases/user_use_cases.py`
   - Add `LogoutUserUseCase` class

2. `/backend/src/infrastructure/web/dependencies.py`
   - Add `get_logout_user_use_case` function
   - Update imports

3. `/backend/src/infrastructure/web/dto/user_dto.py`
   - Add `LogoutResponse` class

4. `/backend/src/infrastructure/web/routers/users.py`
   - Add logout endpoint
   - Update imports

### No New Files Required
- Leverages existing infrastructure
- Follows established patterns
- Maintains architectural consistency

## 8. Alternative Approaches Considered

### Token Blacklisting Approach (Rejected)
**Would require:**
- New `TokenRepositoryPort` interface
- `MongoDBTokenRepository` implementation
- `BlacklistTokenUseCase` use case
- Database storage for revoked tokens
- Performance overhead for validation
- Token cleanup mechanism

**Rejection reasons:**
- Adds significant complexity
- Violates stateless JWT principle
- Minimal security benefit with 30-minute expiration
- Performance impact on all authenticated requests

### Database Session Tracking (Rejected)
**Would require:**
- User session storage
- Session-based authentication
- Complex state management
- Database dependency for all requests

**Rejection reasons:**
- Major architectural change
- Incompatible with current JWT approach
- Increases system complexity

## 9. Implementation Order

1. **Add use case** to `user_use_cases.py`
2. **Add DTO** to `user_dto.py`
3. **Add dependency** to `dependencies.py`
4. **Add endpoint** to `users.py` router
5. **Test implementation** manually
6. **Add unit tests** for use case
7. **Add integration tests** for endpoint

## 10. Compatibility Notes

### Backward Compatibility
- **No breaking changes** to existing endpoints
- **Existing tokens remain valid** until expiration
- **Frontend can handle both** 200 OK and error responses

### Frontend Integration
- Endpoint matches expected `/api/v1/auth/logout` URL
- Returns structured JSON response
- Provides clear success/error messaging
- Compatible with existing error handling

## 11. Production Considerations

### Monitoring
- **Log logout events** for security auditing
- **Monitor logout failure rates**
- **Track token usage patterns**

### Performance
- **Minimal overhead** with current approach
- **No database writes** for logout operation
- **Fast response times** expected

### Scalability
- **Stateless design** supports horizontal scaling
- **No shared state** between server instances
- **CDN-friendly** response format

## Summary

This implementation provides a clean, secure logout endpoint that:
- **Follows hexagonal architecture** principles
- **Maintains consistency** with existing patterns
- **Provides appropriate security** for the current JWT model
- **Minimizes complexity** while meeting requirements
- **Enables proper frontend integration**

The approach prioritizes simplicity and maintainability while providing the necessary functionality for user logout in a stateless JWT authentication system.