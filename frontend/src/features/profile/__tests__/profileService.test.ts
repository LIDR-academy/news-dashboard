import { profileService } from '../data/profile.service';
import { apiClient } from '../../../core/data/apiClient';

// Mock the apiClient
jest.mock('../../../core/data/apiClient');
const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;

describe('profileService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getProfile', () => {
    it('should call apiClient.get with correct URL', async () => {
      const mockProfile = {
        id: 'user123',
        email: 'test@example.com',
        username: 'testuser',
        is_active: true,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-02T00:00:00Z',
      };

      mockApiClient.get.mockResolvedValue(mockProfile);

      const result = await profileService.getProfile();

      expect(mockApiClient.get).toHaveBeenCalledWith('/api/v1/users/me');
      expect(result).toEqual(mockProfile);
    });

    it('should handle API errors', async () => {
      const error = new Error('Failed to fetch profile');
      mockApiClient.get.mockRejectedValue(error);

      await expect(profileService.getProfile()).rejects.toThrow('Failed to fetch profile');
      expect(mockApiClient.get).toHaveBeenCalledWith('/api/v1/users/me');
    });
  });

  describe('updateProfile', () => {
    it('should call apiClient.put with correct URL and data', async () => {
      const updateData = {
        username: 'newusername',
        email: 'newemail@example.com'
      };

      const mockUpdatedProfile = {
        id: 'user123',
        email: 'newemail@example.com',
        username: 'newusername',
        is_active: true,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-02T00:00:00Z',
      };

      mockApiClient.put.mockResolvedValue(mockUpdatedProfile);

      const result = await profileService.updateProfile(updateData);

      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me', updateData);
      expect(result).toEqual(mockUpdatedProfile);
    });

    it('should handle partial update data', async () => {
      const updateData = {
        username: 'newusername'
      };

      const mockUpdatedProfile = {
        id: 'user123',
        email: 'test@example.com',
        username: 'newusername',
        is_active: true,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-02T00:00:00Z',
      };

      mockApiClient.put.mockResolvedValue(mockUpdatedProfile);

      const result = await profileService.updateProfile(updateData);

      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me', updateData);
      expect(result).toEqual(mockUpdatedProfile);
    });

    it('should handle API errors', async () => {
      const updateData = {
        username: 'existinguser'
      };

      const error = new Error('Username already exists');
      mockApiClient.put.mockRejectedValue(error);

      await expect(profileService.updateProfile(updateData)).rejects.toThrow('Username already exists');
      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me', updateData);
    });

    it('should handle validation errors', async () => {
      const updateData = {
        email: 'invalid-email'
      };

      const error = {
        response: {
          data: {
            detail: 'Invalid email format'
          }
        }
      };
      mockApiClient.put.mockRejectedValue(error);

      await expect(profileService.updateProfile(updateData)).rejects.toEqual(error);
      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me', updateData);
    });
  });

  describe('changePassword', () => {
    it('should call apiClient.put with correct URL and data', async () => {
      const passwordData = {
        current_password: 'oldpassword',
        new_password: 'newpassword123',
        confirm_password: 'newpassword123'
      };

      const mockResponse = {
        message: 'Password changed successfully'
      };

      mockApiClient.put.mockResolvedValue(mockResponse);

      const result = await profileService.changePassword(passwordData);

      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me/password', passwordData);
      expect(result).toEqual(mockResponse);
    });

    it('should handle API errors', async () => {
      const passwordData = {
        current_password: 'wrongpassword',
        new_password: 'newpassword123',
        confirm_password: 'newpassword123'
      };

      const error = new Error('Current password is incorrect');
      mockApiClient.put.mockRejectedValue(error);

      await expect(profileService.changePassword(passwordData)).rejects.toThrow('Current password is incorrect');
      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me/password', passwordData);
    });

    it('should handle validation errors', async () => {
      const passwordData = {
        current_password: 'oldpassword',
        new_password: 'newpassword123',
        confirm_password: 'differentpassword'
      };

      const error = {
        response: {
          data: {
            detail: 'New password and confirmation do not match'
          }
        }
      };
      mockApiClient.put.mockRejectedValue(error);

      await expect(profileService.changePassword(passwordData)).rejects.toEqual(error);
      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me/password', passwordData);
    });

    it('should handle server errors', async () => {
      const passwordData = {
        current_password: 'oldpassword',
        new_password: 'newpassword123',
        confirm_password: 'newpassword123'
      };

      const error = {
        response: {
          status: 500,
          data: {
            detail: 'Internal server error'
          }
        }
      };
      mockApiClient.put.mockRejectedValue(error);

      await expect(profileService.changePassword(passwordData)).rejects.toEqual(error);
      expect(mockApiClient.put).toHaveBeenCalledWith('/api/v1/users/me/password', passwordData);
    });
  });
});
