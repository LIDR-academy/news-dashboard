import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BookOpen, Book, CheckCircle, Heart, TrendingUp } from 'lucide-react';
import { useNewsContext } from '../hooks/useNewsContext';

export const NewsStats = () => {
  const { stats } = useNewsContext();

  const statItems = [
    {
      label: 'To Read',
      value: stats.pending,
      icon: BookOpen,
      color: 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/30',
    },
    {
      label: 'Reading',
      value: stats.reading,
      icon: Book,
      color: 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/30',
    },
    {
      label: 'Completed',
      value: stats.read,
      icon: CheckCircle,
      color: 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/30',
    },
    {
      label: 'Favorites',
      value: stats.favorites,
      icon: Heart,
      color: 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/30',
    },
    {
      label: 'Total',
      value: stats.total,
      icon: TrendingUp,
      color: 'text-purple-600 bg-purple-100 dark:text-purple-400 dark:bg-purple-900/30',
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      {statItems.map((stat) => {
        const Icon = stat.icon;
        return (
          <Card key={stat.label}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-muted-foreground">{stat.label}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </div>
                <div className={`p-2 rounded-lg ${stat.color}`}>
                  <Icon className="h-5 w-5" />
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};