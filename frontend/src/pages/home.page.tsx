import { ProtectedRoute } from '@/core/components/ProtectedRoute'
import { NewsProvider } from '@/features/news/hooks/useNewsContext'
import { NewsBoard } from '@/features/news/components/NewsBoard'
import { DashboardHeader } from '@/components/DashboardHeader'

const HomePage = () => {
  return (
    <ProtectedRoute>
      <NewsProvider>
        <div className="min-h-screen bg-background">
          <div className="container mx-auto px-4 py-8">
            <DashboardHeader
              title="News Dashboard"
              subtitle="Manage your reading list with our Kanban-style board"
            />

            <NewsBoard />
          </div>
        </div>
      </NewsProvider>
    </ProtectedRoute>
  )
}

export default HomePage