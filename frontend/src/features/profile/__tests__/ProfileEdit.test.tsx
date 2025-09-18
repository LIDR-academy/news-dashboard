import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { ProfileEdit } from '../components/ProfileEdit';
import { useProfile } from '../hooks/useProfile';
import { useUpdateProfile } from '../hooks/useUpdateProfile';

// Mock the hooks
jest.mock('../hooks/useProfile');
jest.mock('../hooks/useUpdateProfile');
const mockUseProfile = useProfile as jest.MockedFunction<typeof useProfile>;
const mockUseUpdateProfile = useUpdateProfile as jest.MockedFunction<typeof useUpdateProfile>;

// Mock the core components
jest.mock('../../../core/components/ui/card', () => ({
  Card: ({ children }: { children: React.ReactNode }) => <div data-testid="card">{children}</div>,
  CardContent: ({ children }: { children: React.ReactNode }) => <div data-testid="card-content">{children}</div>,
  CardDescription: ({ children }: { children: React.ReactNode }) => <div data-testid="card-description">{children}</div>,
  CardHeader: ({ children }: { children: React.ReactNode }) => <div data-testid="card-header">{children}</div>,
  CardTitle: ({ children }: { children: React.ReactNode }) => <div data-testid="card-title">{children}</div>,
}));

jest.mock('../../../core/components/ui/button', () => ({
  Button: ({ children, onClick, type, disabled, ...props }: any) => (
    <button onClick={onClick} type={type} disabled={disabled} {...props}>
      {children}
    </button>
  ),
}));

jest.mock('../../../core/components/ui/input', () => ({
  Input: ({ onChange, value, className, ...props }: any) => (
    <input onChange={onChange} value={value} className={className} {...props} />
  ),
}));

jest.mock('../../../core/components/ui/label', () => ({
  Label: ({ children, htmlFor }: any) => <label htmlFor={htmlFor}>{children}</label>,
}));

jest.mock('../../../core/components/ui/skeleton', () => ({
  Skeleton: ({ className }: { className?: string }) => <div data-testid="skeleton" className={className}></div>,
}));

jest.mock('lucide-react', () => ({
  ArrowLeft: () => <div data-testid="arrow-left-icon" />,
  Save: () => <div data-testid="save-icon" />,
  X: () => <div data-testid="x-icon" />,
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

describe('ProfileEdit', () => {
  const mockProfile = {
    id: 'user123',
    email: 'test@example.com',
    username: 'testuser',
    is_active: true,
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-02T00:00:00Z',
  };

  const mockUpdateMutation = {
    mutate: jest.fn(),
    isPending: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockUseUpdateProfile.mockReturnValue(mockUpdateMutation as any);
  });

  it('renders loading state', () => {
    mockUseProfile.mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
    } as any);

    renderWithProviders(<ProfileEdit />);

    expect(screen.getAllByTestId('skeleton')).toHaveLength(3);
  });

  it('renders form with current profile data', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileEdit />);

    await waitFor(() => {
      expect(screen.getByDisplayValue('testuser')).toBeInTheDocument();
      expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument();
    });
  });

  it('validates username field', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileEdit />);

    const usernameInput = screen.getByDisplayValue('testuser');
    
    // Test empty username
    fireEvent.change(usernameInput, { target: { value: '' } });
    fireEvent.click(screen.getByText('Save Changes'));
    
    await waitFor(() => {
      expect(screen.getByText('Username is required')).toBeInTheDocument();
    });

    // Test short username
    fireEvent.change(usernameInput, { target: { value: 'ab' } });
    fireEvent.click(screen.getByText('Save Changes'));
    
    await waitFor(() => {
      expect(screen.getByText('Username must be at least 3 characters')).toBeInTheDocument();
    });

    // Test invalid characters
    fireEvent.change(usernameInput, { target: { value: 'test@user' } });
    fireEvent.click(screen.getByText('Save Changes'));
    
    await waitFor(() => {
      expect(screen.getByText('Username can only contain letters, numbers, and underscores')).toBeInTheDocument();
    });
  });

  it('validates email field', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileEdit />);

    const emailInput = screen.getByDisplayValue('test@example.com');
    
    // Test empty email
    fireEvent.change(emailInput, { target: { value: '' } });
    fireEvent.click(screen.getByText('Save Changes'));
    
    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument();
    });

    // Test invalid email format
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.click(screen.getByText('Save Changes'));
    
    await waitFor(() => {
      expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileEdit />);

    const usernameInput = screen.getByDisplayValue('testuser');
    const emailInput = screen.getByDisplayValue('test@example.com');
    
    fireEvent.change(usernameInput, { target: { value: 'newusername' } });
    fireEvent.change(emailInput, { target: { value: 'newemail@example.com' } });
    fireEvent.click(screen.getByText('Save Changes'));

    await waitFor(() => {
      expect(mockUpdateMutation.mutate).toHaveBeenCalledWith({
        username: 'newusername',
        email: 'newemail@example.com'
      });
    });
  });

  it('shows loading state during submission', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    mockUseUpdateProfile.mockReturnValue({
      ...mockUpdateMutation,
      isPending: true,
    } as any);

    renderWithProviders(<ProfileEdit />);

    expect(screen.getByText('Saving...')).toBeInTheDocument();
    expect(screen.getByText('Save Changes')).toBeDisabled();
  });

  it('clears errors when user starts typing', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileEdit />);

    const usernameInput = screen.getByDisplayValue('testuser');
    
    // Trigger validation error
    fireEvent.change(usernameInput, { target: { value: '' } });
    fireEvent.click(screen.getByText('Save Changes'));
    
    await waitFor(() => {
      expect(screen.getByText('Username is required')).toBeInTheDocument();
    });

    // Start typing to clear error
    fireEvent.change(usernameInput, { target: { value: 'new' } });
    
    await waitFor(() => {
      expect(screen.queryByText('Username is required')).not.toBeInTheDocument();
    });
  });

  it('does not submit if no changes are made', async () => {
    mockUseProfile.mockReturnValue({
      data: mockProfile,
      isLoading: false,
      error: null,
    } as any);

    renderWithProviders(<ProfileEdit />);

    fireEvent.click(screen.getByText('Save Changes'));

    // Should not call mutate if no changes
    expect(mockUpdateMutation.mutate).not.toHaveBeenCalled();
  });
});
