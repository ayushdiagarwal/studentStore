export interface User {
  id: string;
  email: string;
  name: string;
  profile_picture?: string;
  gender?: 'male' | 'female';
  hostel?: string;
  is_verified: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginResponse {
  auth_url: string;
}
