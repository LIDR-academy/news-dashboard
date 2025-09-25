# News Creation UI Implementation Plan - NEWS-9

## Overview
This document outlines the detailed UI/UX implementation plan for adding News Creation functionality using shadcn/ui components. The implementation will provide a modal-based interface for creating news items with proper validation, accessibility, and mobile responsiveness.

## Component Architecture

### Core Components to Create

#### 1. AddNewsModal Component
```typescript
// src/features/news/components/AddNewsModal.tsx
interface AddNewsModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  trigger?: React.ReactNode;
}
```

**Purpose**: Main modal wrapper using shadcn/ui Dialog component
**Key Features**:
- Dialog overlay with proper backdrop
- Responsive modal sizing (sm:max-w-[520px] for desktop, max-w-[calc(100%-2rem)] for mobile)
- Proper z-index layering (z-50)
- Animation support with fade and zoom effects
- Accessibility features (ESC key, click outside to close)

#### 2. AddNewsForm Component
```typescript
// src/features/news/components/AddNewsForm.tsx
interface AddNewsFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}
```

**Purpose**: Form component with validation and submission logic
**Key Features**:
- Built-in form validation using useState pattern (following existing project patterns)
- Real-time validation feedback
- Error state management
- Loading states during submission
- Form reset on successful submission

#### 3. AddNewsButton Component
```typescript
// src/features/news/components/AddNewsButton.tsx
interface AddNewsButtonProps {
  className?: string;
  size?: 'default' | 'sm' | 'lg';
  variant?: 'default' | 'outline' | 'ghost';
}
```

**Purpose**: Reusable trigger button with consistent styling
**Key Features**:
- Integration with existing button variants
- Icon support (Plus icon from lucide-react)
- Loading state support
- Accessibility features (proper ARIA labels)

## shadcn/ui Components Utilized

### 1. Dialog System
```typescript
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
```

**Implementation Details**:
- `DialogContent`: Custom width with `sm:max-w-[520px]` for optimal form viewing
- `DialogHeader`: Clean title and description layout
- `DialogFooter`: Action buttons with proper spacing
- `DialogOverlay`: Semi-transparent backdrop (bg-black/50)

### 2. Form Controls
```typescript
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea" // Need to add to project
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
```

**Field Specifications**:
- **Source**: Text input with required validation
- **Title**: Text input with required validation
- **Summary**: Textarea component (needs to be added to project)
- **Link**: URL input with URL validation pattern
- **Image URL**: URL input (optional)
- **Category**: Select dropdown with NewsCategory enum options
- **Make Public**: Checkbox with proper labeling

### 3. Supporting Components
```typescript
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
```

## Form Layout Design

### Modal Structure
```
┌─────────────────────────────────────┐
│ Add News Item                    ✕  │  ← DialogHeader with DialogTitle
├─────────────────────────────────────┤
│ [Form Content - ScrollArea]         │  ← DialogContent
│                                     │
│ Source *        [text input]        │
│ Title *         [text input]        │
│ Summary *       [textarea - 4 rows] │
│ Link *          [url input]         │
│ Image URL       [url input]         │
│ Category        [dropdown]          │
│ ☐ Make public                       │
│                                     │
├─────────────────────────────────────┤
│              [Cancel] [Add News]    │  ← DialogFooter
└─────────────────────────────────────┘
```

### Form Grid Layout
```typescript
<div className="grid gap-4 py-4">
  <div className="grid gap-3">
    <Label htmlFor="source">Source *</Label>
    <Input id="source" className="col-span-3" />
  </div>
  // ... similar structure for other fields
</div>
```

### Field Styling Specifications
```typescript
// Required field styling
const requiredFieldStyle = "aria-invalid:border-destructive aria-invalid:ring-destructive/20"

// Error message styling
const errorMessageStyle = "text-destructive text-sm mt-1"

// Loading state styling
const loadingButtonStyle = "disabled:opacity-50 disabled:cursor-not-allowed"
```

## Integration Points

### 1. NewsColumn Component Integration
**Target Location**: `/src/features/news/components/NewsColumn.tsx` (lines 38-45)

```typescript
// Current header structure
<div className={cn('p-4 border-b', statusColors[status])}>
  <div className="flex items-center justify-between">
    <h3 className="font-semibold text-lg">{title}</h3>
    {status === NewsStatus.PENDING && ( // Only show in "To Read" column
      <div className="flex items-center gap-2">
        <AddNewsButton size="sm" variant="ghost" />
        <Badge variant="secondary" className="ml-2">{count}</Badge>
      </div>
    )}
    {status !== NewsStatus.PENDING && (
      <Badge variant="secondary" className="ml-2">{count}</Badge>
    )}
  </div>
</div>
```

### 2. Mobile View Integration
**Target Location**: `/src/features/news/components/NewsMobileView.tsx`

```typescript
// Floating Action Button for mobile
<div className="fixed bottom-6 right-6 z-40">
  <AddNewsButton
    size="lg"
    className="rounded-full h-14 w-14 shadow-lg"
  />
</div>
```

## Validation Strategy

### Client-Side Validation (Following Existing Pattern)
```typescript
interface FormErrors {
  source?: string;
  title?: string;
  summary?: string;
  link?: string;
  image_url?: string;
  category?: string;
}

const validateForm = (data: CreateNewsRequest): FormErrors => {
  const errors: FormErrors = {};

  // Required field validation
  if (!data.source.trim()) errors.source = 'Source is required';
  if (!data.title.trim()) errors.title = 'Title is required';
  if (!data.summary.trim()) errors.summary = 'Summary is required';
  if (!data.link.trim()) errors.link = 'Link is required';

  // URL validation
  if (data.link && !isValidUrl(data.link)) {
    errors.link = 'Please enter a valid URL';
  }
  if (data.image_url && !isValidUrl(data.image_url)) {
    errors.image_url = 'Please enter a valid URL';
  }

  return errors;
};
```

### Error Display Pattern
```typescript
{errors.source && (
  <p className="text-destructive text-sm mt-1">{errors.source}</p>
)}
```

## Mobile Responsiveness

### Breakpoint Strategy
- **Mobile** (`< 640px`): Full-width modal with padding, stacked form layout
- **Tablet** (`640px - 1024px`): Centered modal with fixed width
- **Desktop** (`> 1024px`): Standard modal width with grid layout

### Mobile-Specific Features
```typescript
// Touch-friendly input sizing
<Input className="h-12 text-base" /> // Prevent zoom on iOS

// Mobile modal sizing
<DialogContent className="w-full max-w-[calc(100%-1rem)] h-auto max-h-[85vh]">
  <ScrollArea className="max-h-[60vh]">
    {/* Form content */}
  </ScrollArea>
</DialogContent>
```

## Accessibility Implementation

### ARIA Features
```typescript
<Dialog>
  <DialogTrigger
    aria-label="Add new news item"
    className="focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
  >
    <Plus className="h-4 w-4" />
  </DialogTrigger>

  <DialogContent aria-describedby="add-news-description">
    <DialogTitle>Add News Item</DialogTitle>
    <DialogDescription id="add-news-description">
      Fill out the form below to add a new news item to your reading list.
    </DialogDescription>
  </DialogContent>
</Dialog>
```

### Keyboard Navigation
- Tab order: Source → Title → Summary → Link → Image URL → Category → Checkbox → Cancel → Submit
- ESC key closes modal
- Enter key submits form when focused on inputs
- Proper focus trapping within modal

### Screen Reader Support
```typescript
<Label htmlFor="source" className="sr-only sm:not-sr-only">
  Source (required)
</Label>
<Input
  id="source"
  aria-required="true"
  aria-invalid={!!errors.source}
  aria-describedby={errors.source ? "source-error" : undefined}
/>
{errors.source && (
  <p id="source-error" role="alert" className="text-destructive text-sm">
    {errors.source}
  </p>
)}
```

## Color System Integration

### Using Project CSS Variables
```typescript
// Primary colors from src/index.css
--primary: oklch(0.646 0.222 263.116);
--primary-foreground: oklch(0.985 0 0);
--destructive: oklch(0.577 0.245 27.325);

// Category-specific colors (matching existing news system)
const categoryColors = {
  [NewsCategory.GENERAL]: 'bg-gray-100 text-gray-800',
  [NewsCategory.RESEARCH]: 'bg-purple-100 text-purple-800',
  // ... existing color mappings from news.schema.ts
}
```

### Dark Mode Support
All components will automatically support dark mode through CSS variables:
```css
.dark {
  --background: oklch(0.145 0 0);
  --card: oklch(0.205 0 0);
  /* Modal will adapt automatically */
}
```

## Performance Considerations

### Lazy Loading
```typescript
// Lazy load the modal to improve initial page load
const AddNewsModal = React.lazy(() => import('./AddNewsModal'));
```

### Form Optimization
```typescript
// Debounced validation for better UX
const [formData, setFormData] = useState<CreateNewsRequest>({
  source: '',
  title: '',
  summary: '',
  link: '',
  image_url: '',
  category: NewsCategory.GENERAL,
  is_public: false
});

// Prevent unnecessary re-renders
const handleInputChange = useCallback((field: string, value: string) => {
  setFormData(prev => ({ ...prev, [field]: value }));
}, []);
```

## Files to Create/Modify

### New Files Required
1. **`/src/features/news/components/AddNewsModal.tsx`** - Main modal component
2. **`/src/features/news/components/AddNewsForm.tsx`** - Form component with validation
3. **`/src/features/news/components/AddNewsButton.tsx`** - Reusable trigger button
4. **`/src/components/ui/textarea.tsx`** - Add missing textarea component

### Files to Modify
1. **`/src/features/news/components/NewsColumn.tsx`** - Add button integration (lines 38-45)
2. **`/src/features/news/components/NewsMobileView.tsx`** - Add floating action button
3. **`/src/features/news/components/NewsBoard.tsx`** - Import and use new components
4. **`/frontend/package.json`** - No additional dependencies needed

## Component Composition Recommendations

### 1. Component Hierarchy
```
NewsBoard
├── NewsColumn (Desktop)
│   └── AddNewsButton → AddNewsModal → AddNewsForm
└── NewsMobileView (Mobile)
    └── AddNewsButton (Floating) → AddNewsModal → AddNewsForm
```

### 2. State Management Pattern
```typescript
// Use existing useCreateNewsMutation hook
const AddNewsModal = ({ open, onOpenChange }: AddNewsModalProps) => {
  const { createNews, isLoading, isSuccess } = useCreateNewsMutation();

  useEffect(() => {
    if (isSuccess) {
      onOpenChange(false);
      // Form reset handled by mutation success
    }
  }, [isSuccess, onOpenChange]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {/* Modal content */}
    </Dialog>
  );
};
```

### 3. Error Handling Integration
```typescript
// Integrate with existing toast system
import { toast } from 'sonner';

const handleSubmit = async (data: CreateNewsRequest) => {
  try {
    await createNews(data);
    // Success toast handled by mutation
  } catch (error) {
    // Error toast handled by mutation
    console.error('Form submission error:', error);
  }
};
```

## Testing Considerations

### Component Testing Requirements
1. **Modal behavior**: Opening/closing, ESC key, backdrop click
2. **Form validation**: Required fields, URL validation, error display
3. **Accessibility**: Focus management, ARIA attributes, keyboard navigation
4. **Mobile responsiveness**: Touch interactions, viewport adaptation
5. **Integration**: Proper mutation calling, success/error handling

### Test File Structure
- `AddNewsModal.test.tsx` - Modal behavior and accessibility
- `AddNewsForm.test.tsx` - Form validation and submission
- `AddNewsButton.test.tsx` - Button rendering and click handling

## Implementation Priority

### Phase 1: Core Components
1. Add Textarea component to UI library
2. Create AddNewsModal with basic structure
3. Create AddNewsForm with validation
4. Create AddNewsButton component

### Phase 2: Integration
1. Integrate button in NewsColumn header
2. Add mobile floating action button
3. Connect to existing mutation hook
4. Test form submission flow

### Phase 3: Polish & Testing
1. Add comprehensive error handling
2. Implement accessibility features
3. Add loading states and animations
4. Write comprehensive test suite

## Notes for Implementation
- Follow existing project patterns (no external form libraries)
- Use existing mutation hook (`useCreateNewsMutation`)
- Maintain consistency with current design system
- Ensure mobile-first responsive design
- Prioritize accessibility and keyboard navigation
- Integrate seamlessly with existing news board functionality