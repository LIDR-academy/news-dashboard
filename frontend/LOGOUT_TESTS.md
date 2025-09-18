# Logout Functionality Test Suite

This document provides comprehensive test coverage for the logout functionality implemented in the React frontend application.

## Overview

The logout functionality consists of two main components:
1. **DashboardHeader Component** - UI component with logout button
2. **useLogoutMutation Hook** - React Query mutation for logout operations

## Test Coverage

### 1. useLogoutMutation Hook Tests
**Location:** `/src/features/auth/hooks/__tests__/mutations/useLogout.mutation.test.tsx`

#### Test Categories:

**Hook Structure (3 tests)**
- Validates correct return interface with `{action, isLoading, error, isSuccess}`
- Ensures proper default states initialization
- Confirms `mutateAsync` usage for promise-based logout action

**Successful Logout (5 tests)**
- Tests backend service call and query cache clearing
- Validates loading state management during mutations
- Confirms success state updates after completion
- Verifies onSuccess callback execution

**Error Handling (5 tests)**
- Tests graceful fallback when backend logout fails (cache still cleared)
- Handles 401, 404, 408, and 500 HTTP error responses
- Manages network errors and timeouts
- Ensures local security (cache clearing) over backend reliability

**Query Cache Integration (4 tests)**
- Verifies cache clearing after successful logout
- Ensures cache clearing even when backend fails (security priority)
- Tests compatibility with new queries after logout
- Handles active queries during logout process

**Multiple Calls (3 tests)**
- Sequential logout attempts handling
- Concurrent logout calls management
- Mixed success/failure scenarios

**Implementation Details (4 tests)**
- Confirms `mutateAsync` usage for promise returns
- Tests React Query mutation state access
- Validates stable function instances across re-renders
- Verifies correct interface property exports

**Edge Cases (4 tests)**
- Query client availability handling
- Backend failure prioritization vs local security
- Malformed response handling
- Side effects prevention during failures

### 2. DashboardHeader Component Tests
**Location:** `/src/components/__tests__/DashboardHeader.test.tsx`

#### Test Categories:

**Component Rendering (5 tests)**
- Required title prop rendering with gradient styling
- Optional subtitle conditional rendering
- Logout button presence and styling

**User Email Display (4 tests)**
- Email display when available
- Conditional rendering based on email presence
- Proper styling for email section

**Logout Button Behavior (3 tests)**
- Click handler execution
- Multiple rapid clicks handling
- Async logout function support

**Loading States (4 tests)**
- Loading text display during logout process
- Button disabled state during loading
- Loading state transitions

**Button Styling and Variants (2 tests)**
- Correct button variant application
- Icon inclusion and styling

**Layout and Positioning (2 tests)**
- Header layout structure
- Title and controls positioning

**Accessibility (5 tests)**
- Semantic HTML structure (header, heading, button)
- Keyboard navigation support (Tab, Enter, Space)
- Screen reader accessibility
- Focus management during loading states

**Responsive Design (3 tests)**
- Flexible container layout
- Long email address handling
- Long title text handling

**Error Scenarios (3 tests)**
- Logout function error handling
- Missing auth context graceful handling
- Undefined auth context values

**Component Props (4 tests)**
- Dynamic title updates
- Special character handling in titles
- Empty title graceful handling
- Subtitle change handling

**Integration with Auth Context (2 tests)**
- Real-time auth state changes
- User email updates

## Test Statistics

- **Total Tests:** 65
- **useLogoutMutation Tests:** 28
- **DashboardHeader Tests:** 37
- **Coverage:** Comprehensive coverage of all user interactions, state changes, error scenarios, and edge cases

## Running Tests

### Run All Logout Tests
```bash
npm test -- --run src/features/auth/hooks/__tests__/mutations/useLogout.mutation.test.tsx src/components/__tests__/DashboardHeader.test.tsx
```

### Run Individual Test Suites

**Logout Mutation Tests:**
```bash
npm test -- --run src/features/auth/hooks/__tests__/mutations/useLogout.mutation.test.tsx
```

**Dashboard Header Tests:**
```bash
npm test -- --run src/components/__tests__/DashboardHeader.test.tsx
```

### Watch Mode for Development
```bash
npm test src/features/auth/hooks/__tests__/mutations/useLogout.mutation.test.tsx
npm test src/components/__tests__/DashboardHeader.test.tsx
```

## Test Dependencies

### Testing Libraries
- **Vitest** - Test runner and framework
- **React Testing Library** - Component testing utilities
- **@testing-library/user-event** - User interaction simulation
- **@testing-library/react-hooks** - Hook testing (renderHook)

### Mocking Strategy
- **Module-level mocking** for auth service and Lucide React icons
- **Context mocking** for useAuthContext hook
- **Query client mocking** for React Query testing
- **Console error suppression** for error scenario testing

## Key Testing Patterns

### 1. Component Testing
- Uses `render()` from React Testing Library
- User interactions with `userEvent.setup()`
- Accessibility-focused queries (`getByRole`, `getByLabelText`)
- Wait patterns for async operations

### 2. Hook Testing
- Uses `renderHook()` with proper provider wrappers
- React Query integration with test query client
- Async testing with `waitFor()` and `expect().resolves/rejects`

### 3. Error Handling
- Graceful fallback testing (logout continues even if backend fails)
- Unhandled rejection prevention
- Console error management during tests

### 4. Accessibility Testing
- Semantic HTML validation
- Keyboard navigation testing
- Screen reader compatibility
- Focus management during state changes

## Implementation Notes

### Security-First Approach
The logout mutation prioritizes local security over backend reliability:
- Cache is always cleared, even if backend logout fails
- Local authentication state is reset regardless of network issues
- Error logging for debugging while maintaining user security

### User Experience Focus
- Loading states provide clear feedback
- Accessible button states and labels
- Responsive design handling for various content lengths
- Graceful error handling without UI crashes

### Testing Philosophy
Tests follow the Testing Trophy approach:
- Integration tests over unit tests where possible
- User behavior validation over implementation details
- Real-world scenario coverage including error cases
- Accessibility and responsive design validation

## Maintenance

When modifying logout functionality:
1. Update corresponding tests for any interface changes
2. Add new test cases for new error scenarios
3. Verify accessibility requirements are maintained
4. Test both success and failure paths
5. Ensure mock configurations match real implementations

The test suite is designed to catch regressions and ensure the logout functionality remains reliable and secure across all supported user scenarios.