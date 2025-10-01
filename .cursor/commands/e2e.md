# E2E Testing Command

**Description**: Run E2E tests with Playwright MCP using the qa-criteria-validator agent

**Usage**: Use `/e2e` command followed by optional test type

## Command Options

- `/e2e` - Interactive mode (choose what to test)
- `/e2e full` - Run complete E2E test suite
- `/e2e login` - Test login functionality specifically
- `/e2e logout` - Test logout functionality specifically
- `/e2e profile` - Test profile management functionality
- `/e2e auth` - Test all authentication flows
- `/e2e dashboard` - Test dashboard functionality
- `/e2e [feature]` - Test specific feature by name

## Implementation

When this command is invoked, Claude should:

1. **Check Application Status**
   - Verify frontend server is running on http://localhost:5173
   - Verify backend server is running on http://localhost:8000
   - Alert user if servers need to be started

2. **Launch qa-criteria-validator Agent**
   - Use the Task tool with subagent_type: "qa-criteria-validator"
   - Pass appropriate test prompt based on command argument

3. **Test Prompts by Type**

### Full Test Suite (`/e2e full`)
```
Please run comprehensive E2E tests for the entire React FastAPI application using Playwright.

Test the following key areas:
1. User authentication (login/logout)
2. Dashboard functionality and navigation
3. Profile management (view/edit/password change)
4. Protected route access
5. Error handling and edge cases
6. User session management

Application details:
- Frontend: React app on http://localhost:5173
- Backend: FastAPI on http://localhost:8000
- Authentication: OAuth2 with JWT tokens

Please start both servers if needed and provide a comprehensive test report.
```

### Logout Testing (`/e2e logout`)
```
Please test the logout functionality thoroughly using Playwright.

Focus on:
1. Logout button accessibility from dashboard
2. Backend logout endpoint call (POST /api/v1/auth/logout)
3. Token clearing from localStorage/sessionStorage
4. Redirection to login page
5. Protected route access prevention after logout
6. Error handling scenarios

Application details:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Key components: DashboardHeader, useLogout mutation, useAuthContext

Provide detailed test results and any issues found.
```

### Login Testing (`/e2e login`)
```
Please test the login functionality comprehensively using Playwright.

Test scenarios:
1. Valid credential login
2. Invalid credential handling
3. Form validation
4. Token storage and session management
5. Redirection to dashboard after login
6. Protected route access after login
7. Remember me functionality (if applicable)

Application details:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Login endpoint: POST /api/v1/auth/login

Provide comprehensive test results and security validation.
```

### Authentication Flows (`/e2e auth`)
```
Please run comprehensive authentication flow tests using Playwright.

Test the complete authentication cycle:
1. User registration (if available)
2. Login with various scenarios
3. Protected route access
4. Session management
5. Logout functionality
6. Token refresh (if applicable)
7. Security edge cases

Application details:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Authentication: OAuth2 with JWT

Provide detailed security assessment and functionality report.
```

### Profile Management (`/e2e profile`)
```
Please test the profile management functionality using Playwright.

Test areas:
1. Profile view and data display
2. Profile editing functionality
3. Password change feature
4. Form validation
5. Error handling
6. Data persistence
7. Navigation and user experience

Application details:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Profile routes and components

Provide detailed test results for all profile features.
```

### Dashboard Testing (`/e2e dashboard`)
```
Please test the dashboard functionality using Playwright.

Test scenarios:
1. Dashboard loading and display
2. Navigation elements
3. User information display
4. Interactive elements
5. Responsive design
6. Header functionality
7. Menu and routing

Application details:
- Frontend: http://localhost:5173
- Dashboard components and navigation

Provide comprehensive dashboard functionality report.
```

### Custom Feature Testing (`/e2e [feature]`)
```
Please test the "{feature}" functionality using Playwright.

Focus on comprehensive testing of this specific feature including:
1. Core functionality
2. User interactions
3. Form validation and data handling
4. Error scenarios
5. Navigation and routing
6. Integration with backend APIs
7. User experience and accessibility

Application details:
- Frontend: React app on http://localhost:5173
- Backend: FastAPI on http://localhost:8000

Please provide detailed test results for the "{feature}" feature.
```

### Interactive Mode (`/e2e`)
When no argument is provided, Claude should ask the user to choose from:
1. Full application test suite
2. Login functionality
3. Logout functionality
4. Profile management
5. Authentication flows
6. Dashboard functionality
7. Custom feature (user specifies)

## Example Usage in Claude Code

**User types**: `/e2e logout`

**Claude should respond**:
"I'll run E2E tests for the logout functionality using Playwright. Let me launch the qa-criteria-validator agent to test this thoroughly."

Then execute:
```
Task tool with:
- subagent_type: "qa-criteria-validator"
- description: "Test logout functionality with Playwright"
- prompt: [logout testing prompt from above]
```

## Prerequisites

- Frontend server running on http://localhost:5173
- Backend server running on http://localhost:8000
- qa-criteria-validator agent has access to Playwright tools
- Test user credentials available for authentication

## Notes

- Always check server status before testing
- Provide clear feedback about what's being tested
- Include server startup instructions if servers aren't running
- Generate comprehensive test reports
- Handle edge cases and error scenarios