# Frontend Implementation Plan: Logout Button for Dashboard Header

## Overview
This document provides a detailed implementation plan for adding a logout button to the dashboard header and fixing the logout mutation to properly call the backend service. The implementation follows the project's feature-based architecture and uses existing auth context patterns.

## Current State Analysis

### Existing Auth Structure
- **Auth Context** (`/frontend/src/features/auth/hooks/useAuthContext.tsx`): Contains complete logout logic that clears state and storage
- **Auth Service** (`/frontend/src/features/auth/data/auth.service.ts`): Has logout function that calls `/api/v1/auth/logout`
- **Current Logout Mutation** (`/frontend/src/features/auth/hooks/mutations/useLogout.mutation.ts`): Only clears query cache, doesn't call backend service
- **Dashboard** (`/frontend/src/pages/home.page.tsx`): Simple header without logout functionality

### Issues Identified
1. Logout mutation doesn't call the auth service backend endpoint
2. Dashboard header lacks logout button UI
3. No user indication in the header (email display)

## Implementation Plan

### 1. Update Logout Mutation Hook

**File**: `/frontend/src/features/auth/hooks/mutations/useLogout.mutation.ts`

**Changes Required**:
- Import `authService` from the auth service
- Update mutation function to call `authService.logout()`
- Handle both success and error states
- Maintain cache clearing functionality
- Follow project's mutation pattern returning `{action, isLoading, error, isSuccess}`

**Implementation Details**:
```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { authService } from "../../data/auth.service";

export const useLogoutMutation = () => {
  const queryClient = useQueryClient();

  const logoutMutation = useMutation({
    mutationFn: async () => {
      // Call backend logout endpoint first
      await authService.logout();
    },
    onSuccess: () => {
      // Clear query cache after successful backend logout
      queryClient.clear();
    },
    onError: (error) => {
      // Still clear cache even if backend call fails
      // This ensures user is logged out locally
      queryClient.clear();
      console.error('Logout error:', error);
    }
  });

  return {
    action: logoutMutation.mutateAsync,
    isLoading: logoutMutation.isPending,
    error: logoutMutation.error,
    isSuccess: logoutMutation.isSuccess
  };
};
```

**Why This Approach**:
- Follows the project's established mutation pattern
- Calls backend service first for proper token invalidation
- Falls back to local cleanup if backend fails
- Maintains React Query cache management
- Compatible with existing auth context usage

### 2. Create Dashboard Header Component

**File**: `/frontend/src/components/DashboardHeader.tsx` (New Component)

**Component Structure**:
```typescript
import { useAuthContext } from '@/features/auth/hooks/useAuthContext';
import { Button } from '@/components/ui/button';
import { LogOut, User } from 'lucide-react';

interface DashboardHeaderProps {
  title: string;
  subtitle?: string;
}

export const DashboardHeader = ({ title, subtitle }: DashboardHeaderProps) => {
  const { logout, userEmail, isLoading } = useAuthContext();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="mb-8 flex items-center justify-between">
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          {title}
        </h1>
        {subtitle && (
          <p className="text-muted-foreground mt-2">
            {subtitle}
          </p>
        )}
      </div>

      <div className="flex items-center gap-3">
        {/* User Email Display */}
        {userEmail && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <User className="h-4 w-4" />
            <span>{userEmail}</span>
          </div>
        )}

        {/* Logout Button */}
        <Button
          variant="outline"
          size="sm"
          onClick={handleLogout}
          disabled={isLoading}
          className="flex items-center gap-2"
        >
          <LogOut className="h-4 w-4" />
          {isLoading ? 'Logging out...' : 'Logout'}
        </Button>
      </div>
    </header>
  );
};
```

**Design Decisions**:
- **Reusable Component**: Can be used across different dashboard pages
- **User Context Integration**: Shows current user email from auth context
- **Loading State**: Handles logout loading state with disabled button
- **Icon Usage**: Uses Lucide React icons (LogOut, User) already available
- **Styling**: Follows existing button variants and color scheme
- **Accessibility**: Proper button states and loading indicators

### 3. Update Dashboard Page

**File**: `/frontend/src/pages/home.page.tsx`

**Changes Required**:
- Import new `DashboardHeader` component
- Replace existing header with new component
- Pass title and subtitle as props

**Updated Implementation**:
```typescript
import { ProtectedRoute } from '@/core/components/ProtectedRoute'
import { NewsProvider } from '@/features/news/hooks/useNewsContext'
import { NewsBoard } from '@/features/news/components/NewsBoard'
import { DashboardHeader } from '@/components/DashboardHeader'

const HomePage = () => {
  return (
    <ProtectedRoute>
      <NewsProvider>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-50">
          <div className="container mx-auto px-4 py-8">
            <DashboardHeader
              title="News Dashboard"
              subtitle="Manage your reading list with our Kanban-style board"
            />

            <NewsBoard />
          </div>
        </div>
      </NewsProvider>
    </ProtectedRoute>
  )
}

export default HomePage
```

## Technical Implementation Details

### Error Handling Strategy
1. **Backend Call Fails**: Still proceed with local logout to ensure user isn't stuck
2. **Network Issues**: Local storage and state are cleared regardless
3. **User Feedback**: Loading states and error handling through existing toast system in auth context

### State Management Flow
1. User clicks logout button → Button shows loading state
2. `handleLogout` calls `useAuthContext.logout()`
3. Auth context calls updated logout mutation
4. Mutation calls backend service → Clears local state → Clears query cache
5. Auth context redirects to login (existing behavior)

### Styling and Theme Compliance
- **Colors**: Uses CSS variables defined in `index.css` (muted-foreground, primary, etc.)
- **Button Variants**: Uses existing button component with `outline` variant for header
- **Typography**: Maintains existing gradient text for title
- **Spacing**: Follows TailwindCSS spacing patterns used in project
- **Icons**: Uses Lucide React icons with consistent sizing (h-4 w-4)

### Responsive Design Considerations
- **Desktop**: Header with email and logout button side by side
- **Mobile**: Could be enhanced later with responsive behavior (hiding email on small screens)
- **Current**: Focuses on desktop-first approach as per existing design patterns

## Files to Create/Modify

### New Files
1. `/frontend/src/components/DashboardHeader.tsx` - Reusable header component

### Modified Files
1. `/frontend/src/features/auth/hooks/mutations/useLogout.mutation.ts` - Fix backend service call
2. `/frontend/src/pages/home.page.tsx` - Use new header component

## Testing Considerations

### Unit Tests Needed
1. **DashboardHeader Component**:
   - Renders user email when available
   - Calls logout function when button clicked
   - Shows loading state during logout
   - Handles missing userEmail gracefully

2. **Updated Logout Mutation**:
   - Calls authService.logout()
   - Clears query cache on success
   - Handles backend errors gracefully
   - Returns correct mutation interface

### Integration Tests
1. **Full Logout Flow**:
   - Click logout button → Backend call → Local cleanup → Redirect
   - Error scenarios (network failure, backend error)
   - Loading states during logout process

## Implementation Order

1. **First**: Update logout mutation to call backend service
2. **Second**: Create DashboardHeader component
3. **Third**: Update dashboard page to use new header
4. **Fourth**: Test complete logout flow
5. **Fifth**: Add unit tests for new components

## Dependencies
- No new dependencies required
- Uses existing:
  - `@radix-ui/react-*` components
  - `lucide-react` for icons
  - `class-variance-authority` for button variants
  - Existing auth context and service layer

## Security Considerations
- Backend logout call ensures server-side session cleanup
- Local storage clearing prevents client-side session persistence
- Query cache clearing removes any cached user data
- Graceful fallback ensures user can always log out locally

This implementation maintains consistency with the project's architecture while providing a clean, accessible, and secure logout experience.