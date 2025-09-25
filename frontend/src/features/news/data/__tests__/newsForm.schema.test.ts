import { describe, it, expect } from 'vitest'
import { createNewsFormSchema, CATEGORY_OPTIONS, type CreateNewsFormData } from '../newsForm.schema'
import { NewsCategory } from '../news.schema'

describe('newsForm.schema', () => {
  describe('createNewsFormSchema', () => {
    describe('source field validation', () => {
      it('should validate required source field', () => {
        const result = createNewsFormSchema.safeParse({
          source: '',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['source'],
              message: 'Source is required'
            })
          )
        }
      })

      it('should validate source minimum length', () => {
        const result = createNewsFormSchema.safeParse({
          source: '',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['source'],
              message: 'Source is required'
            })
          )
        }
      })

      it('should validate source maximum length (100 characters)', () => {
        const longSource = 'A'.repeat(101)
        const result = createNewsFormSchema.safeParse({
          source: longSource,
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['source'],
              message: 'Source must be less than 100 characters'
            })
          )
        }
      })

      it('should accept valid source within length limits', () => {
        const validSource = 'TechCrunch'
        const result = createNewsFormSchema.safeParse({
          source: validSource,
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.source).toBe(validSource)
        }
      })

      it('should accept source at maximum length limit (100 characters)', () => {
        const maxLengthSource = 'A'.repeat(100)
        const result = createNewsFormSchema.safeParse({
          source: maxLengthSource,
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.source).toBe(maxLengthSource)
        }
      })
    })

    describe('title field validation', () => {
      it('should validate required title field', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: '',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['title'],
              message: 'Title is required'
            })
          )
        }
      })

      it('should validate title maximum length (200 characters)', () => {
        const longTitle = 'A'.repeat(201)
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: longTitle,
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['title'],
              message: 'Title must be less than 200 characters'
            })
          )
        }
      })

      it('should accept valid title within length limits', () => {
        const validTitle = 'Breaking: New Technology Announcement'
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: validTitle,
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.title).toBe(validTitle)
        }
      })

      it('should accept title at maximum length limit (200 characters)', () => {
        const maxLengthTitle = 'A'.repeat(200)
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: maxLengthTitle,
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.title).toBe(maxLengthTitle)
        }
      })
    })

    describe('summary field validation', () => {
      it('should validate required summary field', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: '',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['summary'],
              message: 'Summary is required'
            })
          )
        }
      })

      it('should validate summary maximum length (500 characters)', () => {
        const longSummary = 'A'.repeat(501)
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: longSummary,
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['summary'],
              message: 'Summary must be less than 500 characters'
            })
          )
        }
      })

      it('should accept valid summary within length limits', () => {
        const validSummary = 'This is a detailed summary of the news article content that provides valuable information.'
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: validSummary,
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.summary).toBe(validSummary)
        }
      })

      it('should accept summary at maximum length limit (500 characters)', () => {
        const maxLengthSummary = 'A'.repeat(500)
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: maxLengthSummary,
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.summary).toBe(maxLengthSummary)
        }
      })
    })

    describe('link field validation', () => {
      it('should validate required link field', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: '',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['link'],
              message: 'Please enter a valid URL'
            })
          )
        }
      })

      it('should validate proper URL format', () => {
        const invalidUrls = [
          'not-a-url',
          'ftp://invalid-protocol.com',
          'javascript:alert("test")',
          'www.no-protocol.com',
          'http://',
          'https://',
          'https://.',
          'https://.com'
        ]

        invalidUrls.forEach(invalidUrl => {
          const result = createNewsFormSchema.safeParse({
            source: 'TechCrunch',
            title: 'Test Title',
            summary: 'Test Summary',
            link: invalidUrl,
            category: NewsCategory.GENERAL,
            is_public: false
          })

          expect(result.success).toBe(false)
          if (!result.success) {
            const hasUrlError = result.error.issues.some(issue =>
              issue.path.includes('link') &&
              (issue.message === 'Please enter a valid URL' || issue.message === 'Invalid URL format')
            )
            expect(hasUrlError).toBe(true)
          }
        })
      })

      it('should accept valid HTTP and HTTPS URLs', () => {
        const validUrls = [
          'https://example.com',
          'http://example.com',
          'https://www.example.com',
          'https://subdomain.example.com',
          'https://example.com/path',
          'https://example.com/path?query=value',
          'https://example.com/path?query=value&other=test',
          'https://example.com/path#fragment',
          'https://example.com:8080/path',
          'https://192.168.1.1:3000',
          'https://localhost:3000',
          'https://example-site.co.uk',
          'https://example.com/path/with-hyphens_and_underscores'
        ]

        validUrls.forEach(validUrl => {
          const result = createNewsFormSchema.safeParse({
            source: 'TechCrunch',
            title: 'Test Title',
            summary: 'Test Summary',
            link: validUrl,
            category: NewsCategory.GENERAL,
            is_public: false
          })

          expect(result.success).toBe(true)
          if (result.success) {
            expect(result.data.link).toBe(validUrl)
          }
        })
      })

      it('should use both URL validation and custom refine validation', () => {
        // Test that both URL string validation and custom refine work together
        const malformedUrl = 'https://[invalid-brackets'
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: malformedUrl,
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          const hasUrlError = result.error.issues.some(issue =>
            issue.path.includes('link')
          )
          expect(hasUrlError).toBe(true)
        }
      })
    })

    describe('image_url field validation', () => {
      it('should accept empty image_url as optional field', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          image_url: '',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.image_url).toBe('')
        }
      })

      it('should accept undefined image_url', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.image_url).toBeUndefined()
        }
      })

      it('should validate URL format when image_url is provided', () => {
        const invalidImageUrls = [
          'not-a-url',
          'ftp://invalid-protocol.com/image.jpg',
          'javascript:alert("test")',
          'data:image/png;base64,invalid'
        ]

        invalidImageUrls.forEach(invalidUrl => {
          const result = createNewsFormSchema.safeParse({
            source: 'TechCrunch',
            title: 'Test Title',
            summary: 'Test Summary',
            link: 'https://example.com',
            image_url: invalidUrl,
            category: NewsCategory.GENERAL,
            is_public: false
          })

          expect(result.success).toBe(false)
          if (!result.success) {
            expect(result.error.issues).toContainEqual(
              expect.objectContaining({
                path: ['image_url'],
                message: 'Please enter a valid image URL'
              })
            )
          }
        })
      })

      it('should accept valid image URLs', () => {
        const validImageUrls = [
          'https://example.com/image.jpg',
          'https://example.com/image.png',
          'https://example.com/image.gif',
          'https://cdn.example.com/path/to/image.webp',
          'https://images.unsplash.com/photo-123?ixlib=rb-4.0.3'
        ]

        validImageUrls.forEach(validUrl => {
          const result = createNewsFormSchema.safeParse({
            source: 'TechCrunch',
            title: 'Test Title',
            summary: 'Test Summary',
            link: 'https://example.com',
            image_url: validUrl,
            category: NewsCategory.GENERAL,
            is_public: false
          })

          expect(result.success).toBe(true)
          if (result.success) {
            expect(result.data.image_url).toBe(validUrl)
          }
        })
      })
    })

    describe('category field validation', () => {
      it('should validate required category field', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          is_public: false
        })

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues).toContainEqual(
            expect.objectContaining({
              path: ['category'],
              message: 'Please select a category'
            })
          )
        }
      })

      it('should accept all valid NewsCategory enum values', () => {
        const validCategories = Object.values(NewsCategory)

        validCategories.forEach(category => {
          const result = createNewsFormSchema.safeParse({
            source: 'TechCrunch',
            title: 'Test Title',
            summary: 'Test Summary',
            link: 'https://example.com',
            category: category,
            is_public: false
          })

          expect(result.success).toBe(true)
          if (result.success) {
            expect(result.data.category).toBe(category)
          }
        })
      })

      it('should reject invalid category values', () => {
        const invalidCategories = [
          'invalid-category',
          'INVALID',
          '',
          null,
          undefined,
          123,
          {}
        ]

        invalidCategories.forEach(invalidCategory => {
          const result = createNewsFormSchema.safeParse({
            source: 'TechCrunch',
            title: 'Test Title',
            summary: 'Test Summary',
            link: 'https://example.com',
            category: invalidCategory,
            is_public: false
          })

          expect(result.success).toBe(false)
        })
      })
    })

    describe('is_public field validation', () => {
      it('should accept boolean true value', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: true
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.is_public).toBe(true)
        }
      })

      it('should accept boolean false value', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.is_public).toBe(false)
        }
      })

      it('should default to false when is_public is not provided', () => {
        const result = createNewsFormSchema.safeParse({
          source: 'TechCrunch',
          title: 'Test Title',
          summary: 'Test Summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL
        })

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data.is_public).toBe(false)
        }
      })

      it('should reject non-boolean values', () => {
        const invalidValues = ['true', 'false', 1, 0, null, undefined, {}, []]

        invalidValues.forEach(invalidValue => {
          const result = createNewsFormSchema.safeParse({
            source: 'TechCrunch',
            title: 'Test Title',
            summary: 'Test Summary',
            link: 'https://example.com',
            category: NewsCategory.GENERAL,
            is_public: invalidValue
          })

          expect(result.success).toBe(false)
        })
      })
    })

    describe('complete form validation', () => {
      it('should validate a complete valid form', () => {
        const validFormData: CreateNewsFormData = {
          source: 'TechCrunch',
          title: 'Breaking: New Technology Breakthrough',
          summary: 'Scientists have made a significant breakthrough in quantum computing that could revolutionize the industry.',
          link: 'https://techcrunch.com/2024/01/15/quantum-breakthrough',
          image_url: 'https://techcrunch.com/images/quantum-computer.jpg',
          category: NewsCategory.RESEARCH,
          is_public: true
        }

        const result = createNewsFormSchema.safeParse(validFormData)

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data).toEqual(validFormData)
        }
      })

      it('should validate minimal valid form (required fields only)', () => {
        const minimalFormData: CreateNewsFormData = {
          source: 'TechCrunch',
          title: 'Test Article',
          summary: 'Test summary',
          link: 'https://example.com',
          category: NewsCategory.GENERAL,
          is_public: false
        }

        const result = createNewsFormSchema.safeParse(minimalFormData)

        expect(result.success).toBe(true)
        if (result.success) {
          expect(result.data).toEqual(minimalFormData)
        }
      })

      it('should collect multiple validation errors', () => {
        const invalidFormData = {
          source: '',
          title: '',
          summary: '',
          link: 'invalid-url',
          image_url: 'invalid-image-url',
          category: 'invalid-category',
          is_public: 'not-boolean'
        }

        const result = createNewsFormSchema.safeParse(invalidFormData)

        expect(result.success).toBe(false)
        if (!result.success) {
          expect(result.error.issues.length).toBeGreaterThan(1)

          // Check that we get errors for all invalid fields
          const errorPaths = result.error.issues.map(issue => issue.path[0])
          expect(errorPaths).toContain('source')
          expect(errorPaths).toContain('title')
          expect(errorPaths).toContain('summary')
          expect(errorPaths).toContain('link')
          expect(errorPaths).toContain('image_url')
          expect(errorPaths).toContain('category')
          expect(errorPaths).toContain('is_public')
        }
      })
    })

    describe('TypeScript type inference', () => {
      it('should infer correct TypeScript type', () => {
        const validData = {
          source: 'TechCrunch',
          title: 'Test Article',
          summary: 'Test summary',
          link: 'https://example.com',
          image_url: 'https://example.com/image.jpg',
          category: NewsCategory.GENERAL,
          is_public: true
        }

        const result = createNewsFormSchema.safeParse(validData)

        if (result.success) {
          // TypeScript should infer the correct type
          const data: CreateNewsFormData = result.data

          expect(typeof data.source).toBe('string')
          expect(typeof data.title).toBe('string')
          expect(typeof data.summary).toBe('string')
          expect(typeof data.link).toBe('string')
          expect(typeof data.image_url).toBe('string')
          expect(Object.values(NewsCategory)).toContain(data.category)
          expect(typeof data.is_public).toBe('boolean')
        }
      })
    })
  })

  describe('CATEGORY_OPTIONS', () => {
    it('should contain all NewsCategory enum values', () => {
      const categoryValues = CATEGORY_OPTIONS.map(option => option.value)
      const enumValues = Object.values(NewsCategory)

      expect(categoryValues).toHaveLength(enumValues.length)
      enumValues.forEach(enumValue => {
        expect(categoryValues).toContain(enumValue)
      })
    })

    it('should have proper label-value structure', () => {
      CATEGORY_OPTIONS.forEach(option => {
        expect(option).toHaveProperty('value')
        expect(option).toHaveProperty('label')
        expect(typeof option.value).toBe('string')
        expect(typeof option.label).toBe('string')
        expect(option.label.length).toBeGreaterThan(0)
      })
    })

    it('should have meaningful labels for each category', () => {
      const expectedOptions = [
        { value: NewsCategory.GENERAL, label: 'General' },
        { value: NewsCategory.RESEARCH, label: 'Research' },
        { value: NewsCategory.PRODUCT, label: 'Product' },
        { value: NewsCategory.COMPANY, label: 'Company' },
        { value: NewsCategory.TUTORIAL, label: 'Tutorial' },
        { value: NewsCategory.OPINION, label: 'Opinion' }
      ]

      expect(CATEGORY_OPTIONS).toEqual(expectedOptions)
    })

    it('should not have duplicate values', () => {
      const values = CATEGORY_OPTIONS.map(option => option.value)
      const uniqueValues = [...new Set(values)]
      expect(values).toHaveLength(uniqueValues.length)
    })

    it('should not have duplicate labels', () => {
      const labels = CATEGORY_OPTIONS.map(option => option.label)
      const uniqueLabels = [...new Set(labels)]
      expect(labels).toHaveLength(uniqueLabels.length)
    })
  })

  describe('schema integration with forms', () => {
    it('should work with form libraries for validation', () => {
      // Simulate what a form library might do
      const formData = {
        source: 'T', // Too short to be meaningful but technically valid
        title: 'T', // Too short to be meaningful but technically valid
        summary: 'T', // Too short to be meaningful but technically valid
        link: 'https://t.co', // Valid but very short URL
        category: NewsCategory.GENERAL,
        is_public: false
      }

      const result = createNewsFormSchema.safeParse(formData)
      expect(result.success).toBe(true) // All fields meet minimum requirements
    })

    it('should provide detailed error information for form field highlighting', () => {
      const invalidData = {
        source: 'A'.repeat(101), // Too long
        title: 'A'.repeat(201), // Too long
        summary: 'A'.repeat(501), // Too long
        link: 'invalid',
        image_url: 'invalid',
        category: 'invalid',
        is_public: 'invalid'
      }

      const result = createNewsFormSchema.safeParse(invalidData)
      expect(result.success).toBe(false)

      if (!result.success) {
        result.error.issues.forEach(issue => {
          expect(issue).toHaveProperty('path')
          expect(issue).toHaveProperty('message')
          expect(issue).toHaveProperty('code')
          expect(Array.isArray(issue.path)).toBe(true)
          expect(typeof issue.message).toBe('string')
        })
      }
    })
  })
})