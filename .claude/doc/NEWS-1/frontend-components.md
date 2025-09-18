# Frontend Components Documentation

## DashboardHeader Component

### Overview
The `DashboardHeader` component is a reusable header component designed for dashboard pages, featuring title display, optional subtitle, user email display, and logout functionality.

### Location
`/frontend/src/components/DashboardHeader.tsx`

### Props Interface
```typescript
interface DashboardHeaderProps {
  title: string;           // Required: Main dashboard title
  subtitle?: string;       // Optional: Additional description text
}
```

### Features
- **Responsive Design**: Flexible layout that adapts to different screen sizes
- **User Information Display**: Shows authenticated user's email with user icon
- **Logout Functionality**: Integrated logout button with loading states
- **Gradient Styling**: Modern gradient text styling for titles
- **Accessibility**: Full keyboard navigation and screen reader support

### Usage Example
```typescript
import { DashboardHeader } from '@/components/DashboardHeader';

function DashboardPage() {
  return (
    <div>
      <DashboardHeader
        title="Analytics Dashboard"
        subtitle="View your performance metrics and insights"
      />
      {/* Rest of dashboard content */}
    </div>
  );
}
```

### Visual Structure
```
┌─────────────────────────────────────────────────────────────┐
│ [Title with gradient styling]          [Email] [Logout Btn] │
│ [Optional subtitle]                                         │
└─────────────────────────────────────────────────────────────┘
```

### Dependencies
- **React Context**: `useAuthContext` for authentication state
- **UI Components**: Radix UI Button component
- **Icons**: Lucide React (User, LogOut icons)
- **Styling**: TailwindCSS classes

### Authentication Integration
The component integrates with the authentication system through:
- `useAuthContext()` hook for user state and logout functionality
- Conditional rendering based on user authentication status
- Loading state management during logout process

### Styling Classes
- **Header Container**: `mb-8 flex items-center justify-between`
- **Title**: `text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent`
- **Subtitle**: `text-muted-foreground mt-2`
- **User Email**: `flex items-center gap-2 text-sm text-muted-foreground`
- **Controls Container**: `flex items-center gap-3`

### Accessibility Features
- **Semantic HTML**: Uses proper `<header>`, `<h1>`, and `<button>` elements
- **Keyboard Navigation**: Full keyboard support with tab navigation
- **Screen Reader Support**: Accessible button labels and proper heading hierarchy
- **Focus Management**: Proper focus states and disabled states during loading

### States
1. **Default State**: Title, optional subtitle, user email, and logout button
2. **Loading State**: Logout button shows "Logging out..." and is disabled
3. **No User State**: Only title and subtitle displayed (email section hidden)

## useLogout Mutation Hook

### Overview
Enhanced mutation hook that handles the complete logout flow, including backend API call followed by cache clearing.

### Location
`/frontend/src/features/auth/hooks/mutations/useLogout.mutation.ts`

### Return Interface
```typescript
interface LogoutMutationReturn {
  action: () => Promise<void>;     // Async logout function
  isLoading: boolean;              // Loading state indicator
  error: Error | null;             // Error state
  isSuccess: boolean;              // Success state indicator
}
```

### Features
- **Backend Integration**: Calls `authService.logout()` before local cleanup
- **Error Handling**: Graceful fallback - always clears cache even if backend fails
- **React Query Integration**: Proper mutation state management
- **Security-First Approach**: Prioritizes local cleanup for security

### Implementation Details
```typescript
export const useLogoutMutation = () => {
  const queryClient = useQueryClient();

  const logoutMutation = useMutation({
    mutationFn: async () => {
      // Call backend logout endpoint
      await authService.logout();
    },
    onSuccess: () => {
      // Clear all cached data
      queryClient.clear();
    },
    onError: (error) => {
      // Security-first: clear cache even on error
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

### Error Scenarios Handled
- **Network Failures**: Internet connectivity issues
- **Backend Errors**: 401, 404, 500 HTTP status codes
- **Service Unavailable**: Backend service downtime
- **Token Expiration**: Expired authentication tokens

### Testing Coverage
- **28 comprehensive tests** covering all aspects of the logout mutation
- Success scenarios with backend integration
- Error handling and graceful fallback testing
- Cache clearing verification
- Loading state transitions
- Rapid click protection

## Component Testing Strategy

### DashboardHeader Tests
- **37 comprehensive test methods** with React Testing Library
- Full coverage of user interactions and accessibility
- Responsive design and edge case testing
- Integration testing with auth context

### Test Categories
1. **Component Rendering**: Title, subtitle, button display
2. **User Email Display**: Conditional rendering and styling
3. **Logout Button Behavior**: Click handling and async operations
4. **Loading States**: Button disabled state and loading text
5. **Accessibility**: Keyboard navigation and screen readers
6. **Responsive Design**: Long text handling and flexible layouts
7. **Error Scenarios**: Network failures and missing context
8. **Integration Testing**: Auth context changes and real-time updates

### Best Practices
- **User-Centric Testing**: Tests behavior from user perspective
- **Accessibility-Focused**: Proper ARIA attributes testing
- **Error-Resilient**: Comprehensive error scenario coverage
- **Real-World Scenarios**: Edge cases and rapid user interactions

## Performance Considerations

### Optimization Features
- **Memoization**: Component optimized for re-render performance
- **Conditional Rendering**: Efficient DOM updates based on state
- **Event Handling**: Optimized onClick handlers
- **Icon Loading**: Efficient Lucide React icon rendering

### Bundle Impact
- **Minimal Dependencies**: Only essential imports
- **Tree Shaking**: Unused code eliminated in production builds
- **CSS-in-JS**: TailwindCSS for optimal stylesheet generation

## Migration Notes

### From Previous Implementation
- **Enhanced Logout**: Now calls backend service before cache clearing
- **Improved UX**: Better loading states and error handling
- **Component Reusability**: Extracted from page-specific implementation
- **Better Testing**: Comprehensive test coverage added

### Breaking Changes
- None - fully backward compatible with existing auth context
- New component is additive to existing functionality

## Future Enhancements

### Potential Improvements
- **Theme Toggle**: Dark/light mode toggle integration
- **Notifications**: User notification badge display
- **Profile Menu**: Expandable user profile dropdown
- **Breadcrumb Integration**: Navigation breadcrumb support
- **Search Integration**: Global search functionality