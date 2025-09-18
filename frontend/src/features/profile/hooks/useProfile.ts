import { useQuery } from '@tanstack/react-query';
import { profileService } from '../data/profile.service';
import { ProfileUser } from '../data/profile.schema';

export const useProfile = () => {
  return useQuery<ProfileUser>({
    queryKey: ['profile'],
    queryFn: profileService.getProfile,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });
};
