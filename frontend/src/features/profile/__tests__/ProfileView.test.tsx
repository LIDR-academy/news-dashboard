import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { ProfileView } from '../components/ProfileView';
import { useProfile } from '../hooks/useProfile';

// Mock the useProfile hook
jest.mock('../hooks/useProfile');
const mockUseProfile = useProfile as jest.MockedFunction<typeof useProfile>;

// Mock the core components
jest.mock('../../../core/components/ui/card', () => ({
  Card: ({ children }: { children: React.ReactNode }) => <div data-testid="card">{children}</div>,
  CardContent: ({ children }: { children: React.ReactNode }) => <div data-testid="card-content">{children}</div>,
  CardDescription: ({ children }: { children: React.ReactNode }) => <div data-testid="card-description">{children}</div>,
  CardHeader: ({ children }: { children: React.ReactNode }) => <div data-testid="card-header">{children}</div>,
  CardTitle: ({ children }: { children: React.ReactNode }) => <div data-testid="card-title">{children}</div>,
}));

jest.mock('../../../core/components/ui/button', () => ({
  Button: ({ children, ...props }: any) => <button {...props}>{children}</button>,
}));

jest.mock('../../../core/components/ui/badge', () => ({
  Badge: ({ children, ...props }: any) => <span {...props}>{children}</span>,
}));

jest.mock('../../../core/components/ui/skeleton', () => ({
  Skeleton: ({ className }: { className?: string }) => <div data-testid="skeleton" className={className}></div>,
}));

jest.mock('lucide-react', () => ({
  User: () => <div data-testid="user-icon" />,
  Mail: () => <div data-testid="mail-icon" />,
  Shield: () => <div data-testid="shield-icon" />,
  CalendarDays: () => <div data-testid="calendar-icon" />,
  Edit: () => <div data-testid="edit-icon" />,
  Key: () => <div data-testid="key-icon" />,
}));

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

const renderWithProviders = (component: React.ReactElement) => {
  const queryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {component}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('ProfileView', () => {
  const mockProfile = {
    id: 'user123',
    email: 'test@example.com',
    username: 'testuser',
    is_active: true,
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-02T00:00:00Z',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state', () => {
    mockUseProfile.mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
    } as any);

    renderWithProviders(<ProfileView />);

    expect(screen.getAllByTestId('skeleton')).toHaveLength(5);
  });

  it('renders error state', () => {
    mockUseProfile.mockReturnValue({
      data: undefined,
      isLoading: false,
      error: new Error('Failed to load'),
    } as any);

    renderWithProviders(<ProfileView />);

    expect(screen.getByText('Failed to load profile. Please try again.')).toBeInTheDocument();
  });

  it('renders no data state', () => {
    mockUseProfile.mockReturnValue({
      data: undefined,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileView />);

    expect(screen.getByText('No profile data available.')).toBeInTheDocument();
  });

  it('renders profile information correctly', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileView />);

    await waitFor(() => {
      expect(screen.getByText('Profile Information')).toBeInTheDocument();
      expect(screen.getByText('testuser')).toBeInTheDocument();
      expect(screen.getByText('test@example.com')).toBeInTheDocument();
      expect(screen.getByText('Active')).toBeInTheDocument();
    });

    // Check for navigation links
    expect(screen.getByText('Edit Profile')).toBeInTheDocument();
    expect(screen.getByText('Change Password')).toBeInTheDocument();
  });

  it('displays inactive status correctly', async () => {
    const inactiveProfile = { ...mockProfile, is_active: false };
    
    mockUseProfile.mockReturnValue({
      data: inactiveProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileView />);

    await waitFor(() => {
      expect(screen.getByText('Inactive')).toBeInTheDocument();
    });
  });

  it('formats dates correctly', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileView />);

    await waitFor(() => {
      // Check that dates are formatted (exact format may vary by locale)
      expect(screen.getByText(/January 1, 2023/)).toBeInTheDocument();
      expect(screen.getByText(/January 2, 2023/)).toBeInTheDocument();
    });
  });
});
