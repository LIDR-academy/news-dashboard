import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { ChangePassword } from '../components/ChangePassword';
import { useChangePassword } from '../hooks/useChangePassword';

// Mock the hook
jest.mock('../hooks/useChangePassword');
const mockUseChangePassword = useChangePassword as jest.MockedFunction<typeof useChangePassword>;

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
  Input: ({ onChange, value, type, className, ...props }: any) => (
    <input onChange={onChange} value={value} type={type} className={className} {...props} />
  ),
}));

jest.mock('../../../core/components/ui/label', () => ({
  Label: ({ children, htmlFor }: any) => <label htmlFor={htmlFor}>{children}</label>,
}));

jest.mock('lucide-react', () => ({
  ArrowLeft: () => <div data-testid="arrow-left-icon" />,
  Key: () => <div data-testid="key-icon" />,
  Eye: () => <div data-testid="eye-icon" />,
  EyeOff: () => <div data-testid="eye-off-icon" />,
}));

// Mock react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
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

describe('ChangePassword', () => {
  const mockChangePasswordMutation = {
    mutate: jest.fn(),
    isPending: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockUseChangePassword.mockReturnValue(mockChangePasswordMutation as any);
  });

  it('renders form with all password fields', () => {
    renderWithProviders(<ChangePassword />);

    expect(screen.getByLabelText('Current Password')).toBeInTheDocument();
    expect(screen.getByLabelText('New Password')).toBeInTheDocument();
    expect(screen.getByLabelText('Confirm New Password')).toBeInTheDocument();
    expect(screen.getByText('Change Password')).toBeInTheDocument();
  });

  it('validates current password field', async () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    
    // Test empty current password
    fireEvent.change(currentPasswordInput, { target: { value: '' } });
    fireEvent.click(screen.getByText('Change Password'));
    
    await waitFor(() => {
      expect(screen.getByText('Current password is required')).toBeInTheDocument();
    });
  });

  it('validates new password field', async () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    
    fireEvent.change(currentPasswordInput, { target: { value: 'oldpassword' } });
    
    // Test empty new password
    fireEvent.change(newPasswordInput, { target: { value: '' } });
    fireEvent.click(screen.getByText('Change Password'));
    
    await waitFor(() => {
      expect(screen.getByText('New password is required')).toBeInTheDocument();
    });

    // Test short new password
    fireEvent.change(newPasswordInput, { target: { value: '123' } });
    fireEvent.click(screen.getByText('Change Password'));
    
    await waitFor(() => {
      expect(screen.getByText('New password must be at least 6 characters')).toBeInTheDocument();
    });
  });

  it('validates confirm password field', async () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm New Password');
    
    fireEvent.change(currentPasswordInput, { target: { value: 'oldpassword' } });
    fireEvent.change(newPasswordInput, { target: { value: 'newpassword123' } });
    
    // Test empty confirm password
    fireEvent.change(confirmPasswordInput, { target: { value: '' } });
    fireEvent.click(screen.getByText('Change Password'));
    
    await waitFor(() => {
      expect(screen.getByText('Please confirm your new password')).toBeInTheDocument();
    });
  });

  it('validates password confirmation match', async () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm New Password');
    
    fireEvent.change(currentPasswordInput, { target: { value: 'oldpassword' } });
    fireEvent.change(newPasswordInput, { target: { value: 'newpassword123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'differentpassword' } });
    fireEvent.click(screen.getByText('Change Password'));
    
    await waitFor(() => {
      expect(screen.getByText('Passwords do not match')).toBeInTheDocument();
    });
  });

  it('validates new password is different from current', async () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm New Password');
    
    fireEvent.change(currentPasswordInput, { target: { value: 'samepassword' } });
    fireEvent.change(newPasswordInput, { target: { value: 'samepassword' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'samepassword' } });
    fireEvent.click(screen.getByText('Change Password'));
    
    await waitFor(() => {
      expect(screen.getByText('New password must be different from current password')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm New Password');
    
    fireEvent.change(currentPasswordInput, { target: { value: 'oldpassword' } });
    fireEvent.change(newPasswordInput, { target: { value: 'newpassword123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'newpassword123' } });
    fireEvent.click(screen.getByText('Change Password'));

    await waitFor(() => {
      expect(mockChangePasswordMutation.mutate).toHaveBeenCalledWith({
        current_password: 'oldpassword',
        new_password: 'newpassword123',
        confirm_password: 'newpassword123'
      });
    });
  });

  it('shows loading state during submission', () => {
    mockUseChangePassword.mockReturnValue({
      ...mockChangePasswordMutation,
      isPending: true,
    } as any);

    renderWithProviders(<ChangePassword />);

    expect(screen.getByText('Changing...')).toBeInTheDocument();
    expect(screen.getByText('Change Password')).toBeDisabled();
  });

  it('navigates back to profile on successful submission', async () => {
    mockChangePasswordMutation.mutate.mockImplementation((data, options) => {
      options?.onSuccess?.();
    });

    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm New Password');
    
    fireEvent.change(currentPasswordInput, { target: { value: 'oldpassword' } });
    fireEvent.change(newPasswordInput, { target: { value: 'newpassword123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'newpassword123' } });
    fireEvent.click(screen.getByText('Change Password'));

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/profile');
    });
  });

  it('toggles password visibility', () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm New Password');

    // Initially passwords should be hidden
    expect(currentPasswordInput).toHaveAttribute('type', 'password');
    expect(newPasswordInput).toHaveAttribute('type', 'password');
    expect(confirmPasswordInput).toHaveAttribute('type', 'password');

    // Click visibility toggle for current password
    const currentPasswordToggle = screen.getAllByTestId('eye-icon')[0];
    fireEvent.click(currentPasswordToggle);
    expect(currentPasswordInput).toHaveAttribute('type', 'text');

    // Click visibility toggle for new password
    const newPasswordToggle = screen.getAllByTestId('eye-icon')[1];
    fireEvent.click(newPasswordToggle);
    expect(newPasswordInput).toHaveAttribute('type', 'text');

    // Click visibility toggle for confirm password
    const confirmPasswordToggle = screen.getAllByTestId('eye-icon')[2];
    fireEvent.click(confirmPasswordToggle);
    expect(confirmPasswordInput).toHaveAttribute('type', 'text');
  });

  it('clears errors when user starts typing', async () => {
    renderWithProviders(<ChangePassword />);

    const currentPasswordInput = screen.getByLabelText('Current Password');
    
    // Trigger validation error
    fireEvent.change(currentPasswordInput, { target: { value: '' } });
    fireEvent.click(screen.getByText('Change Password'));
    
    await waitFor(() => {
      expect(screen.getByText('Current password is required')).toBeInTheDocument();
    });

    // Start typing to clear error
    fireEvent.change(currentPasswordInput, { target: { value: 'new' } });
    
    await waitFor(() => {
      expect(screen.queryByText('Current password is required')).not.toBeInTheDocument();
    });
  });
});
