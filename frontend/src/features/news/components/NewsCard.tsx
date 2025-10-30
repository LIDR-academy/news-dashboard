import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Heart, ExternalLink, NotebookPen } from 'lucide-react';
import { useNewsContext } from '../hooks/useNewsContext';
import { CATEGORY_COLORS, STATUS_COLORS, type NewsItem } from '../data/news.schema';
import { cn } from '@/lib/utils';
import { useState } from 'react';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';
import { useUpdateNoteMutation } from '../hooks/mutations/useUpdateNote.mutation';

interface NewsCardProps {
  item: NewsItem;
  isDragging?: boolean;
}

export const NewsCard = ({ item, isDragging = false }: NewsCardProps) => {
  const { toggleFavorite } = useNewsContext();
  const { updateNote, deleteNote, isUpdating, isDeleting } = useUpdateNoteMutation();
  const [open, setOpen] = useState(false);
  const [note, setNote] = useState<string>(item.personal_note ?? '');
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: item.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    toggleFavorite(item.id);
  };

  const handleLinkClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(item.link, '_blank', 'noopener,noreferrer');
  };

  const handleOpenNotes = (e: React.MouseEvent) => {
    e.stopPropagation();
    setNote(item.personal_note ?? '');
    setOpen(true);
  };

  const handleSaveNote = () => {
    updateNote(
      { newsId: item.id, note },
      { onSuccess: () => setOpen(false) }
    );
  };

  const handleDeleteNote = () => {
    deleteNote(
      { newsId: item.id },
      { onSuccess: () => setOpen(false) }
    );
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={cn(
        'cursor-grab active:cursor-grabbing',
        (isDragging || isSortableDragging) && 'opacity-50'
      )}
    >
      <Card
        className={cn(
          'bg-white/95 backdrop-blur-sm hover:shadow-lg transition-all',
          STATUS_COLORS[item.status]
        )}
      >
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <h4 className="font-medium text-sm line-clamp-2">{item.title}</h4>
              <p className="text-xs text-muted-foreground mt-1">{item.source}</p>
            </div>
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7"
                onClick={handleOpenNotes}
              >
                <NotebookPen className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7"
                onClick={handleFavoriteClick}
              >
                <Heart
                  className={cn(
                    'h-4 w-4',
                    item.is_favorite && 'fill-red-500 text-red-500'
                  )}
                />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7"
                onClick={handleLinkClick}
              >
                <ExternalLink className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="pt-0">
          <p className="text-xs text-muted-foreground line-clamp-2 mb-3">
            {item.summary}
          </p>
          
          <div className="flex items-center justify-between">
            <Badge
              variant="secondary"
              className={cn('text-xs', CATEGORY_COLORS[item.category])}
            >
              {item.category}
            </Badge>
            
            {item.is_public && (
              <Badge variant="outline" className="text-xs">
                Public
              </Badge>
            )}
          </div>
          
          {item.image_url && (
            <img
              src={item.image_url}
              alt={item.title}
              className="mt-3 w-full h-24 object-cover rounded"
              loading="lazy"
            />
          )}

          {item.personal_note && (
            <div className="mt-3 rounded border bg-muted/40 p-2">
              <p className="text-[11px] uppercase tracking-wide text-muted-foreground mb-1">Personal note</p>
              <p className="text-sm whitespace-pre-wrap">{item.personal_note}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
          <span className="hidden" />
        </DialogTrigger>
        <DialogContent onOpenAutoFocus={(e) => e.preventDefault()}>
          <DialogHeader>
            <DialogTitle>Edit personal note</DialogTitle>
          </DialogHeader>
          <div>
            <Textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Write your note…"
              className="min-h-32"
            />
          </div>
          <DialogFooter>
            <Button
              variant="secondary"
              onClick={handleDeleteNote}
              disabled={isDeleting}
            >
              {isDeleting ? 'Deleting…' : 'Delete note'}
            </Button>
            <Button
              onClick={handleSaveNote}
              disabled={isUpdating}
            >
              {isUpdating ? 'Saving…' : 'Save note'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};