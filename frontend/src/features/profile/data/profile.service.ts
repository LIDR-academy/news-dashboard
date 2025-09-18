import { apiClient } from '../../../core/data/apiClient';
import { ProfileUpdate, ChangePasswordRequest, ChangePasswordResponse, ProfileUser } from './profile.schema';

const BASE_URL = '/api/v1';

export const profileService = {
  getProfile: (): Promise<ProfileUser> => 
    apiClient.get<ProfileUser>(`${BASE_URL}/users/me`),
    
  updateProfile: (data: ProfileUpdate): Promise<ProfileUser> => 
    apiClient.put<ProfileUser>(`${BASE_URL}/users/me`, data),
    
  changePassword: (data: ChangePasswordRequest): Promise<ChangePasswordResponse> => 
    apiClient.put<ChangePasswordResponse>(`${BASE_URL}/users/me/password`, data)
};
