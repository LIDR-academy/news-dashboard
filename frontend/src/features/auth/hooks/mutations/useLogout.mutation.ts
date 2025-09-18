
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { authService } from "../../data/auth.service";

export const useLogoutMutation = () => {
  const queryClient = useQueryClient();

  const logoutMutation = useMutation({
    mutationFn: async () => {
      // Call backend logout endpoint first
      await authService.logout();
    },
    onSuccess: () => {
      // Clear query cache after successful backend logout
      queryClient.clear();
    },
    onError: (error) => {
      // Still clear cache even if backend call fails
      // This ensures user is logged out locally
      queryClient.clear();
      console.error('Logout error:', error);
    }
  });

  return {
    action: logoutMutation.mutateAsync,
    isLoading: logoutMutation.isPending,
    error: logoutMutation.error,
    isSuccess: logoutMutation.isSuccess
  };
};
