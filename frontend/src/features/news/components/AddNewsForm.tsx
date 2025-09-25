import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Textarea } from '@/components/ui/textarea';
import { NewsCategory, type CreateNewsRequest } from '../data/news.schema';
import { CATEGORY_OPTIONS } from '../data/newsForm.schema';

interface FormErrors {
  source?: string;
  title?: string;
  summary?: string;
  link?: string;
  image_url?: string;
  category?: string;
}

interface AddNewsFormProps {
  onSubmit: (data: CreateNewsRequest) => void;
  isSubmitting: boolean;
  onCancel: () => void;
}

const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

const validateForm = (data: CreateNewsRequest): FormErrors => {
  const errors: FormErrors = {};

  // Required field validation
  if (!data.source.trim()) errors.source = 'Source is required';
  else if (data.source.length > 100) errors.source = 'Source must be less than 100 characters';

  if (!data.title.trim()) errors.title = 'Title is required';
  else if (data.title.length > 200) errors.title = 'Title must be less than 200 characters';

  if (!data.summary.trim()) errors.summary = 'Summary is required';
  else if (data.summary.length > 500) errors.summary = 'Summary must be less than 500 characters';

  if (!data.link.trim()) errors.link = 'Link is required';
  else if (!isValidUrl(data.link)) errors.link = 'Please enter a valid URL';

  // Optional field validation
  if (data.image_url && data.image_url.trim() && !isValidUrl(data.image_url)) {
    errors.image_url = 'Please enter a valid URL';
  }

  return errors;
};

export const AddNewsForm = ({ onSubmit, isSubmitting, onCancel }: AddNewsFormProps) => {
  const [formData, setFormData] = useState<CreateNewsRequest>({
    source: '',
    title: '',
    summary: '',
    link: '',
    image_url: '',
    category: NewsCategory.GENERAL,
    is_public: false
  });

  const [errors, setErrors] = useState<FormErrors>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate form
    const validationErrors = validateForm(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Clean up data before submitting
    const cleanedData = {
      ...formData,
      image_url: formData.image_url?.trim() || undefined
    };

    onSubmit(cleanedData);
  };

  const handleInputChange = (field: keyof CreateNewsRequest, value: string | boolean | NewsCategory) => {
    setFormData(prev => ({ ...prev, [field]: value }));

    // Clear error for this field when user starts typing
    if (errors[field as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const isFormValid = !Object.keys(errors).length &&
    formData.source.trim() &&
    formData.title.trim() &&
    formData.summary.trim() &&
    formData.link.trim();

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Source Field */}
      <div className="space-y-2">
        <Label htmlFor="source">Source *</Label>
        <Input
          id="source"
          placeholder="e.g., TechCrunch, Medium, etc."
          value={formData.source}
          onChange={(e) => handleInputChange('source', e.target.value)}
          aria-invalid={!!errors.source}
          aria-required="true"
        />
        {errors.source && (
          <p className="text-sm text-destructive" role="alert">
            {errors.source}
          </p>
        )}
      </div>

      {/* Title Field */}
      <div className="space-y-2">
        <Label htmlFor="title">Title *</Label>
        <Input
          id="title"
          placeholder="Article title"
          value={formData.title}
          onChange={(e) => handleInputChange('title', e.target.value)}
          aria-invalid={!!errors.title}
          aria-required="true"
        />
        {errors.title && (
          <p className="text-sm text-destructive" role="alert">
            {errors.title}
          </p>
        )}
      </div>

      {/* Summary Field */}
      <div className="space-y-2">
        <Label htmlFor="summary">Summary *</Label>
        <Textarea
          id="summary"
          placeholder="Brief summary of the article"
          value={formData.summary}
          onChange={(e) => handleInputChange('summary', e.target.value)}
          aria-invalid={!!errors.summary}
          aria-required="true"
          className="min-h-[80px]"
        />
        {errors.summary && (
          <p className="text-sm text-destructive" role="alert">
            {errors.summary}
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
          value={formData.link}
          onChange={(e) => handleInputChange('link', e.target.value)}
          aria-invalid={!!errors.link}
          aria-required="true"
        />
        {errors.link && (
          <p className="text-sm text-destructive" role="alert">
            {errors.link}
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
          value={formData.image_url || ''}
          onChange={(e) => handleInputChange('image_url', e.target.value)}
          aria-invalid={!!errors.image_url}
        />
        {errors.image_url && (
          <p className="text-sm text-destructive" role="alert">
            {errors.image_url}
          </p>
        )}
      </div>

      {/* Category Field */}
      <div className="space-y-2">
        <Label htmlFor="category">Category *</Label>
        <Select
          value={formData.category}
          onValueChange={(value) => handleInputChange('category', value as NewsCategory)}
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
        {errors.category && (
          <p className="text-sm text-destructive" role="alert">
            {errors.category}
          </p>
        )}
      </div>

      {/* Public Checkbox */}
      <div className="flex items-center space-x-2">
        <Checkbox
          id="is_public"
          checked={formData.is_public}
          onCheckedChange={(checked) => handleInputChange('is_public', checked as boolean)}
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
          disabled={isSubmitting || !isFormValid}
        >
          {isSubmitting ? 'Creating...' : 'Create News'}
        </Button>
      </div>
    </form>
  );
};