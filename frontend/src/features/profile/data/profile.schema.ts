export interface ProfileUpdate {
  username?: string;
  email?: string;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

export interface ChangePasswordResponse {
  message: string;
}

export interface ProfileUser {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
