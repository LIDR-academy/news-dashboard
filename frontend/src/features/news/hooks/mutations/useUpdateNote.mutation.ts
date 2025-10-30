import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { newsService } from '../../data/news.service';
import type { UpdatePersonalNoteRequest } from '../../data/news.schema';

export const useUpdateNoteMutation = () => {
  const queryClient = useQueryClient();

  const { mutate: updateNote, isPending: isUpdating } = useMutation({
    mutationFn: async ({ newsId, note }: { newsId: string; note: string }) => {
      const payload: UpdatePersonalNoteRequest = { note };
      return await newsService.updatePersonalNote(newsId, payload);
    },
    onSuccess: () => {
      toast.success('Note saved');
      // Invalidate user news
      void queryClient.invalidateQueries({ queryKey: ['news', 'user'] });
    },
    onError: (error: unknown) => {
      toast.error(error instanceof Error ? error.message : 'Failed to save note');
    },
  });

  const { mutate: deleteNote, isPending: isDeleting } = useMutation({
    mutationFn: async ({ newsId }: { newsId: string }) => {
      return await newsService.deletePersonalNote(newsId);
    },
    onSuccess: () => {
      toast.success('Note deleted');
      void queryClient.invalidateQueries({ queryKey: ['news', 'user'] });
    },
    onError: (error: unknown) => {
      toast.error(error instanceof Error ? error.message : 'Failed to delete note');
    },
  });

  return { updateNote, deleteNote, isUpdating, isDeleting };
};


