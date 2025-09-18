import { useAuthContext } from '@/features/auth/hooks/useAuthContext';
import { Button } from '@/components/ui/button';
import { LogOut, User, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';

interface DashboardHeaderProps {
  title: string;
  subtitle?: string;
}

export const DashboardHeader = ({ title, subtitle }: DashboardHeaderProps) => {
  const { logout, userEmail, isLoading } = useAuthContext();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="mb-8 flex items-center justify-between">
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          {title}
        </h1>
        {subtitle && (
          <p className="text-muted-foreground mt-2">
            {subtitle}
          </p>
        )}
      </div>

      <div className="flex items-center gap-3">
        {/* User Email Display */}
        {userEmail && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <User className="h-4 w-4" />
            <span>{userEmail}</span>
          </div>
        )}

        {/* Profile Button */}
        <Button
          variant="outline"
          size="sm"
          asChild
          className="flex items-center gap-2"
        >
          <Link to="/profile">
            <Settings className="h-4 w-4" />
            Profile
          </Link>
        </Button>

        {/* Logout Button */}
        <Button
          variant="outline"
          size="sm"
          onClick={handleLogout}
          disabled={isLoading}
          className="flex items-center gap-2"
        >
          <LogOut className="h-4 w-4" />
          {isLoading ? 'Logging out...' : 'Logout'}
        </Button>
      </div>
    </header>
  );
};