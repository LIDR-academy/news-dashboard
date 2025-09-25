import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AddNewsForm } from '../AddNewsForm'
import { NewsCategory } from '../../data/news.schema'
import type { CreateNewsRequest } from '../../data/news.schema'

describe('AddNewsForm', () => {
  const mockOnSubmit = vi.fn()
  const mockOnCancel = vi.fn()

  const defaultProps = {
    onSubmit: mockOnSubmit,
    isSubmitting: false,
    onCancel: mockOnCancel
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('Rendering', () => {
    it('should render all form fields with correct labels and placeholders', () => {
      render(<AddNewsForm {...defaultProps} />)

      // Required fields
      expect(screen.getByLabelText(/source \*/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/techcrunch, medium/i)).toBeInTheDocument()

      expect(screen.getByLabelText(/title \*/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/article title/i)).toBeInTheDocument()

      expect(screen.getByLabelText(/summary \*/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/brief summary of the article/i)).toBeInTheDocument()

      expect(screen.getByLabelText(/link \*/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/https:\/\/example\.com\/article/i)).toBeInTheDocument()

      // Optional fields
      expect(screen.getByLabelText(/image url \(optional\)/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/https:\/\/example\.com\/image\.jpg/i)).toBeInTheDocument()

      expect(screen.getByLabelText(/category \*/i)).toBeInTheDocument()
      expect(screen.getByText(/select a category/i)).toBeInTheDocument()

      expect(screen.getByLabelText(/make this article public/i)).toBeInTheDocument()
    })

    it('should render form buttons with correct labels', () => {
      render(<AddNewsForm {...defaultProps} />)

      expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /create news/i })).toBeInTheDocument()
    })

    it('should have correct form structure and accessibility attributes', () => {
      render(<AddNewsForm {...defaultProps} />)

      const form = screen.getByRole('form')
      expect(form).toBeInTheDocument()

      // Check required field attributes
      expect(screen.getByLabelText(/source \*/i)).toHaveAttribute('aria-required', 'true')
      expect(screen.getByLabelText(/title \*/i)).toHaveAttribute('aria-required', 'true')
      expect(screen.getByLabelText(/summary \*/i)).toHaveAttribute('aria-required', 'true')
      expect(screen.getByLabelText(/link \*/i)).toHaveAttribute('aria-required', 'true')
    })
  })

  describe('Form Validation', () => {
    describe('Required Fields Validation', () => {
      it('should show validation errors for empty required fields when submitting', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        const submitButton = screen.getByRole('button', { name: /create news/i })
        await user.click(submitButton)

        await waitFor(() => {
          expect(screen.getByText('Source is required')).toBeInTheDocument()
          expect(screen.getByText('Title is required')).toBeInTheDocument()
          expect(screen.getByText('Summary is required')).toBeInTheDocument()
          expect(screen.getByText('Link is required')).toBeInTheDocument()
        })

        expect(mockOnSubmit).not.toHaveBeenCalled()
      })

      it('should validate field length limits', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        // Test source length limit (100 characters)
        const sourceInput = screen.getByLabelText(/source \*/i)
        await user.clear(sourceInput)
        await user.type(sourceInput, 'A'.repeat(101))

        const submitButton = screen.getByRole('button', { name: /create news/i })
        await user.click(submitButton)

        await waitFor(() => {
          expect(screen.getByText('Source must be less than 100 characters')).toBeInTheDocument()
        })

        // Test title length limit (200 characters)
        await user.clear(sourceInput)
        await user.type(sourceInput, 'Valid source')

        const titleInput = screen.getByLabelText(/title \*/i)
        await user.type(titleInput, 'A'.repeat(201))

        await user.click(submitButton)

        await waitFor(() => {
          expect(screen.getByText('Title must be less than 200 characters')).toBeInTheDocument()
        })

        // Test summary length limit (500 characters)
        await user.clear(titleInput)
        await user.type(titleInput, 'Valid title')

        const summaryInput = screen.getByLabelText(/summary \*/i)
        await user.type(summaryInput, 'A'.repeat(501))

        await user.click(submitButton)

        await waitFor(() => {
          expect(screen.getByText('Summary must be less than 500 characters')).toBeInTheDocument()
        })
      })

      it('should validate URL format for link field', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        const linkInput = screen.getByLabelText(/link \*/i)

        // Test invalid URL
        await user.type(linkInput, 'invalid-url')

        const submitButton = screen.getByRole('button', { name: /create news/i })
        await user.click(submitButton)

        await waitFor(() => {
          expect(screen.getByText('Please enter a valid URL')).toBeInTheDocument()
        })

        expect(mockOnSubmit).not.toHaveBeenCalled()
      })

      it('should validate URL format for optional image_url field', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        // Fill required fields with valid data
        await user.type(screen.getByLabelText(/source \*/i), 'TechCrunch')
        await user.type(screen.getByLabelText(/title \*/i), 'Test Article')
        await user.type(screen.getByLabelText(/summary \*/i), 'Test summary')
        await user.type(screen.getByLabelText(/link \*/i), 'https://example.com')

        // Test invalid image URL
        const imageUrlInput = screen.getByLabelText(/image url/i)
        await user.type(imageUrlInput, 'invalid-image-url')

        const submitButton = screen.getByRole('button', { name: /create news/i })
        await user.click(submitButton)

        await waitFor(() => {
          expect(screen.getByText('Please enter a valid URL')).toBeInTheDocument()
        })

        expect(mockOnSubmit).not.toHaveBeenCalled()
      })
    })

    describe('Real-time Validation', () => {
      it('should clear validation errors when user starts typing in a field', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        // First trigger validation error
        const submitButton = screen.getByRole('button', { name: /create news/i })
        await user.click(submitButton)

        await waitFor(() => {
          expect(screen.getByText('Source is required')).toBeInTheDocument()
        })

        // Then start typing in the field
        const sourceInput = screen.getByLabelText(/source \*/i)
        await user.type(sourceInput, 'T')

        await waitFor(() => {
          expect(screen.queryByText('Source is required')).not.toBeInTheDocument()
        })
      })
    })
  })

  describe('Form Interactions', () => {
    describe('Category Selection', () => {
      it('should render all category options in the dropdown', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        const categoryTrigger = screen.getByRole('combobox')
        await user.click(categoryTrigger)

        const dropdown = screen.getByRole('listbox')
        expect(within(dropdown).getByText('General')).toBeInTheDocument()
        expect(within(dropdown).getByText('Research')).toBeInTheDocument()
        expect(within(dropdown).getByText('Product')).toBeInTheDocument()
        expect(within(dropdown).getByText('Company')).toBeInTheDocument()
        expect(within(dropdown).getByText('Tutorial')).toBeInTheDocument()
        expect(within(dropdown).getByText('Opinion')).toBeInTheDocument()
      })

      it('should select a category and update the form', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        const categoryTrigger = screen.getByRole('combobox')
        await user.click(categoryTrigger)

        const researchOption = screen.getByText('Research')
        await user.click(researchOption)

        expect(categoryTrigger).toHaveTextContent('Research')
      })

      it('should default to General category', () => {
        render(<AddNewsForm {...defaultProps} />)

        const categoryTrigger = screen.getByRole('combobox')
        expect(categoryTrigger).toHaveTextContent('General')
      })
    })

    describe('Public Checkbox', () => {
      it('should toggle public checkbox state', async () => {
        const user = userEvent.setup()
        render(<AddNewsForm {...defaultProps} />)

        const publicCheckbox = screen.getByLabelText(/make this article public/i)
        expect(publicCheckbox).not.toBeChecked()

        await user.click(publicCheckbox)
        expect(publicCheckbox).toBeChecked()

        await user.click(publicCheckbox)
        expect(publicCheckbox).not.toBeChecked()
      })

      it('should default to false for is_public', () => {
        render(<AddNewsForm {...defaultProps} />)

        const publicCheckbox = screen.getByLabelText(/make this article public/i)
        expect(publicCheckbox).not.toBeChecked()
      })
    })
  })

  describe('Form Submission', () => {
    const validFormData: CreateNewsRequest = {
      source: 'TechCrunch',
      title: 'Test Article',
      summary: 'This is a test article summary',
      link: 'https://example.com/article',
      image_url: 'https://example.com/image.jpg',
      category: NewsCategory.RESEARCH,
      is_public: true
    }

    it('should submit form with valid data', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      // Fill all fields
      await user.type(screen.getByLabelText(/source \*/i), validFormData.source)
      await user.type(screen.getByLabelText(/title \*/i), validFormData.title)
      await user.type(screen.getByLabelText(/summary \*/i), validFormData.summary)
      await user.type(screen.getByLabelText(/link \*/i), validFormData.link)
      await user.type(screen.getByLabelText(/image url/i), validFormData.image_url!)

      // Select category
      const categoryTrigger = screen.getByRole('combobox')
      await user.click(categoryTrigger)
      await user.click(screen.getByText('Research'))

      // Check public checkbox
      await user.click(screen.getByLabelText(/make this article public/i))

      // Submit form
      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith(validFormData)
      })
    })

    it('should submit form without optional fields', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      const minimalFormData = {
        source: 'TechCrunch',
        title: 'Test Article',
        summary: 'This is a test article summary',
        link: 'https://example.com/article',
        image_url: undefined, // Should be cleaned up to undefined
        category: NewsCategory.GENERAL,
        is_public: false
      }

      // Fill required fields only
      await user.type(screen.getByLabelText(/source \*/i), minimalFormData.source)
      await user.type(screen.getByLabelText(/title \*/i), minimalFormData.title)
      await user.type(screen.getByLabelText(/summary \*/i), minimalFormData.summary)
      await user.type(screen.getByLabelText(/link \*/i), minimalFormData.link)

      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith(minimalFormData)
      })
    })

    it('should clean up empty image_url field before submission', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      // Fill required fields and leave image_url as empty string
      await user.type(screen.getByLabelText(/source \*/i), 'TechCrunch')
      await user.type(screen.getByLabelText(/title \*/i), 'Test Article')
      await user.type(screen.getByLabelText(/summary \*/i), 'Test summary')
      await user.type(screen.getByLabelText(/link \*/i), 'https://example.com')

      // Type something then delete it to have empty string
      const imageUrlInput = screen.getByLabelText(/image url/i)
      await user.type(imageUrlInput, 'test')
      await user.clear(imageUrlInput)

      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith(
          expect.objectContaining({
            image_url: undefined
          })
        )
      })
    })
  })

  describe('Form States', () => {
    it('should disable submit button when form is invalid', () => {
      render(<AddNewsForm {...defaultProps} />)

      const submitButton = screen.getByRole('button', { name: /create news/i })
      expect(submitButton).toBeDisabled()
    })

    it('should enable submit button when all required fields are filled', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      const submitButton = screen.getByRole('button', { name: /create news/i })
      expect(submitButton).toBeDisabled()

      // Fill all required fields
      await user.type(screen.getByLabelText(/source \*/i), 'TechCrunch')
      await user.type(screen.getByLabelText(/title \*/i), 'Test Article')
      await user.type(screen.getByLabelText(/summary \*/i), 'Test summary')
      await user.type(screen.getByLabelText(/link \*/i), 'https://example.com')

      await waitFor(() => {
        expect(submitButton).toBeEnabled()
      })
    })

    it('should disable buttons and show loading state when submitting', () => {
      render(<AddNewsForm {...defaultProps} isSubmitting={true} />)

      const submitButton = screen.getByRole('button', { name: /creating\.\.\./i })
      const cancelButton = screen.getByRole('button', { name: /cancel/i })

      expect(submitButton).toBeDisabled()
      expect(cancelButton).toBeDisabled()
      expect(submitButton).toHaveTextContent('Creating...')
    })
  })

  describe('Form Actions', () => {
    it('should call onCancel when cancel button is clicked', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      const cancelButton = screen.getByRole('button', { name: /cancel/i })
      await user.click(cancelButton)

      expect(mockOnCancel).toHaveBeenCalledTimes(1)
    })

    it('should not call onCancel when cancel button is disabled during submission', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} isSubmitting={true} />)

      const cancelButton = screen.getByRole('button', { name: /cancel/i })

      // Try to click disabled button
      await user.click(cancelButton)

      expect(mockOnCancel).not.toHaveBeenCalled()
    })
  })

  describe('Accessibility', () => {
    it('should have proper ARIA attributes for form validation', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      // Trigger validation
      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      await waitFor(() => {
        const sourceInput = screen.getByLabelText(/source \*/i)
        expect(sourceInput).toHaveAttribute('aria-invalid', 'true')
      })

      // Check error messages have role="alert"
      const errorMessage = screen.getByText('Source is required')
      expect(errorMessage).toHaveAttribute('role', 'alert')
    })

    it('should update aria-invalid when validation state changes', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      const sourceInput = screen.getByLabelText(/source \*/i)

      // Initially should be valid
      expect(sourceInput).toHaveAttribute('aria-invalid', 'false')

      // Trigger validation error
      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(sourceInput).toHaveAttribute('aria-invalid', 'true')
      })

      // Fix the error
      await user.type(sourceInput, 'Valid source')

      await waitFor(() => {
        expect(sourceInput).toHaveAttribute('aria-invalid', 'false')
      })
    })
  })

  describe('Edge Cases', () => {
    it('should handle whitespace-only input as empty for required fields', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      // Fill with whitespace only
      await user.type(screen.getByLabelText(/source \*/i), '   ')

      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(screen.getByText('Source is required')).toBeInTheDocument()
      })
    })

    it('should handle special characters in URLs', async () => {
      const user = userEvent.setup()
      render(<AddNewsForm {...defaultProps} />)

      // Fill required fields
      await user.type(screen.getByLabelText(/source \*/i), 'TechCrunch')
      await user.type(screen.getByLabelText(/title \*/i), 'Test Article')
      await user.type(screen.getByLabelText(/summary \*/i), 'Test summary')

      // URL with special characters
      const complexUrl = 'https://example.com/article?id=123&category=tech#section1'
      await user.type(screen.getByLabelText(/link \*/i), complexUrl)

      const submitButton = screen.getByRole('button', { name: /create news/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith(
          expect.objectContaining({
            link: complexUrl
          })
        )
      })
    })

    it('should handle form reset when component unmounts during submission', () => {
      const { unmount } = render(<AddNewsForm {...defaultProps} isSubmitting={true} />)

      // Should not throw errors when unmounting during submission
      expect(() => unmount()).not.toThrow()
    })
  })
})