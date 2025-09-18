import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { profileService } from '../data/profile.service';
import { ChangePasswordRequest, ChangePasswordResponse } from '../data/profile.schema';

export const useChangePassword = () => {
  return useMutation<ChangePasswordResponse, Error, ChangePasswordRequest>({
    mutationFn: profileService.changePassword,
    onSuccess: () => {
      toast.success('Password changed successfully');
    },
    onError: (error: any) => {
      const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to change password';
      toast.error(errorMessage);
    },
  });
};
