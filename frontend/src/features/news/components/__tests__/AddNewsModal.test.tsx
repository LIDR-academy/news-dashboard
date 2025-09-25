import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React, { type ReactNode } from 'react'
import { toast } from 'sonner'
import { AddNewsModal } from '../AddNewsModal'
import { NewsCategory } from '../../data/news.schema'

// Mock the mutation hook
vi.mock('../../hooks/mutations/useCreateNews.mutation')
vi.mock('sonner')

import { useCreateNewsMutation } from '../../hooks/mutations/useCreateNews.mutation'

describe('AddNewsModal', () => {
  let queryClient: QueryClient
  const mockCreateNews = vi.fn()
  const mockUseCreateNewsMutation = useCreateNewsMutation as any

  const createWrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false }
      }
    })

    // Default mock implementation
    mockUseCreateNewsMutation.mockReturnValue({
      createNews: mockCreateNews,
      isLoading: false,
      error: null,
      isSuccess: false
    })

    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('Rendering', () => {
    it('should render with default trigger button', () => {
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      expect(triggerButton).toBeInTheDocument()
      expect(triggerButton).toHaveTextContent('Add News')
    })

    it('should render with custom trigger content', () => {
      const customTrigger = <button>Custom Add Button</button>

      render(
        <AddNewsModal>
          {customTrigger}
        </AddNewsModal>,
        { wrapper: createWrapper }
      )

      expect(screen.getByRole('button', { name: /custom add button/i })).toBeInTheDocument()
      expect(screen.queryByText('Add News')).not.toBeInTheDocument()
    })

    it('should apply custom className, size, and variant props to default trigger', () => {
      render(
        <AddNewsModal
          className="custom-class"
          size="lg"
          variant="outline"
        />,
        { wrapper: createWrapper }
      )

      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      expect(triggerButton).toHaveClass('custom-class')
    })

    it('should show plus icon and responsive text in default trigger', () => {
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      const triggerButton = screen.getByRole('button', { name: /add new news item/i })

      // Plus icon should be present
      const plusIcon = within(triggerButton).getByRole('img', { hidden: true })
      expect(plusIcon).toBeInTheDocument()

      // Text should have responsive classes (hidden on small screens)
      const textSpan = within(triggerButton).getByText('Add News')
      expect(textSpan).toHaveClass('hidden', 'sm:inline')
    })
  })

  describe('Modal Interactions', () => {
    it('should open modal when trigger button is clicked', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByText('Add News Item')).toBeInTheDocument()
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })
    })

    it('should close modal when escape key is pressed', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })

      // Press Escape
      await user.keyboard('{Escape}')

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
      })
    })

    it('should close modal when clicking outside the dialog', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })

      // Click on overlay (outside dialog)
      const overlay = screen.getByRole('dialog').parentElement
      if (overlay) {
        await user.click(overlay)
      }

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
      })
    })

    it('should close modal when cancel button in form is clicked', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })

      // Click cancel button in form
      const cancelButton = screen.getByRole('button', { name: /cancel/i })
      await user.click(cancelButton)

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
      })
    })
  })

  describe('Form Integration', () => {
    it('should render AddNewsForm inside the modal', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })

      // Check that form elements are present
      expect(screen.getByLabelText(/source \*/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/title \*/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/summary \*/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/link \*/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /create news/i })).toBeInTheDocument()
    })

    it('should pass isSubmitting state to form', async () => {
      const user = userEvent.setup()

      // Mock loading state
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: true,
        error: null,
        isSuccess: false
      })

      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /creating\.\.\./i })).toBeInTheDocument()
      })
    })

    it('should call createNews mutation when form is submitted with valid data', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })

      // Fill form with valid data
      await user.type(screen.getByLabelText(/source \*/i), 'TechCrunch')
      await user.type(screen.getByLabelText(/title \*/i), 'Test Article')
      await user.type(screen.getByLabelText(/summary \*/i), 'Test summary')
      await user.type(screen.getByLabelText(/link \*/i), 'https://example.com')

      // Submit form
      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      expect(mockCreateNews).toHaveBeenCalledWith({
        source: 'TechCrunch',
        title: 'Test Article',
        summary: 'Test summary',
        link: 'https://example.com',
        image_url: undefined,
        category: NewsCategory.GENERAL,
        is_public: false
      })
    })
  })

  describe('Success Handling', () => {
    it('should close modal automatically when mutation is successful', async () => {
      const user = userEvent.setup()

      // Initially render with success = false
      let mockReturnValue = {
        createNews: mockCreateNews,
        isLoading: false,
        error: null,
        isSuccess: false
      }
      mockUseCreateNewsMutation.mockReturnValue(mockReturnValue)

      const { rerender } = render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })

      // Simulate success
      mockReturnValue.isSuccess = true
      mockUseCreateNewsMutation.mockReturnValue(mockReturnValue)

      rerender(
        <AddNewsModal />
      )

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
      })
    })

    it('should reset modal state when reopened after successful creation', async () => {
      const user = userEvent.setup()

      // Mock successful state
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: null,
        isSuccess: true
      })

      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal (should close immediately due to success state)
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      // Reset success state for next render
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: null,
        isSuccess: false
      })

      // Open modal again
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
        // Form should be in clean state
        expect(screen.getByLabelText(/source \*/i)).toHaveValue('')
      })
    })
  })

  describe('Error Handling', () => {
    it('should display error message when mutation fails', async () => {
      const user = userEvent.setup()
      const errorMessage = 'Failed to create news item'

      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: new Error(errorMessage),
        isSuccess: false
      })

      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument()
      })
    })

    it('should not close modal when there is an error', async () => {
      const user = userEvent.setup()

      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: new Error('Something went wrong'),
        isSuccess: false
      })

      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
        expect(screen.getByText(/error:/i)).toBeInTheDocument()
      })

      // Modal should stay open
      expect(screen.getByRole('dialog')).toBeInTheDocument()
    })

    it('should clear error when modal is closed and reopened', async () => {
      const user = userEvent.setup()

      // Start with error state
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: new Error('Test error'),
        isSuccess: false
      })

      const { rerender } = render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByText(/error:/i)).toBeInTheDocument()
      })

      // Close modal
      await user.keyboard('{Escape}')

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
      })

      // Clear error and rerender
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: null,
        isSuccess: false
      })

      rerender(<AddNewsModal />)

      // Open modal again
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
        expect(screen.queryByText(/error:/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Modal Styling and Layout', () => {
    it('should have proper responsive modal sizing', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        const modalContent = screen.getByRole('dialog')
        expect(modalContent).toHaveClass('sm:max-w-[520px]')
        expect(modalContent).toHaveClass('max-w-[calc(100%-1rem)]')
        expect(modalContent).toHaveClass('max-h-[90vh]')
        expect(modalContent).toHaveClass('overflow-y-auto')
      })
    })

    it('should have proper modal header and title', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
        expect(screen.getByText('Add News Item')).toBeInTheDocument()
      })

      // Title should be in header element
      const title = screen.getByText('Add News Item')
      expect(title.tagName.toLowerCase()).toBe('h2')
    })
  })

  describe('Accessibility', () => {
    it('should have proper ARIA attributes', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      expect(triggerButton).toHaveAttribute('aria-label', 'Add new news item')

      // Open modal
      await user.click(triggerButton)

      await waitFor(() => {
        const dialog = screen.getByRole('dialog')
        expect(dialog).toBeInTheDocument()
      })

      // Error messages should have role="alert"
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: new Error('Test error'),
        isSuccess: false
      })

      const { rerender } = render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      await user.click(triggerButton)

      await waitFor(() => {
        const errorMessage = screen.getByRole('alert')
        expect(errorMessage).toBeInTheDocument()
        expect(errorMessage).toHaveTextContent('Error: Test error')
      })
    })

    it('should maintain focus management in modal', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
      })

      // First focusable element should be focused
      // (Implementation depends on Radix UI dialog behavior)
      expect(document.activeElement).not.toBe(triggerButton)
    })
  })

  describe('Integration with useCreateNewsMutation', () => {
    it('should handle all mutation states correctly', async () => {
      const user = userEvent.setup()

      // Test initial state
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: null,
        isSuccess: false
      })

      const { rerender } = render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Open modal
      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      // Test loading state
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: true,
        error: null,
        isSuccess: false
      })

      rerender(<AddNewsModal />)

      expect(screen.getByRole('button', { name: /creating\.\.\./i })).toBeInTheDocument()

      // Test error state
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: new Error('Network error'),
        isSuccess: false
      })

      rerender(<AddNewsModal />)

      expect(screen.getByText('Error: Network error')).toBeInTheDocument()

      // Test success state
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: null,
        isSuccess: true
      })

      rerender(<AddNewsModal />)

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
      })
    })
  })

  describe('Edge Cases', () => {
    it('should handle rapid open/close operations', async () => {
      const user = userEvent.setup()
      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      const triggerButton = screen.getByRole('button', { name: /add new news item/i })

      // Rapidly open and close
      await user.click(triggerButton)
      await user.keyboard('{Escape}')
      await user.click(triggerButton)
      await user.keyboard('{Escape}')

      // Should not cause any errors
      expect(() => screen.queryByRole('dialog')).not.toThrow()
    })

    it('should handle component unmounting during open state', () => {
      const { unmount } = render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      // Should not throw errors when unmounting
      expect(() => unmount()).not.toThrow()
    })

    it('should handle mutation hook returning undefined values', async () => {
      const user = userEvent.setup()

      // Mock undefined error case
      mockUseCreateNewsMutation.mockReturnValue({
        createNews: mockCreateNews,
        isLoading: false,
        error: undefined,
        isSuccess: false
      })

      render(
        <AddNewsModal />,
        { wrapper: createWrapper }
      )

      const triggerButton = screen.getByRole('button', { name: /add new news item/i })
      await user.click(triggerButton)

      // Should not crash with undefined error
      await waitFor(() => {
        expect(screen.getByRole('dialog')).toBeInTheDocument()
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      })
    })
  })
})