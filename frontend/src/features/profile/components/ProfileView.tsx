import React from 'react';
import { useProfile } from '../hooks/useProfile';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { BackButton, ThemeToggle } from '../../../core/components';
import { CalendarDays, Mail, User, Shield, Edit, Key, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Skeleton } from '../../../components/ui/skeleton';

export const ProfileView: React.FC = () => {
  const { data: profile, isLoading, error } = useProfile();

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <Card>
          <CardHeader>
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-64" />
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center text-red-600">
              Failed to load profile. Please try again.
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center text-muted-foreground">
              No profile data available.
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      {/* Back Button */}
      <div className="mb-4">
        <BackButton to="/home" />
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Profile Information
          </CardTitle>
          <CardDescription>
            View and manage your account information
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Username */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center gap-3">
              <User className="h-5 w-5 text-muted-foreground" />
              <div>
                <div className="font-medium">Username</div>
                <div className="text-sm text-muted-foreground">{profile.username}</div>
              </div>
            </div>
          </div>

          {/* Email */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center gap-3">
              <Mail className="h-5 w-5 text-muted-foreground" />
              <div>
                <div className="font-medium">Email Address</div>
                <div className="text-sm text-muted-foreground">{profile.email}</div>
              </div>
            </div>
          </div>

          {/* Account Status */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center gap-3">
              <Shield className="h-5 w-5 text-muted-foreground" />
              <div>
                <div className="font-medium">Account Status</div>
                <div className="text-sm text-muted-foreground">
                  <Badge variant={profile.is_active ? "default" : "secondary"}>
                    {profile.is_active ? "Active" : "Inactive"}
                  </Badge>
                </div>
              </div>
            </div>
          </div>

          {/* Theme Settings */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center gap-3">
              <Settings className="h-5 w-5 text-muted-foreground" />
              <div>
                <div className="font-medium">Theme Preference</div>
                <div className="text-sm text-muted-foreground">Choose your preferred color theme</div>
              </div>
            </div>
            <ThemeToggle />
          </div>

          {/* Created Date */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center gap-3">
              <CalendarDays className="h-5 w-5 text-muted-foreground" />
              <div>
                <div className="font-medium">Member Since</div>
                <div className="text-sm text-muted-foreground">
                  {formatDate(profile.created_at)}
                </div>
              </div>
            </div>
          </div>

          {/* Last Updated */}
          {profile.updated_at && (
            <div className="flex items-center justify-between p-4 border rounded-lg">
              <div className="flex items-center gap-3">
                <CalendarDays className="h-5 w-5 text-muted-foreground" />
                <div>
                  <div className="font-medium">Last Updated</div>
                  <div className="text-sm text-muted-foreground">
                    {formatDate(profile.updated_at)}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <Button asChild className="flex-1">
              <Link to="/profile/edit">
                <Edit className="h-4 w-4 mr-2" />
                Edit Profile
              </Link>
            </Button>
            <Button asChild variant="outline" className="flex-1">
              <Link to="/profile/change-password">
                <Key className="h-4 w-4 mr-2" />
                Change Password
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
