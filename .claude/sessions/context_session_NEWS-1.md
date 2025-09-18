# Context Session: NEWS-1

## Initial Analysis
Starting work on Jira ticket NEWS-1. Need to get ticket details and understand the requirements.

## Phase 1: Planning
- Getting ticket details from Jira
- Will analyze the problem and create implementation plan
- Will consult relevant subagents based on the ticket requirements

## Todo List
1. Get Jira ticket NEWS-1 details ✅ (in progress)
2. Understand the problem described in the ticket
3. Search the codebase for relevant files
4. Implement necessary changes to solve the ticket
5. Write and run tests to verify the solution
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR

## Ticket Details
**Summary:** Add Logout Endpoint and Dashboard Logout Button
**Priority:** Medium
**Status:** To Do

**Description:**
The application currently has authentication functionality with login and register features, but lacks a proper logout endpoint on the backend and a logout button in the dashboard UI.

**Requirements:**

### Backend
- Add `POST /api/v1/auth/logout` endpoint in `/backend/src/infrastructure/web/routers/users.py`
- Follow hexagonal architecture patterns (use case → domain → infrastructure)
- Handle token invalidation/blacklisting if needed
- Return appropriate HTTP status codes

### Frontend
- Add logout button to dashboard header (`/frontend/src/pages/home.page.tsx`)
- Position button in top-right corner of the header
- Use existing `useAuthContext` hook for logout functionality
- Ensure logout redirects to login page
- Follow project's feature-based architecture and UI conventions

**Current State:**
- ✅ Frontend logout logic exists in `useAuthContext.tsx`
- ✅ Frontend auth service has logout function calling `/api/v1/auth/logout`
- ❌ Backend `/api/v1/auth/logout` endpoint is missing
- ❌ Dashboard lacks visible logout button

## Implementation Plan
This requires both backend and frontend work:

1. **Backend Implementation:**
   - Create logout use case following hexagonal architecture
   - Add logout endpoint to users router
   - Handle token invalidation

2. **Frontend Implementation:**
   - Add logout button to dashboard header
   - Use existing auth context and service

**Subagents needed:**
- backend-developer: For logout endpoint implementation
- frontend-developer: For dashboard UI changes
- backend-test-engineer: For backend testing
- frontend-test-engineer: For frontend testing

## Codebase Analysis
**Current Auth Structure:**

**Backend:**
- `/backend/src/infrastructure/web/routers/users.py` - Contains `/auth/register` and `/auth/login` endpoints
- Missing `/auth/logout` endpoint
- Uses JWT tokens with security module
- Follows hexagonal architecture with use cases

**Frontend:**
- `useAuthContext.tsx` - Has logout function that clears local storage and calls logout mutation
- `auth.service.ts` - Has logout function that calls `/api/v1/auth/logout` (404 currently)
- `useLogout.mutation.ts` - Only clears query cache, doesn't call backend service
- `home.page.tsx` - Dashboard without logout button

**Issues Found:**
1. Backend `/auth/logout` endpoint missing
2. Frontend logout mutation doesn't call the auth service
3. Dashboard header has no logout button

## Backend Architecture Analysis

### Current Authentication Structure
- **JWT-based authentication** using jose library with stateless tokens
- **30-minute token expiration** with no server-side tracking
- **Hexagonal architecture** with clear layer separation:
  - Domain: User entity with validation
  - Application: Use cases with dependency injection
  - Infrastructure: MongoDB repositories, FastAPI routers, DTOs

### Key Findings
1. **No token blacklisting mechanism** exists (by design for stateless JWT)
2. **Repository pattern** well-established with abstract ports
3. **Use case pattern** consistent: constructor injection + single execute method
4. **Dependency injection** uses @lru_cache() for optimization
5. **Error handling** maps domain exceptions to HTTP status codes

### Token Invalidation Decision
**Recommendation: Simple success response without blacklisting**
- Current stateless JWT architecture doesn't support server-side invalidation
- Short 30-minute expiration limits security risk
- Adding blacklisting would require significant architectural changes
- Frontend already handles token removal from local storage

### Implementation Strategy
1. **LogoutUserUseCase** - Validates user exists, returns success
2. **LogoutResponse DTO** - Structured response with message and success flag
3. **POST /auth/logout endpoint** - Follows existing router patterns
4. **No repository changes** needed (leverages existing UserRepository)

**Files to modify:**
- `user_use_cases.py` - Add LogoutUserUseCase
- `dependencies.py` - Add logout use case dependency
- `user_dto.py` - Add LogoutResponse DTO
- `users.py` router - Add logout endpoint

**Detailed implementation plan:** `.claude/doc/NEWS-1/backend.md`

## Frontend Implementation Plan

**Created**: Detailed implementation plan at `.claude/doc/NEWS-1/frontend.md`

**Key Frontend Requirements**:
1. Fix logout mutation to call backend service (authService.logout())
2. Create reusable DashboardHeader component with logout button
3. Update dashboard page to use new header component
4. Maintain existing auth context patterns and error handling

**Implementation Approach**:
- **Logout Mutation Fix**: Update to call authService.logout() before clearing cache
- **Header Component**: New reusable component with user email display and logout button
- **UI Design**: Top-right positioning, outline button variant, Lucide icons
- **Error Handling**: Graceful fallback to local logout if backend fails
- **State Management**: Uses existing useAuthContext hook

**Files to Create/Modify**:
- New: `/frontend/src/components/DashboardHeader.tsx`
- Modify: `/frontend/src/features/auth/hooks/mutations/useLogout.mutation.ts`
- Modify: `/frontend/src/pages/home.page.tsx`

**Design Decisions**:
- Reusable header component for consistency across dashboard pages
- User email display for better UX
- Loading states and error handling
- Follows project's button variants and color scheme
- Uses existing auth context without modifications

## Implementation Summary

### Backend Changes (✅ Completed)
1. **LogoutUserUseCase** added to `/backend/src/application/use_cases/user_use_cases.py`
   - Validates user exists before logout
   - Returns success confirmation for stateless JWT approach
2. **LogoutResponse DTO** added to `/backend/src/infrastructure/web/dto/user_dto.py`
   - Structured response with message and success flag
3. **Logout dependency** added to `/backend/src/infrastructure/web/dependencies.py`
   - Dependency injection for logout use case
4. **POST /auth/logout endpoint** added to `/backend/src/infrastructure/web/routers/users.py`
   - Requires authentication via current_user dependency
   - Returns 200 with success message or appropriate error codes

### Frontend Changes (✅ Completed)
1. **Fixed logout mutation** in `/frontend/src/features/auth/hooks/mutations/useLogout.mutation.ts`
   - Now calls `authService.logout()` before clearing cache
   - Graceful error handling with local fallback
   - Updated interface to match project conventions
2. **Created DashboardHeader component** at `/frontend/src/components/DashboardHeader.tsx`
   - Reusable header with user email display and logout button
   - Uses Lucide React icons and existing button variants
   - Loading states and responsive design
3. **Updated dashboard page** in `/frontend/src/pages/home.page.tsx`
   - Replaced static header with new DashboardHeader component
   - Maintains existing styling and layout

### Testing & Validation (✅ Completed)
- Backend imports compile successfully
- Frontend dependencies installed and no new lint errors introduced
- Python syntax validation passes for all modified files

### Files Modified
**Backend:**
- `src/application/use_cases/user_use_cases.py` - Added LogoutUserUseCase
- `src/infrastructure/web/dto/user_dto.py` - Added LogoutResponse DTO
- `src/infrastructure/web/dependencies.py` - Added logout dependency
- `src/infrastructure/web/routers/users.py` - Added logout endpoint

**Frontend:**
- `src/features/auth/hooks/mutations/useLogout.mutation.ts` - Fixed to call backend
- `src/components/DashboardHeader.tsx` - New reusable header component
- `src/pages/home.page.tsx` - Updated to use new header

## Subagent Consultations