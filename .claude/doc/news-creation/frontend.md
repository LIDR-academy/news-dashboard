# NEWS-9: Add News Creation Functionality - Frontend Implementation Plan

## Overview
This document outlines the detailed implementation plan for adding news creation functionality to the existing news feature. The implementation follows the project's established feature-based architecture with React Query patterns.

## Current Architecture Analysis

### Existing Components Structure
```
src/features/news/
├── components/
│   ├── NewsBoard.tsx       # Main Kanban board with mobile responsive design
│   ├── NewsCard.tsx        # Individual news item display
│   ├── NewsColumn.tsx      # Column container for Kanban board
│   ├── NewsFilters.tsx     # Filter controls
│   ├── NewsMobileView.tsx  # Mobile-optimized view
│   └── NewsStats.tsx       # Statistics display
├── data/
│   ├── news.schema.ts      # TypeScript interfaces and Zod schemas
│   └── news.service.ts     # API service functions
└── hooks/
    ├── mutations/
    │   ├── useCreateNews.mutation.ts     # ✅ EXISTS - Ready for use
    │   ├── useToggleFavorite.mutation.ts
    │   └── useUpdateStatus.mutation.ts
    ├── queries/
    │   ├── useNewsStats.query.ts
    │   ├── usePublicNews.query.ts
    │   └── useUserNews.query.ts
    └── useNewsContext.tsx    # Context provider for news state management
```

### Key Existing Assets
1. **`useCreateNewsMutation`** - Already implemented and ready to use
2. **`CreateNewsRequest` interface** - Schema already defined in news.schema.ts
3. **`NewsCategory` enum** - Available categories for dropdown
4. **NewsColumn component** - Target location for Add button
5. **Dialog, Button, Input, Select** - UI components available

## Implementation Plan

### Phase 1: Form Validation Schema (Zod)

**File**: `src/features/news/data/newsForm.schema.ts`
```typescript
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
```

### Phase 2: News Creation Form Component

**File**: `src/features/news/components/AddNewsForm.tsx`
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { createNewsFormSchema, type CreateNewsFormData, CATEGORY_OPTIONS } from '../data/newsForm.schema';

interface AddNewsFormProps {
  onSubmit: (data: CreateNewsFormData) => void;
  isSubmitting: boolean;
  onCancel: () => void;
}

export const AddNewsForm = ({ onSubmit, isSubmitting, onCancel }: AddNewsFormProps) => {
  const form = useForm<CreateNewsFormData>({
    resolver: zodResolver(createNewsFormSchema),
    defaultValues: {
      source: '',
      title: '',
      summary: '',
      link: '',
      image_url: '',
      category: undefined,
      is_public: false
    }
  });

  const handleSubmit = (data: CreateNewsFormData) => {
    // Clean up empty image_url
    const cleanedData = {
      ...data,
      image_url: data.image_url?.trim() || undefined
    };
    onSubmit(cleanedData);
  };

  return (
    <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
      {/* Source Field */}
      <div className="space-y-2">
        <Label htmlFor="source">Source *</Label>
        <Input
          id="source"
          placeholder="e.g., TechCrunch, Medium, etc."
          {...form.register('source')}
          aria-invalid={!!form.formState.errors.source}
        />
        {form.formState.errors.source && (
          <p className="text-sm text-destructive" role="alert">
            {form.formState.errors.source.message}
          </p>
        )}
      </div>

      {/* Title Field */}
      <div className="space-y-2">
        <Label htmlFor="title">Title *</Label>
        <Input
          id="title"
          placeholder="Article title"
          {...form.register('title')}
          aria-invalid={!!form.formState.errors.title}
        />
        {form.formState.errors.title && (
          <p className="text-sm text-destructive" role="alert">
            {form.formState.errors.title.message}
          </p>
        )}
      </div>

      {/* Summary Field */}
      <div className="space-y-2">
        <Label htmlFor="summary">Summary *</Label>
        <textarea
          id="summary"
          className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          placeholder="Brief summary of the article"
          {...form.register('summary')}
          aria-invalid={!!form.formState.errors.summary}
        />
        {form.formState.errors.summary && (
          <p className="text-sm text-destructive" role="alert">
            {form.formState.errors.summary.message}
          </p>
        )}
      </div>

      {/* Link Field */}
      <div className="space-y-2">
        <Label htmlFor="link">Link *</Label>
        <Input
          id="link"
          type="url"
          placeholder="https://example.com/article"
          {...form.register('link')}
          aria-invalid={!!form.formState.errors.link}
        />
        {form.formState.errors.link && (
          <p className="text-sm text-destructive" role="alert">
            {form.formState.errors.link.message}
          </p>
        )}
      </div>

      {/* Image URL Field */}
      <div className="space-y-2">
        <Label htmlFor="image_url">Image URL (optional)</Label>
        <Input
          id="image_url"
          type="url"
          placeholder="https://example.com/image.jpg"
          {...form.register('image_url')}
          aria-invalid={!!form.formState.errors.image_url}
        />
        {form.formState.errors.image_url && (
          <p className="text-sm text-destructive" role="alert">
            {form.formState.errors.image_url.message}
          </p>
        )}
      </div>

      {/* Category Field */}
      <div className="space-y-2">
        <Label htmlFor="category">Category *</Label>
        <Select
          value={form.watch('category')}
          onValueChange={(value) => form.setValue('category', value as any)}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select a category" />
          </SelectTrigger>
          <SelectContent>
            {CATEGORY_OPTIONS.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {form.formState.errors.category && (
          <p className="text-sm text-destructive" role="alert">
            {form.formState.errors.category.message}
          </p>
        )}
      </div>

      {/* Public Checkbox */}
      <div className="flex items-center space-x-2">
        <Checkbox
          id="is_public"
          checked={form.watch('is_public')}
          onCheckedChange={(checked) => form.setValue('is_public', checked as boolean)}
        />
        <Label
          htmlFor="is_public"
          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          Make this article public
        </Label>
      </div>

      {/* Form Actions */}
      <div className="flex justify-end space-x-2 pt-4">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={isSubmitting || !form.formState.isValid}
        >
          {isSubmitting ? 'Creating...' : 'Create News'}
        </Button>
      </div>
    </form>
  );
};
```

### Phase 3: News Creation Modal Component

**File**: `src/features/news/components/AddNewsModal.tsx`
```typescript
import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import { AddNewsForm } from './AddNewsForm';
import { useCreateNewsMutation } from '../hooks/mutations/useCreateNews.mutation';
import type { CreateNewsFormData } from '../data/newsForm.schema';

interface AddNewsModalProps {
  className?: string;
}

export const AddNewsModal = ({ className }: AddNewsModalProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const { createNews, isLoading, error, isSuccess } = useCreateNewsMutation();

  const handleSubmit = (data: CreateNewsFormData) => {
    createNews(data);
  };

  // Close modal on successful creation
  if (isSuccess && isOpen) {
    setIsOpen(false);
  }

  const handleCancel = () => {
    setIsOpen(false);
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button
          size="sm"
          className={className}
          aria-label="Add new news item"
        >
          <Plus className="w-4 h-4" />
          <span className="hidden sm:inline">Add News</span>
        </Button>
      </DialogTrigger>

      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Add New News Item</DialogTitle>
        </DialogHeader>

        <AddNewsForm
          onSubmit={handleSubmit}
          isSubmitting={isLoading}
          onCancel={handleCancel}
        />

        {error && (
          <div className="mt-4 p-3 rounded-md bg-destructive/10 border border-destructive/20">
            <p className="text-sm text-destructive" role="alert">
              Error: {error.message}
            </p>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};
```

### Phase 4: NewsColumn Integration

**File**: Update `src/features/news/components/NewsColumn.tsx`

Add the import and button to the "To Read" column header:

```typescript
// Add to imports
import { AddNewsModal } from './AddNewsModal';
import { NewsStatus } from '../data/news.schema';

// Update the header section (around line 38-45):
<div className={cn('p-4 border-b', statusColors[status])}>
  <div className="flex items-center justify-between">
    <h3 className="font-semibold text-lg">{title}</h3>
    <div className="flex items-center gap-2">
      {status === NewsStatus.PENDING && (
        <AddNewsModal className="h-8" />
      )}
      <Badge variant="secondary" className="ml-2">
        {count}
      </Badge>
    </div>
  </div>
</div>
```

### Phase 5: Mobile Support Enhancement

**File**: Update `src/features/news/components/NewsMobileView.tsx`

Add a floating action button for mobile news creation:

```typescript
// Add to imports
import { AddNewsModal } from './AddNewsModal';

// Add floating action button at the end of the component:
<div className="fixed bottom-6 right-6 z-50">
  <AddNewsModal />
</div>
```

## Technical Implementation Details

### Form Validation Strategy
- **Zod Schema**: Comprehensive validation with custom error messages
- **React Hook Form**: Optimized form handling with proper TypeScript support
- **Real-time Validation**: Field-level validation with error display
- **URL Validation**: Custom refinement for proper URL validation
- **Accessibility**: Proper ARIA attributes and error announcements

### State Management Integration
- **Existing Context**: No changes needed to `useNewsContext`
- **Mutation Hook**: Leverages existing `useCreateNewsMutation`
- **Cache Invalidation**: Automatic news list refresh after creation
- **Toast Notifications**: Success/error feedback via existing toast system

### Mobile Responsiveness
- **Responsive Button**: Text hidden on small screens, icon only
- **Modal Adaptation**: Full-height modal on mobile devices
- **Touch-friendly**: Adequate touch targets and spacing
- **Floating Action Button**: Mobile-optimized creation access

### Error Handling
- **Form Validation**: Client-side validation with user-friendly messages
- **API Errors**: Server error display with proper error boundaries
- **Loading States**: Visual feedback during submission
- **Accessibility**: Screen reader-friendly error announcements

## File Structure After Implementation

```
src/features/news/
├── components/
│   ├── AddNewsForm.tsx          # 🆕 Form component with validation
│   ├── AddNewsModal.tsx         # 🆕 Modal wrapper component
│   ├── NewsBoard.tsx            # ⚡ No changes needed
│   ├── NewsCard.tsx             # ⚡ No changes needed
│   ├── NewsColumn.tsx           # 📝 Updated with Add button
│   ├── NewsFilters.tsx          # ⚡ No changes needed
│   ├── NewsMobileView.tsx       # 📝 Updated with FAB
│   └── NewsStats.tsx            # ⚡ No changes needed
├── data/
│   ├── newsForm.schema.ts       # 🆕 Form validation schema
│   ├── news.schema.ts           # ⚡ No changes needed
│   └── news.service.ts          # ⚡ No changes needed
└── hooks/
    ├── mutations/
    │   ├── useCreateNews.mutation.ts     # ⚡ Already exists
    │   ├── useToggleFavorite.mutation.ts # ⚡ No changes needed
    │   └── useUpdateStatus.mutation.ts   # ⚡ No changes needed
    ├── queries/
    │   ├── useNewsStats.query.ts         # ⚡ No changes needed
    │   ├── usePublicNews.query.ts        # ⚡ No changes needed
    │   └── useUserNews.query.ts          # ⚡ No changes needed
    └── useNewsContext.tsx                # ⚡ No changes needed
```

## Dependencies Required

All required dependencies are already available in the project:
- `@hookform/resolvers` - For Zod integration with React Hook Form
- `react-hook-form` - Form management
- `zod` - Schema validation
- `lucide-react` - Plus icon
- `@radix-ui/react-dialog` - Modal component
- `@tanstack/react-query` - Already used by existing mutation

## Testing Strategy

### Unit Tests Required
1. **AddNewsForm.tsx**
   - Form validation behavior
   - Field interactions
   - Error message display
   - Accessibility attributes

2. **AddNewsModal.tsx**
   - Modal open/close behavior
   - Form submission integration
   - Error state handling
   - Success state handling

3. **Form Schema**
   - Validation rules testing
   - Edge cases (empty strings, invalid URLs)
   - Required field validation

### Integration Tests Required
1. **NewsColumn Integration**
   - Add button visibility on "To Read" column only
   - Button click opens modal
   - Successful creation updates column

2. **Mobile View Integration**
   - Floating action button functionality
   - Mobile modal behavior
   - Touch interactions

## Performance Considerations

### Optimizations
- **Form Memoization**: Form component wrapped with `React.memo` if needed
- **Modal Lazy Loading**: Dialog content loaded only when opened
- **Validation Debouncing**: Field validation debounced for better UX
- **Image URL Preview**: Optional enhancement for future iterations

### Bundle Size Impact
- **Minimal Impact**: All UI components already imported in project
- **Schema Validation**: Zod already in use, no additional bundle cost
- **Form Library**: React Hook Form already in dependencies

## Important Implementation Notes

### Critical Requirements
1. **Add Button Location**: Must be next to "To Read" column header ONLY
2. **Required Fields**: source, title, summary, link must be validated
3. **Optional Fields**: image_url can be empty, category defaults, is_public defaults to false
4. **Mobile Support**: Floating action button for mobile accessibility
5. **Existing Integration**: Must use existing `useCreateNewsMutation` hook

### Code Quality Standards
- **TypeScript**: Full type safety with proper interfaces
- **Accessibility**: ARIA labels, roles, and keyboard navigation
- **Error Handling**: Comprehensive error states and user feedback
- **Responsive Design**: Mobile-first approach with desktop enhancements
- **Testing**: Unit tests for all new components and integration points

### Future Enhancement Opportunities
1. **Image URL Preview**: Show thumbnail when image URL is provided
2. **Draft Saving**: Save form data to localStorage
3. **Bulk Import**: Import multiple news items from feeds
4. **Category Management**: Allow custom categories
5. **Rich Text Editor**: Enhanced summary editing with formatting

This implementation plan follows the established architecture patterns and provides a comprehensive, accessible, and mobile-responsive news creation feature that integrates seamlessly with the existing news management system.