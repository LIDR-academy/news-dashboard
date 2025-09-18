# Logout API Documentation

## Overview
The logout endpoint provides secure user logout functionality for the React-FastAPI application, following the hexagonal architecture pattern.

## Endpoint Details

### POST /api/v1/auth/logout

**Description**: Securely logs out an authenticated user by validating the user exists and returning a success confirmation.

**Authentication**: Required (Bearer JWT token)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**: None required

**Response Model**: `LogoutResponse`

**Success Response (200 OK)**:
```json
{
  "message": "Successfully logged out",
  "success": true
}
```

**Error Responses**:

**401 Unauthorized** - Missing or invalid authentication token:
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** - User not found in database:
```json
{
  "detail": "User not found"
}
```

**500 Internal Server Error** - Server-side errors:
```json
{
  "detail": "Internal server error"
}
```

## Architecture Implementation

### Backend Components

**Use Case**: `LogoutUserUseCase`
- Location: `src/application/use_cases/user_use_cases.py`
- Purpose: Validates user exists before confirming logout
- Pattern: Constructor injection + single execute method
- Returns: Boolean success status

**DTO**: `LogoutResponse`
- Location: `src/infrastructure/web/dto/user_dto.py`
- Purpose: Structured response with message and success flag
- Validation: Pydantic model with field validation

**Router**: Logout endpoint
- Location: `src/infrastructure/web/routers/users.py`
- Dependencies: Authentication, dependency injection
- Error handling: Maps domain exceptions to HTTP status codes

### Security Considerations

**Stateless JWT Approach**:
- No server-side token blacklisting (by design)
- 30-minute token expiration limits security risk
- Client-side token removal handled by frontend
- User validation ensures legitimate logout requests

**Authentication Flow**:
1. Client sends authenticated request with JWT token
2. Backend validates token and extracts user information
3. Use case validates user exists in database
4. Returns success confirmation
5. Frontend clears local storage and cache

## Frontend Integration

**Service Call**: `authService.logout()`
- Makes HTTP POST request to logout endpoint
- Handles authentication headers automatically
- Returns promise for success/error handling

**Mutation Hook**: `useLogoutMutation`
- Calls backend service before clearing local cache
- Provides loading states and error handling
- Graceful fallback: clears cache even if backend fails

**Component Integration**: `DashboardHeader`
- Uses auth context for logout functionality
- Displays loading states during logout process
- Handles user feedback and error scenarios

## Testing Coverage

**Backend Tests**: 40 comprehensive tests
- Unit tests for LogoutUserUseCase (11 tests)
- Integration tests for logout endpoint (9 tests)
- DTO validation tests (18 tests)
- Error scenario coverage (various edge cases)

**Frontend Tests**: 65 comprehensive tests
- Logout mutation tests (28 tests)
- DashboardHeader component tests (37 tests)
- User interaction and accessibility testing
- Error handling and loading state validation

## Example Usage

**Frontend Implementation**:
```typescript
// Using the logout mutation
const { action: logout, isLoading, error } = useLogoutMutation();

const handleLogout = async () => {
  try {
    await logout();
    // Success: user redirected to login page
  } catch (error) {
    // Error: graceful fallback, cache still cleared
    console.error('Logout error:', error);
  }
};
```

**curl Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

## Performance Characteristics

- **Response Time**: < 100ms typical
- **Database Operations**: Single user lookup query
- **Memory Usage**: Minimal (stateless operation)
- **Scalability**: Horizontal scaling compatible

## Monitoring and Observability

**Logging**: Structured logging with Logfire
- Request/response logging
- Error tracking and alerting
- Performance metrics collection

**Health Checks**: Endpoint availability monitoring
**Error Tracking**: Comprehensive error scenario coverage
**Metrics**: Success rate, response time, error distribution