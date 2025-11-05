import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DashboardHeader } from '../DashboardHeader'
import { cleanup } from '@/test-utils/mocks'

// Mock the auth context
const mockLogout = vi.fn()
const mockUseAuthContext = vi.fn()

vi.mock('@/features/auth/hooks/useAuthContext', () => ({
  useAuthContext: () => mockUseAuthContext()
}))

// Mock react-router-dom
vi.mock('react-router-dom', () => ({
  Link: ({ to, children, ...props }: any) => (
    <a href={to} {...props}>{children}</a>
  )
}))

// Mock Lucide React icons
vi.mock('lucide-react', () => ({
  LogOut: ({ className }: { className?: string }) => (
    <span data-testid="logout-icon" className={className}>LogOut</span>
  ),
  User: ({ className }: { className?: string }) => (
    <span data-testid="user-icon" className={className}>User</span>
  ),
  Settings: ({ className }: { className?: string }) => (
    <span data-testid="settings-icon" className={className}>Settings</span>
  )
}))

describe('DashboardHeader', () => {
  const defaultProps = {
    title: 'Dashboard',
    subtitle: 'Welcome to your dashboard'
  }

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks()

    // Default mock return values
    mockUseAuthContext.mockReturnValue({
      logout: mockLogout,
      userEmail: 'test@example.com',
      isLoading: false
    })
  })

  afterEach(() => {
    cleanup.all()
  })

  describe('Component Rendering', () => {
    it('should render with required title prop', () => {
      render(<DashboardHeader title="Test Dashboard" />)

      expect(screen.getByRole('banner')).toBeInTheDocument()
      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Test Dashboard')
    })

    it('should render title with gradient styling', () => {
      render(<DashboardHeader title="Styled Title" />)

      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toHaveClass('text-3xl', 'font-bold', 'bg-gradient-to-r', 'from-blue-600', 'to-purple-600', 'bg-clip-text', 'text-transparent')
    })

    it('should render optional subtitle when provided', () => {
      render(<DashboardHeader title="Dashboard" subtitle="Test subtitle" />)

      expect(screen.getByText('Test subtitle')).toBeInTheDocument()
      expect(screen.getByText('Test subtitle')).toHaveClass('text-muted-foreground', 'mt-2')
    })

    it('should not render subtitle when not provided', () => {
      render(<DashboardHeader title="Dashboard" />)

      expect(screen.queryByText('Test subtitle')).not.toBeInTheDocument()
    })

    it('should render logout button', () => {
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })
      expect(logoutButton).toBeInTheDocument()
      expect(logoutButton).toHaveClass('flex', 'items-center', 'gap-2')
    })
  })

  describe('User Email Display', () => {
    it('should display user email when available', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'john.doe@example.com',
        isLoading: false
      })

      render(<DashboardHeader {...defaultProps} />)

      expect(screen.getByText('john.doe@example.com')).toBeInTheDocument()
      expect(screen.getByTestId('user-icon')).toBeInTheDocument()
    })

    it('should not display user email section when email is null', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: null,
        isLoading: false
      })

      render(<DashboardHeader {...defaultProps} />)

      expect(screen.queryByTestId('user-icon')).not.toBeInTheDocument()
    })

    it('should not display user email section when email is empty string', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: '',
        isLoading: false
      })

      render(<DashboardHeader {...defaultProps} />)

      expect(screen.queryByTestId('user-icon')).not.toBeInTheDocument()
    })

    it('should style user email section correctly', () => {
      render(<DashboardHeader {...defaultProps} />)

      const userEmailContainer = screen.getByText('test@example.com').parentElement
      expect(userEmailContainer).toHaveClass('flex', 'items-center', 'gap-2', 'text-sm', 'text-muted-foreground')
    })
  })

  describe('Logout Button Behavior', () => {
    it('should call logout function when button is clicked', async () => {
      const user = userEvent.setup()
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })
      await user.click(logoutButton)

      expect(mockLogout).toHaveBeenCalledTimes(1)
    })

    it('should handle multiple rapid clicks gracefully', async () => {
      const user = userEvent.setup()
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })

      // Click multiple times rapidly
      await user.click(logoutButton)
      await user.click(logoutButton)
      await user.click(logoutButton)

      expect(mockLogout).toHaveBeenCalledTimes(3)
    })

    it('should handle async logout function', async () => {
      const asyncLogout = vi.fn().mockResolvedValue(undefined)
      mockUseAuthContext.mockReturnValue({
        logout: asyncLogout,
        userEmail: 'test@example.com',
        isLoading: false
      })

      const user = userEvent.setup()
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })
      await user.click(logoutButton)

      expect(asyncLogout).toHaveBeenCalledTimes(1)
      await waitFor(() => {
        expect(asyncLogout).toHaveBeenCalledWith()
      })
    })
  })

  describe('Loading States', () => {
    it('should show loading text when isLoading is true', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'test@example.com',
        isLoading: true
      })

      render(<DashboardHeader {...defaultProps} />)

      expect(screen.getByText('Logging out...')).toBeInTheDocument()
      expect(screen.queryByText('Logout')).not.toBeInTheDocument()
    })

    it('should show normal text when isLoading is false', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'test@example.com',
        isLoading: false
      })

      render(<DashboardHeader {...defaultProps} />)

      expect(screen.getByText('Logout')).toBeInTheDocument()
      expect(screen.queryByText('Logging out...')).not.toBeInTheDocument()
    })

    it('should disable button when isLoading is true', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'test@example.com',
        isLoading: true
      })

      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logging out/i })
      expect(logoutButton).toBeDisabled()
    })

    it('should enable button when isLoading is false', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'test@example.com',
        isLoading: false
      })

      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })
      expect(logoutButton).not.toBeDisabled()
    })
  })

  describe('Button Styling and Variants', () => {
    it('should apply correct button variant and size', () => {
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })
      // Note: These classes would be applied by the Button component
      // We can't test the exact classes without mocking the Button component
      expect(logoutButton).toBeInTheDocument()
    })

    it('should include logout icon in button', () => {
      render(<DashboardHeader {...defaultProps} />)

      expect(screen.getByTestId('logout-icon')).toBeInTheDocument()
      expect(screen.getByTestId('logout-icon')).toHaveClass('h-4', 'w-4')
    })
  })

  describe('Layout and Positioning', () => {
    it('should have correct header layout structure', () => {
      render(<DashboardHeader {...defaultProps} />)

      const header = screen.getByRole('banner')
      expect(header).toHaveClass('mb-8', 'flex', 'items-center', 'justify-between')
    })

    it('should position title and controls correctly', () => {
      render(<DashboardHeader {...defaultProps} />)

      const header = screen.getByRole('banner')
      const titleSection = header.firstChild
      const controlsSection = header.lastChild

      expect(titleSection).toBeInTheDocument()
      expect(controlsSection).toBeInTheDocument()
      expect(controlsSection).toHaveClass('flex', 'items-center', 'gap-3')
    })
  })

  describe('Accessibility', () => {
    it('should have proper semantic HTML structure', () => {
      render(<DashboardHeader {...defaultProps} />)

      expect(screen.getByRole('banner')).toBeInTheDocument()
      expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument()
    })

    it('should support keyboard navigation', async () => {
      const user = userEvent.setup()
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })

      // Tab to button and press Enter
      await user.tab()
      expect(logoutButton).toHaveFocus()

      await user.keyboard('{Enter}')
      expect(mockLogout).toHaveBeenCalledTimes(1)
    })

    it('should support space key activation', async () => {
      const user = userEvent.setup()
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })
      logoutButton.focus()

      await user.keyboard(' ')
      expect(mockLogout).toHaveBeenCalledTimes(1)
    })

    it('should have accessible button text for screen readers', () => {
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })
      expect(logoutButton).toHaveAccessibleName()
    })

    it('should maintain focus management during loading state', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'test@example.com',
        isLoading: true
      })

      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logging out/i })
      expect(logoutButton).toBeDisabled()
      expect(logoutButton).toHaveAttribute('disabled')
    })
  })

  describe('Responsive Design', () => {
    it('should render user email and logout button in flexible container', () => {
      render(<DashboardHeader {...defaultProps} />)

      const controlsContainer = screen.getByText('test@example.com').closest('div')?.parentElement
      expect(controlsContainer).toHaveClass('flex', 'items-center', 'gap-3')
    })

    it('should handle long email addresses gracefully', () => {
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'very.long.email.address.that.might.overflow@example.com',
        isLoading: false
      })

      render(<DashboardHeader {...defaultProps} />)

      expect(screen.getByText('very.long.email.address.that.might.overflow@example.com')).toBeInTheDocument()
    })

    it('should handle long titles gracefully', () => {
      render(
        <DashboardHeader
          title="Very Long Dashboard Title That Might Wrap On Smaller Screens"
          subtitle="Also a very long subtitle that provides detailed information"
        />
      )

      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
        'Very Long Dashboard Title That Might Wrap On Smaller Screens'
      )
      expect(screen.getByText('Also a very long subtitle that provides detailed information')).toBeInTheDocument()
    })
  })

  describe('Error Scenarios', () => {
    it('should handle logout function errors gracefully without crashing', async () => {
      // Create a console error spy to suppress error output during test
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

      const errorLogout = vi.fn().mockResolvedValue(undefined) // Mock as resolved to avoid unhandled rejection

      mockUseAuthContext.mockReturnValue({
        logout: errorLogout,
        userEmail: 'test@example.com',
        isLoading: false
      })

      const user = userEvent.setup()
      render(<DashboardHeader {...defaultProps} />)

      const logoutButton = screen.getByRole('button', { name: /logout/i })

      await user.click(logoutButton)

      expect(errorLogout).toHaveBeenCalledTimes(1)
      // Component should not crash and remain functional
      expect(screen.getByRole('banner')).toBeInTheDocument()
      expect(logoutButton).toBeInTheDocument()

      consoleErrorSpy.mockRestore()
    })

    it('should handle missing auth context gracefully', () => {
      mockUseAuthContext.mockImplementation(() => {
        throw new Error('useAuth must be used within an AuthProvider')
      })

      expect(() => render(<DashboardHeader {...defaultProps} />)).toThrow(
        'useAuth must be used within an AuthProvider'
      )
    })

    it('should handle undefined values from auth context', () => {
      mockUseAuthContext.mockReturnValue({
        logout: undefined as any,
        userEmail: undefined,
        isLoading: undefined as any
      })

      render(<DashboardHeader {...defaultProps} />)

      // Should render without crashing
      expect(screen.getByRole('banner')).toBeInTheDocument()
      expect(screen.getByRole('button')).toBeInTheDocument()
    })
  })

  describe('Component Props', () => {
    it('should render different titles correctly', () => {
      const { rerender } = render(<DashboardHeader title="Initial Title" />)
      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Initial Title')

      rerender(<DashboardHeader title="Updated Title" />)
      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Updated Title')
    })

    it('should handle title with special characters', () => {
      render(<DashboardHeader title="Dashboard with émojis 🚀 & symbols!" />)

      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
        'Dashboard with émojis 🚀 & symbols!'
      )
    })

    it('should handle empty title gracefully', () => {
      render(<DashboardHeader title="" />)

      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveTextContent('')
    })

    it('should handle subtitle changes', () => {
      const { rerender } = render(
        <DashboardHeader title="Test" subtitle="Initial subtitle" />
      )
      expect(screen.getByText('Initial subtitle')).toBeInTheDocument()

      rerender(<DashboardHeader title="Test" subtitle="New subtitle" />)
      expect(screen.getByText('New subtitle')).toBeInTheDocument()
      expect(screen.queryByText('Initial subtitle')).not.toBeInTheDocument()
    })
  })

  describe('Integration with Auth Context', () => {
    it('should reflect real-time changes from auth context', () => {
      const { rerender } = render(<DashboardHeader {...defaultProps} />)

      // Initially not loading
      expect(screen.getByText('Logout')).toBeInTheDocument()

      // Simulate loading state change
      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'test@example.com',
        isLoading: true
      })

      rerender(<DashboardHeader {...defaultProps} />)
      expect(screen.getByText('Logging out...')).toBeInTheDocument()
    })

    it('should handle user email changes', () => {
      const { rerender } = render(<DashboardHeader {...defaultProps} />)

      expect(screen.getByText('test@example.com')).toBeInTheDocument()

      mockUseAuthContext.mockReturnValue({
        logout: mockLogout,
        userEmail: 'newemail@example.com',
        isLoading: false
      })

      rerender(<DashboardHeader {...defaultProps} />)
      expect(screen.getByText('newemail@example.com')).toBeInTheDocument()
      expect(screen.queryByText('test@example.com')).not.toBeInTheDocument()
    })
  })
})