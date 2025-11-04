# NEWS-[XX]: Add Dark Mode Toggle to Profile Page

## Story Type
**Feature**

## Priority
**Medium**

## Story Points
**3**

---

## [ORIGINAL] User Story

As a user, I want to toggle between light and dark mode from my profile page, so that I can customize the interface appearance to my preference and reduce eye strain when using the application in low-light conditions.

---

## [ENHANCED] User Story

As a user, I want to toggle between light and dark mode from my profile page, so that I can customize the interface appearance to my preference and reduce eye strain when using the application in low-light conditions.

### Background Context

The application currently has dark mode styles configured but not activated:
- CSS variables for dark mode are defined in `frontend/src/index.css` (lines 122-154)
- Tailwind is configured with `darkMode: ['class']`
- UI components already include dark mode variants (e.g., `dark:bg-input/30`)
- `next-themes` package is installed but the ThemeProvider is not set up

This task will activate the existing dark mode infrastructure and add a user-facing toggle control.

---

## Detailed Description

### Functionality Overview

Implement a dark mode toggle switch in the Profile View page that allows users to switch between light and dark themes. The theme preference should:
1. Apply immediately when toggled
2. Persist across browser sessions
3. Respect system preferences as a default option
4. Provide visual feedback during the toggle action

### User Interface

**Location**: Profile View page (`/profile`)  
**Component Type**: Toggle switch with icons  
**Placement**: New settings section in the profile card, after account status and before action buttons

The toggle should display:
- Sun icon (☀️) for light mode
- Moon icon (🌙) for dark mode  
- Label: "Theme Preference"
- Description: "Choose your preferred color theme"

---

## Technical Implementation Details

### 1. Theme Provider Setup

**File**: `frontend/src/main.tsx`

**Changes Required**:
- Import `ThemeProvider` from `next-themes`
- Wrap the App component with ThemeProvider
- Configure with:
  - `attribute="class"` (to add/remove `dark` class on `<html>`)
  - `defaultTheme="system"` (respect OS preference by default)
  - `enableSystem={true}` (allow system theme detection)

**Code Example**:
```typescript
import { ThemeProvider } from 'next-themes'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
```

### 2. Theme Toggle Component

**File**: `frontend/src/core/components/ThemeToggle.tsx` (NEW)

**Purpose**: Reusable theme toggle component

**Requirements**:
- Use `useTheme` hook from `next-themes`
- Display current theme state
- Provide toggle functionality
- Include proper accessibility attributes
- Use Lucide React icons (Sun, Moon)
- Use shadcn/ui Switch component

**Exports**:
```typescript
export function ThemeToggle(): JSX.Element
```

**Props**: None (self-contained)

**Dependencies**:
- `next-themes` (useTheme hook)
- `@/components/ui/switch` (Switch component)
- `lucide-react` (Sun, Moon icons)

### 3. Profile View Integration

**File**: `frontend/src/features/profile/components/ProfileView.tsx`

**Changes Required**:
1. Import the new `ThemeToggle` component
2. Add a new settings section in the card content
3. Place the section after "Account Status" (line ~130) and before action buttons (line ~140)

**New Section Structure**:
```tsx
{/* Theme Settings */}
<div className="flex items-center justify-between p-4 border rounded-lg">
  <div className="flex items-center gap-3">
    <Settings className="h-5 w-5 text-gray-500" />
    <div>
      <div className="font-medium">Theme Preference</div>
      <div className="text-sm text-gray-600">Choose your preferred color theme</div>
    </div>
  </div>
  <ThemeToggle />
</div>
```

**Additional Imports**:
- `Settings` icon from `lucide-react`
- `ThemeToggle` from `@/core/components/ThemeToggle`

### 4. Files to Create/Modify

#### Files to Create:
1. **`frontend/src/core/components/ThemeToggle.tsx`**
   - New reusable theme toggle component
   - Exports: `ThemeToggle` component

#### Files to Modify:
1. **`frontend/src/main.tsx`**
   - Add ThemeProvider wrapper
   - Lines to modify: 1-10 (imports and render)

2. **`frontend/src/features/profile/components/ProfileView.tsx`**
   - Import ThemeToggle component
   - Add theme settings section
   - Lines to modify: 7 (imports), ~130 (add new section)

3. **`frontend/src/core/components/index.ts`** (if exists, or create)
   - Export ThemeToggle for easier imports

---

## API Requirements

**Backend Changes**: None required  
**Reason**: Theme preference is stored client-side in localStorage by `next-themes`

---

## Acceptance Criteria

### Functional Requirements

- [ ] **AC1**: Theme provider is properly configured in the application root
  - Verify `ThemeProvider` wraps the entire app
  - Verify `attribute="class"` is set
  - Verify `defaultTheme="system"` is configured

- [ ] **AC2**: Theme toggle appears in profile view page
  - Navigate to `/profile`
  - Verify toggle switch is visible
  - Verify proper labeling ("Theme Preference")
  - Verify icons are displayed correctly (Sun/Moon)

- [ ] **AC3**: Toggle switches between light and dark modes
  - Click the toggle in light mode
  - Verify the interface switches to dark mode
  - Verify the toggle icon updates (Sun → Moon)
  - Click the toggle again
  - Verify the interface switches back to light mode
  - Verify the toggle icon updates (Moon → Sun)

- [ ] **AC4**: Dark mode styles are applied correctly
  - In dark mode, verify:
    - Background color changes (lighter → darker)
    - Text color inverts for readability
    - All UI components render properly
    - Borders and shadows are visible
    - Cards have appropriate dark backgrounds

- [ ] **AC5**: Theme preference persists across sessions
  - Set theme to dark mode
  - Refresh the page
  - Verify dark mode remains active
  - Close and reopen the browser
  - Verify dark mode remains active

- [ ] **AC6**: System theme preference works as default
  - Clear localStorage for the site
  - Verify app matches OS theme preference
  - Change OS theme setting
  - Verify app updates automatically (if OS set to "auto")

### UI/UX Requirements

- [ ] **AC7**: Toggle is accessible and usable
  - Toggle can be activated via keyboard (Tab + Space/Enter)
  - Toggle has proper ARIA labels
  - Toggle provides visual feedback on interaction
  - Toggle is properly aligned within the settings section

- [ ] **AC8**: Transitions are smooth
  - Theme changes have smooth visual transitions
  - No flickering or flash of unstyled content
  - Icons transition smoothly

- [ ] **AC9**: Responsive design works in dark mode
  - Test on mobile viewport (375px)
  - Test on tablet viewport (768px)
  - Test on desktop viewport (1440px)
  - Verify all breakpoints work correctly in both themes

### Technical Requirements

- [ ] **AC10**: No console errors or warnings
  - Check browser console for errors during theme toggle
  - Verify no React hydration warnings
  - Verify no accessibility warnings

---

## Testing Requirements

### Unit Tests

**File**: `frontend/src/core/components/__tests__/ThemeToggle.test.tsx` (NEW)

**Test Cases**:
1. Renders toggle switch correctly
2. Displays correct icon based on current theme
3. Calls theme toggle function on click
4. Has proper accessibility attributes
5. Handles loading state before theme is initialized

**File**: `frontend/src/features/profile/__tests__/ProfileView.test.tsx` (MODIFY)

**Additional Test Cases**:
1. Profile view renders theme toggle section
2. Theme toggle is visible in settings area
3. Settings section has proper icons and labels

### Integration Tests

**Optional E2E Test** (using Playwright MCP if available):
1. Navigate to profile page
2. Verify initial theme state
3. Click theme toggle
4. Verify theme changes visually
5. Refresh page
6. Verify theme persists

### Manual Testing Checklist

- [ ] Test in Chrome
- [ ] Test in Firefox
- [ ] Test in Safari (if available)
- [ ] Test with system theme = light
- [ ] Test with system theme = dark
- [ ] Test localStorage persistence
- [ ] Test keyboard navigation
- [ ] Test screen reader announcements

---

## Non-Functional Requirements

### Performance
- Theme toggle should respond in < 100ms
- Theme transition should be smooth (no layout shift)
- No impact on initial page load time

### Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support (Tab, Space, Enter)
- Screen reader compatible
- Sufficient color contrast in both themes (4.5:1 minimum)
- Focus indicators visible in both themes

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Security
- No XSS vulnerabilities through theme switching
- localStorage access is properly scoped
- No sensitive data in theme preferences

---

## Dependencies

### Existing Packages (Already Installed)
- `next-themes` v0.4.6 - Theme management
- `lucide-react` v0.525.0 - Icons
- `@radix-ui/react-switch` v1.2.6 - Switch component

### No New Dependencies Required

---

## Documentation Updates

### Files to Update

1. **`frontend/README.md`**
   - Add section about theme support
   - Document how to use theme toggle
   - Add note about localStorage key used

2. **`README.md`** (root)
   - Add dark mode to features list
   - Update screenshots (optional, if they exist)

---

## Definition of Done

- [ ] Code implemented and follows project architecture patterns
- [ ] All acceptance criteria met
- [ ] Unit tests written and passing (coverage maintained at 80%+)
- [ ] No linting errors (`npm run lint` passes)
- [ ] No TypeScript errors (`tsc --noEmit` passes)
- [ ] Manual testing completed across browsers
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] PR created and linked to Jira ticket
- [ ] Feature tested in staging environment (if applicable)

---

## Estimated Effort

- **Development**: 2-3 hours
- **Testing**: 1 hour
- **Code Review**: 30 minutes
- **Total**: ~4 hours

---

## Related Tickets

- None (standalone feature)

---

## Notes

### Implementation Sequence
1. Create ThemeToggle component
2. Add ThemeProvider to main.tsx
3. Integrate toggle into ProfileView
4. Add unit tests
5. Update documentation
6. Manual testing and refinement

### Design Considerations
- The toggle uses the existing design system (shadcn/ui components)
- Dark mode colors are already defined in `index.css`
- No design mockups needed - follows existing profile page patterns

### Future Enhancements (Not in Scope)
- Per-user theme preference stored in backend
- Auto-schedule theme (dark at night, light during day)
- Custom theme colors
- Multiple theme options (not just light/dark)

---

## Labels
`frontend`, `ui`, `enhancement`, `profile`, `accessibility`, `ready-for-dev`

## Epic
User Experience Improvements

## Component
Profile Management

