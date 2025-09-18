import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useChangePassword } from '../hooks/useChangePassword';
import { profileService } from '../data/profile.service';
import { toast } from 'sonner';

// Mock the profile service
jest.mock('../data/profile.service');
const mockProfileService = profileService as jest.Mocked<typeof profileService>;

// Mock sonner toast
jest.mock('sonner', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
  },
}));

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useChangePassword', () => {
  const mockResponse = {
    message: 'Password changed successfully'
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should change password successfully', async () => {
    mockProfileService.changePassword.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'oldpassword',
      new_password: 'newpassword123',
      confirm_password: 'newpassword123'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data).toEqual(mockResponse);
    expect(mockProfileService.changePassword).toHaveBeenCalledWith(passwordData);
    expect(toast.success).toHaveBeenCalledWith('Password changed successfully');
  });

  it('should handle change password error', async () => {
    const error = new Error('Failed to change password');
    mockProfileService.changePassword.mockRejectedValue(error);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'wrongpassword',
      new_password: 'newpassword123',
      confirm_password: 'newpassword123'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
    expect(toast.error).toHaveBeenCalledWith('Failed to change password');
  });

  it('should handle API error response', async () => {
    const apiError = {
      response: {
        data: {
          detail: 'Current password is incorrect'
        }
      }
    };
    mockProfileService.changePassword.mockRejectedValue(apiError);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'wrongpassword',
      new_password: 'newpassword123',
      confirm_password: 'newpassword123'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(toast.error).toHaveBeenCalledWith('Current password is incorrect');
  });

  it('should handle error without response data', async () => {
    const error = new Error('Network error');
    mockProfileService.changePassword.mockRejectedValue(error);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'oldpassword',
      new_password: 'newpassword123',
      confirm_password: 'newpassword123'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(toast.error).toHaveBeenCalledWith('Network error');
  });

  it('should handle error with message property', async () => {
    const error = {
      message: 'Custom error message'
    };
    mockProfileService.changePassword.mockRejectedValue(error);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'oldpassword',
      new_password: 'newpassword123',
      confirm_password: 'newpassword123'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(toast.error).toHaveBeenCalledWith('Custom error message');
  });

  it('should handle unknown error format', async () => {
    const error = 'Unknown error';
    mockProfileService.changePassword.mockRejectedValue(error);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'oldpassword',
      new_password: 'newpassword123',
      confirm_password: 'newpassword123'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(toast.error).toHaveBeenCalledWith('Failed to change password');
  });

  it('should handle validation error from API', async () => {
    const validationError = {
      response: {
        data: {
          detail: 'New password and confirmation do not match'
        }
      }
    };
    mockProfileService.changePassword.mockRejectedValue(validationError);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'oldpassword',
      new_password: 'newpassword123',
      confirm_password: 'differentpassword'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(toast.error).toHaveBeenCalledWith('New password and confirmation do not match');
  });

  it('should handle server error', async () => {
    const serverError = {
      response: {
        data: {
          detail: 'Internal server error'
        }
      }
    };
    mockProfileService.changePassword.mockRejectedValue(serverError);

    const { result } = renderHook(() => useChangePassword(), { wrapper });

    const passwordData = {
      current_password: 'oldpassword',
      new_password: 'newpassword123',
      confirm_password: 'newpassword123'
    };

    result.current.mutate(passwordData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(toast.error).toHaveBeenCalledWith('Internal server error');
  });
});
