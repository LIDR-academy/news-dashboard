import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import { AddNewsForm } from './AddNewsForm';
import { useCreateNewsMutation } from '../hooks/mutations/useCreateNews.mutation';
import type { CreateNewsRequest } from '../data/news.schema';

interface AddNewsModalProps {
  className?: string;
  size?: 'default' | 'sm' | 'lg';
  variant?: 'default' | 'outline' | 'ghost';
  children?: React.ReactNode; // For custom trigger
}

export const AddNewsModal = ({
  className,
  size = 'sm',
  variant = 'default',
  children
}: AddNewsModalProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const { createNews, isLoading, error, isSuccess } = useCreateNewsMutation();

  const handleSubmit = (data: CreateNewsRequest) => {
    createNews(data);
  };

  // Close modal on successful creation
  useEffect(() => {
    if (isSuccess) {
      setIsOpen(false);
    }
  }, [isSuccess]);

  const handleCancel = () => {
    setIsOpen(false);
  };

  const trigger = children || (
    <Button
      size={size}
      variant={variant}
      className={className}
      aria-label="Add new news item"
    >
      <Plus className="w-4 h-4" />
      <span className="hidden sm:inline ml-2">Add News</span>
    </Button>
  );

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        {trigger}
      </DialogTrigger>

      <DialogContent className="sm:max-w-[520px] max-w-[calc(100%-1rem)] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Add News Item</DialogTitle>
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