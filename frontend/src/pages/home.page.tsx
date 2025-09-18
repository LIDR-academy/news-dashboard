import { ProtectedRoute } from '@/core/components/ProtectedRoute'
import { NewsProvider } from '@/features/news/hooks/useNewsContext'
import { NewsBoard } from '@/features/news/components/NewsBoard'
import { DashboardHeader } from '@/components/DashboardHeader'

const HomePage = () => {
  return (
    <ProtectedRoute>
      <NewsProvider>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-50">
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