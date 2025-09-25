import { z } from 'zod';
import { NewsCategory } from './news.schema';

export const createNewsFormSchema = z.object({
  source: z.string()
    .min(1, 'Source is required')
    .max(100, 'Source must be less than 100 characters'),

  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters'),

  summary: z.string()
    .min(1, 'Summary is required')
    .max(500, 'Summary must be less than 500 characters'),

  link: z.string()
    .url('Please enter a valid URL')
    .refine((url) => {
      try {
        new URL(url);
        return true;
      } catch {
        return false;
      }
    }, 'Invalid URL format'),

  image_url: z.string()
    .url('Please enter a valid image URL')
    .optional()
    .or(z.literal('')), // Allow empty string

  category: z.nativeEnum(NewsCategory, {
    required_error: 'Please select a category'
  }),

  is_public: z.boolean().default(false)
});

export type CreateNewsFormData = z.infer<typeof createNewsFormSchema>;

// Category options for dropdown
export const CATEGORY_OPTIONS = [
  { value: NewsCategory.GENERAL, label: 'General' },
  { value: NewsCategory.RESEARCH, label: 'Research' },
  { value: NewsCategory.PRODUCT, label: 'Product' },
  { value: NewsCategory.COMPANY, label: 'Company' },
  { value: NewsCategory.TUTORIAL, label: 'Tutorial' },
  { value: NewsCategory.OPINION, label: 'Opinion' }
];