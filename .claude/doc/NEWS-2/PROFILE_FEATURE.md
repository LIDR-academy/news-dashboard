# User Profile Feature Documentation

## Overview

The User Profile feature allows authenticated users to view and manage their personal information, including username, email, and password management.

## Features

### 1. Profile View (`/profile`)
- Display user information (username, email, account status, creation date, last updated)
- Navigation to edit profile and change password
- Responsive design for mobile and desktop

### 2. Profile Edit (`/profile/edit`)
- Edit username and email address
- Form validation for data integrity
- Real-time error handling and success feedback
- Optimistic updates for better UX

### 3. Change Password (`/profile/change-password`)
- Change password with current password verification
- Password strength validation
- Password visibility toggle
- Secure password confirmation

## Backend Implementation

### New Use Cases
- `UpdateUserUseCase`: Updates user profile information
- `ChangePasswordUseCase`: Changes user password with verification

### New Endpoints
- `PUT /api/v1/users/me`: Update user profile
- `PUT /api/v1/users/me/password`: Change user password

### Repository Updates
- Added `update_user()` method for profile updates
- Added `update_user_password()` method for password changes
- Added alias methods for consistency

### DTOs
- `UserUpdate`: For profile updates
- `ChangePasswordRequest`: For password changes

## Frontend Implementation

### Feature Structure
```
src/features/profile/
├── components/
│   ├── ProfileView.tsx
│   ├── ProfileEdit.tsx
│   └── ChangePassword.tsx
├── hooks/
│   ├── useProfile.ts
│   ├── useUpdateProfile.ts
│   └── useChangePassword.ts
├── data/
│   ├── profile.schema.ts
│   └── profile.service.ts
└── index.ts
```

### Components
- **ProfileView**: Displays user information with navigation and back button
- **ProfileEdit**: Form for editing profile information with back button
- **ChangePassword**: Form for changing password with back button
- **BackButton**: Reusable back navigation component

### Hooks
- **useProfile**: Fetches user profile data
- **useUpdateProfile**: Updates profile information
- **useChangePassword**: Changes user password

### Services
- **profileService**: API calls for profile operations

## Security Features

- All endpoints require authentication
- Password changes require current password verification
- Email and username uniqueness validation
- Input sanitization and validation
- CSRF protection

## Validation Rules

### Username
- 3-50 characters
- Alphanumeric and underscores only
- Must be unique

### Email
- Valid email format
- Must be unique

### Password
- Minimum 6 characters
- Must be different from current password
- Confirmation must match

## Testing

### Backend Tests
- Unit tests for use cases
- Integration tests for endpoints
- Repository tests for new methods
- Validation tests for all fields

### Frontend Tests
- Component tests for all profile components
- Hook tests for custom hooks
- Integration tests for user flows
- Accessibility tests

## Navigation

The profile feature is accessible from:
- Dashboard header "Profile" button
- Direct navigation to `/profile`
- Back button navigation within profile sections
- Reusable BackButton component for consistent navigation

### BackButton Component

A reusable navigation component with the following features:
- **Default behavior**: Navigates back in browser history
- **Custom URL**: Navigate to specific route with `to` prop
- **Custom action**: Execute custom function with `onBack` prop
- **Customizable**: Variant, size, text, and icon options
- **Consistent styling**: Matches design system

## Error Handling

- Form validation with real-time feedback
- API error handling with user-friendly messages
- Loading states for better UX
- Optimistic updates with rollback on failure

## Performance

- Profile page loads within 2 seconds
- Form submissions complete within 3 seconds
- Optimistic updates for immediate feedback
- Proper caching with React Query

## Accessibility

- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- High contrast support
- Focus management

## Future Enhancements

- Profile picture upload
- Two-factor authentication
- Account deletion
- Privacy settings
- Activity history
