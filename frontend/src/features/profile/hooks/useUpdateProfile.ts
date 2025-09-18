import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { profileService } from '../data/profile.service';
import { ProfileUpdate, ProfileUser } from '../data/profile.schema';

export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation<ProfileUser, Error, ProfileUpdate>({
    mutationFn: profileService.updateProfile,
    onSuccess: (data) => {
      // Update the profile cache
      queryClient.setQueryData(['profile'], data);
      // Invalidate and refetch profile data
      queryClient.invalidateQueries({ queryKey: ['profile'] });
      toast.success('Profile updated successfully');
    },
    onError: (error: any) => {
      const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to update profile';
      toast.error(errorMessage);
    },
  });
};
