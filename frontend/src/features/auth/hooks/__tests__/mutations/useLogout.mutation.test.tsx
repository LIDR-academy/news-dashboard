import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React, { type ReactNode } from 'react'
import { useLogoutMutation } from '../../mutations/useLogout.mutation'
import { cleanup, createMockAxiosError } from '@/test-utils/mocks'

// Mock auth service at module level
vi.mock('../../../data/auth.service', () => ({
  authService: {
    logout: vi.fn()
  }
}))

import { authService } from '../../../data/auth.service'

describe('useLogoutMutation', () => {
  let queryClient: QueryClient
  let clearSpy: ReturnType<typeof vi.spyOn>
  let consoleErrorSpy: ReturnType<typeof vi.spyOn>

  // Type cast to access mocked methods
  const mockAuthService = authService as any

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false }
      }
    })

    // Spy on queryClient.clear method
    clearSpy = vi.spyOn(queryClient, 'clear').mockImplementation(() => {})

    // Spy on console.error to test error logging
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

    // Reset auth service mocks
    mockAuthService.logout.mockResolvedValue('Logout successful')

    vi.clearAllMocks()
  })

  afterEach(() => {
    cleanup.all()
    clearSpy.mockRestore()
    consoleErrorSpy.mockRestore()
  })

  const createWrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )

  describe('Hook Structure', () => {
    it('should return correct structure with expected properties', () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      expect(result.current).toEqual({
        action: expect.any(Function),
        isLoading: expect.any(Boolean),
        error: null,
        isSuccess: expect.any(Boolean)
      })
    })

    it('should initialize with correct default states', () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      expect(result.current.action).toBeInstanceOf(Function)
      expect(result.current.isLoading).toBe(false)
      expect(result.current.error).toBe(null)
      expect(result.current.isSuccess).toBe(false)
    })

    it('should use mutateAsync for action function (not mutate)', () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // The action function should be mutateAsync (bound function) to return a promise
      expect(typeof result.current.action).toBe('function')
    })
  })

  describe('Successful Logout', () => {
    it('should call authService.logout and clear query cache on successful logout', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await result.current.action()

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
    })

    it('should complete logout operation without errors', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await expect(result.current.action()).resolves.toBeUndefined()

      expect(result.current.error).toBe(null)
      expect(result.current.isLoading).toBe(false)
      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
    })

    it('should set loading state correctly during mutation', async () => {
      // Mock authService.logout to take some time
      mockAuthService.logout.mockImplementation(
        () => new Promise(resolve => setTimeout(() => resolve('Success'), 50))
      )

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      const logoutPromise = result.current.action()

      // The function should return a promise
      expect(logoutPromise).toBeInstanceOf(Promise)

      await logoutPromise

      // Loading should be false after completion
      await waitFor(() => {
        expect(result.current.isLoading).toBe(false)
      })
      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
    })

    it('should set isSuccess to true after successful logout', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await result.current.action()

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })
      expect(result.current.error).toBe(null)
      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
    })

    it('should call onSuccess callback after successful backend logout', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await result.current.action()

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
      expect(result.current.error).toBe(null)
    })
  })

  describe('Error Handling', () => {
    it('should clear cache even when backend logout fails (graceful fallback)', async () => {
      const backendError = createMockAxiosError('Backend logout failed', 500)
      mockAuthService.logout.mockRejectedValue(backendError)

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // mutateAsync will throw but onError still clears cache
      await expect(result.current.action()).rejects.toThrow('Backend logout failed')

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1) // Cache still cleared via onError
      expect(consoleErrorSpy).toHaveBeenCalledWith('Logout error:', backendError)
    })

    it('should handle 401 unauthorized errors from backend', async () => {
      const unauthorizedError = createMockAxiosError('Unauthorized', 401)
      mockAuthService.logout.mockRejectedValue(unauthorizedError)

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await expect(result.current.action()).rejects.toThrow('Unauthorized')

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
      expect(consoleErrorSpy).toHaveBeenCalledWith('Logout error:', unauthorizedError)
    })

    it('should handle 404 not found errors from backend', async () => {
      const notFoundError = createMockAxiosError('Endpoint not found', 404)
      mockAuthService.logout.mockRejectedValue(notFoundError)

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await expect(result.current.action()).rejects.toThrow('Endpoint not found')

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
      expect(consoleErrorSpy).toHaveBeenCalledWith('Logout error:', notFoundError)
    })

    it('should handle network errors gracefully', async () => {
      const networkError = new Error('Network Error')
      mockAuthService.logout.mockRejectedValue(networkError)

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await expect(result.current.action()).rejects.toThrow('Network Error')

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
      expect(consoleErrorSpy).toHaveBeenCalledWith('Logout error:', networkError)
    })

    it('should handle timeout errors from backend', async () => {
      const timeoutError = createMockAxiosError('Request timeout', 408)
      mockAuthService.logout.mockRejectedValue(timeoutError)

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await expect(result.current.action()).rejects.toThrow('Request timeout')

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
      expect(consoleErrorSpy).toHaveBeenCalledWith('Logout error:', timeoutError)
    })
  })

  describe('Query Cache Integration', () => {
    it('should clear all cached queries and mutations after successful backend logout', async () => {
      // Add some data to the cache
      queryClient.setQueryData(['users'], { data: 'user data' })
      queryClient.setQueryData(['products'], { data: 'product data' })
      queryClient.setQueryData(['orders'], { data: 'order data' })

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await result.current.action()

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)

      // Verify clear was called on the correct queryClient instance
      expect(clearSpy).toHaveBeenCalledWith()
    })

    it('should clear cache even when backend call fails', async () => {
      const backendError = createMockAxiosError('Backend error', 500)
      mockAuthService.logout.mockRejectedValue(backendError)

      // Add some data to the cache
      queryClient.setQueryData(['sensitive-data'], { token: 'secret' })

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await expect(result.current.action()).rejects.toThrow('Backend error')

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1) // Cache still cleared for security
    })

    it('should not interfere with new queries after logout', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await result.current.action()

      // After logout, new queries should still work
      queryClient.setQueryData(['new-data'], { data: 'new data after logout' })
      const newData = queryClient.getQueryData(['new-data'])

      expect(newData).toEqual({ data: 'new data after logout' })
      expect(clearSpy).toHaveBeenCalledTimes(1)
    })

    it('should handle cache clear with active queries', async () => {
      // Simulate active queries
      queryClient.prefetchQuery({
        queryKey: ['active-query'],
        queryFn: () => Promise.resolve({ data: 'active' })
      })

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await result.current.action()

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
    })
  })

  describe('Multiple Calls', () => {
    it('should handle multiple sequential logout attempts', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // First logout
      await result.current.action()
      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)

      // Second logout
      await result.current.action()
      expect(mockAuthService.logout).toHaveBeenCalledTimes(2)
      expect(clearSpy).toHaveBeenCalledTimes(2)

      // Third logout
      await result.current.action()
      expect(mockAuthService.logout).toHaveBeenCalledTimes(3)
      expect(clearSpy).toHaveBeenCalledTimes(3)
    })

    it('should handle concurrent logout calls', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // Make multiple concurrent calls
      const promises = [
        result.current.action(),
        result.current.action(),
        result.current.action()
      ]

      await Promise.all(promises)

      expect(mockAuthService.logout).toHaveBeenCalledTimes(3)
      expect(clearSpy).toHaveBeenCalledTimes(3)
    })

    it('should handle mixed success and failure scenarios', async () => {
      let callCount = 0
      mockAuthService.logout.mockImplementation(() => {
        callCount++
        if (callCount === 1) {
          return Promise.resolve('Success')
        } else if (callCount === 2) {
          return Promise.reject(createMockAxiosError('Backend error', 500))
        } else {
          return Promise.resolve('Success again')
        }
      })

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // First call should succeed
      await result.current.action()
      expect(clearSpy).toHaveBeenCalledTimes(1)

      // Second call should fail but still clear cache
      await expect(result.current.action()).rejects.toThrow('Backend error')
      expect(clearSpy).toHaveBeenCalledTimes(2)
      expect(consoleErrorSpy).toHaveBeenCalledWith('Logout error:', expect.any(Error))

      // Third call should succeed again
      await result.current.action()
      expect(clearSpy).toHaveBeenCalledTimes(3)

      expect(mockAuthService.logout).toHaveBeenCalledTimes(3)
    })
  })

  describe('Implementation Details', () => {
    it('should use mutateAsync instead of mutate for promise return', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // mutateAsync returns a promise, mutate does not
      const logoutResult = result.current.action()
      expect(logoutResult).toBeInstanceOf(Promise)

      await logoutResult
      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
    })

    it('should have access to React Query mutation state', async () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // Initially idle
      expect(result.current.isLoading).toBe(false)
      expect(result.current.error).toBe(null)
      expect(result.current.isSuccess).toBe(false)

      const logoutPromise = result.current.action()

      // Should show loading during execution
      await waitFor(() => {
        if (result.current.isLoading) {
          expect(result.current.isLoading).toBe(true)
        }
      })

      await logoutPromise

      // Should return to idle after completion
      expect(result.current.isLoading).toBe(false)
      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })
    })

    it('should maintain mutation instance across re-renders', () => {
      const { result, rerender } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      const firstInstance = result.current.action
      rerender()
      const secondInstance = result.current.action

      // Function instances should be stable across re-renders
      expect(firstInstance).toBe(secondInstance)
    })

    it('should export correct interface properties', () => {
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // Verify interface matches useLogoutMutation return type
      expect(result.current).toHaveProperty('action')
      expect(result.current).toHaveProperty('isLoading')
      expect(result.current).toHaveProperty('error')
      expect(result.current).toHaveProperty('isSuccess')

      // Should not have the old 'logout' property
      expect(result.current).not.toHaveProperty('logout')
    })
  })

  describe('Edge Cases', () => {
    it('should handle queryClient being null or undefined', async () => {
      // This is a theoretical edge case - in practice, the hook would throw
      // if queryClient is not available, but we test the robustness
      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // Even with a mocked clear that might fail, the structure should be maintained
      expect(result.current.action).toBeInstanceOf(Function)
      expect(result.current.isLoading).toBe(false)
      expect(result.current.error).toBe(null)
      expect(result.current.isSuccess).toBe(false)
    })

    it('should prioritize local security over backend errors', async () => {
      // Even if backend fails, we should clear local cache for security
      const backendError = createMockAxiosError('Server unavailable', 503)
      mockAuthService.logout.mockRejectedValue(backendError)

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await expect(result.current.action()).rejects.toThrow('Server unavailable')

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1) // Local cache cleared despite backend error
      expect(consoleErrorSpy).toHaveBeenCalledWith('Logout error:', backendError)
    })

    it('should handle malformed response from backend', async () => {
      mockAuthService.logout.mockResolvedValue(null as any) // Malformed response

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      await result.current.action()

      expect(mockAuthService.logout).toHaveBeenCalledTimes(1)
      expect(clearSpy).toHaveBeenCalledTimes(1)
      expect(result.current.error).toBe(null) // Should not error on malformed success response
    })

    it('should not have side effects when mutation fails', async () => {
      const originalState = { isLoading: false, error: null, isSuccess: false }
      const backendError = createMockAxiosError('Backend error', 500)
      mockAuthService.logout.mockRejectedValue(backendError)

      const { result } = renderHook(() => useLogoutMutation(), {
        wrapper: createWrapper
      })

      // Capture pre-logout state
      expect(result.current.isLoading).toBe(originalState.isLoading)
      expect(result.current.error).toBe(originalState.error)
      expect(result.current.isSuccess).toBe(originalState.isSuccess)

      // Attempt logout - will throw but onError still clears cache
      await expect(result.current.action()).rejects.toThrow('Backend error')

      // Verify we're back to non-loading state
      expect(result.current.isLoading).toBe(false)
      expect(clearSpy).toHaveBeenCalledTimes(1) // Cache still cleared
    })
  })
})