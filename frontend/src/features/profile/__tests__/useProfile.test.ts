import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useProfile } from '../hooks/useProfile';
import { profileService } from '../data/profile.service';

// Mock the profile service
jest.mock('../data/profile.service');
const mockProfileService = profileService as jest.Mocked<typeof profileService>;

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

describe('useProfile', () => {
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

  it('should fetch profile data successfully', async () => {
    mockProfileService.getProfile.mockResolvedValue(mockProfile);

    const { result } = renderHook(() => useProfile(), { wrapper });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data).toEqual(mockProfile);
    expect(mockProfileService.getProfile).toHaveBeenCalledTimes(1);
  });

  it('should handle fetch error', async () => {
    const error = new Error('Failed to fetch profile');
    mockProfileService.getProfile.mockRejectedValue(error);

    const { result } = renderHook(() => useProfile(), { wrapper });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
    expect(mockProfileService.getProfile).toHaveBeenCalledTimes(1);
  });

  it('should have correct query configuration', () => {
    const { result } = renderHook(() => useProfile(), { wrapper });

    expect(result.current.queryKey).toEqual(['profile']);
    expect(result.current.staleTime).toBe(5 * 60 * 1000); // 5 minutes
    expect(result.current.retry).toBe(1);
  });
});
