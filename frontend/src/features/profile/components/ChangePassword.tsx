import React, { useState } from 'react';
import { useChangePassword } from '../hooks/useChangePassword';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Input } from '../../../components/ui/input';
import { Label } from '../../../components/ui/label';
import { BackButton } from '../../../core/components/BackButton';
import { Key, Eye, EyeOff } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export const ChangePassword: React.FC = () => {
  const changePasswordMutation = useChangePassword();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    // Current password validation
    if (!formData.current_password.trim()) {
      newErrors.current_password = 'Current password is required';
    }

    // New password validation
    if (!formData.new_password.trim()) {
      newErrors.new_password = 'New password is required';
    } else if (formData.new_password.length < 6) {
      newErrors.new_password = 'New password must be at least 6 characters';
    }

    // Confirm password validation
    if (!formData.confirm_password.trim()) {
      newErrors.confirm_password = 'Please confirm your new password';
    } else if (formData.new_password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match';
    }

    // Check if new password is different from current
    if (formData.current_password && formData.new_password && 
        formData.current_password === formData.new_password) {
      newErrors.new_password = 'New password must be different from current password';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    changePasswordMutation.mutate(formData, {
      onSuccess: () => {
        // Reset form
        setFormData({
          current_password: '',
          new_password: '',
          confirm_password: ''
        });
        // Navigate back to profile
        navigate('/profile');
      }
    });
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const togglePasswordVisibility = (field: 'current' | 'new' | 'confirm') => {
    setShowPasswords(prev => ({ ...prev, [field]: !prev[field] }));
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      {/* Back Button */}
      <div className="mb-4">
        <BackButton to="/profile" />
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            Change Password
          </CardTitle>
          <CardDescription>
            Update your account password for better security
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Current Password Field */}
            <div className="space-y-2">
              <Label htmlFor="current_password">Current Password</Label>
              <div className="relative">
                <Input
                  id="current_password"
                  type={showPasswords.current ? 'text' : 'password'}
                  value={formData.current_password}
                  onChange={(e) => handleInputChange('current_password', e.target.value)}
                  className={errors.current_password ? 'border-red-500 pr-10' : 'pr-10'}
                  placeholder="Enter your current password"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                  onClick={() => togglePasswordVisibility('current')}
                >
                  {showPasswords.current ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </Button>
              </div>
              {errors.current_password && (
                <p className="text-sm text-red-600">{errors.current_password}</p>
              )}
            </div>

            {/* New Password Field */}
            <div className="space-y-2">
              <Label htmlFor="new_password">New Password</Label>
              <div className="relative">
                <Input
                  id="new_password"
                  type={showPasswords.new ? 'text' : 'password'}
                  value={formData.new_password}
                  onChange={(e) => handleInputChange('new_password', e.target.value)}
                  className={errors.new_password ? 'border-red-500 pr-10' : 'pr-10'}
                  placeholder="Enter your new password"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                  onClick={() => togglePasswordVisibility('new')}
                >
                  {showPasswords.new ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </Button>
              </div>
              {errors.new_password && (
                <p className="text-sm text-red-600">{errors.new_password}</p>
              )}
            </div>

            {/* Confirm Password Field */}
            <div className="space-y-2">
              <Label htmlFor="confirm_password">Confirm New Password</Label>
              <div className="relative">
                <Input
                  id="confirm_password"
                  type={showPasswords.confirm ? 'text' : 'password'}
                  value={formData.confirm_password}
                  onChange={(e) => handleInputChange('confirm_password', e.target.value)}
                  className={errors.confirm_password ? 'border-red-500 pr-10' : 'pr-10'}
                  placeholder="Confirm your new password"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                  onClick={() => togglePasswordVisibility('confirm')}
                >
                  {showPasswords.confirm ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </Button>
              </div>
              {errors.confirm_password && (
                <p className="text-sm text-red-600">{errors.confirm_password}</p>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <Button
                type="submit"
                disabled={changePasswordMutation.isPending}
                className="flex-1"
              >
                {changePasswordMutation.isPending ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Changing...
                  </>
                ) : (
                  <>
                    <Key className="h-4 w-4 mr-2" />
                    Change Password
                  </>
                )}
              </Button>
              <Button type="button" variant="outline" asChild className="flex-1">
                <Link to="/profile">
                  Cancel
                </Link>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};
