import axios from 'axios';
import type { TokenResponse, LoginResponse, User } from '../types/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002/api/v1';

console.log('Auth Service initialized with API URL:', API_BASE_URL);

// Create axios instance with base configuration
const authApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
authApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  console.log('Making request to:', config.url, 'with headers:', config.headers);
  return config;
});

// Handle token expiration
authApi.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data, error.message);
    if (error.response?.status === 401) {
      // Token expired or invalid, clear local storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  // Get Google OAuth URL
  async getGoogleAuthUrl(): Promise<string> {
    try {
      console.log('Requesting Google OAuth URL from:', `${API_BASE_URL}/auth/google/login`);
      const response = await authApi.get<LoginResponse>('/auth/google/login');
      console.log('Google OAuth URL received:', response.data.auth_url);
      return response.data.auth_url;
    } catch (error) {
      console.error('Error getting Google auth URL:', error);
      throw error;
    }
  },

  // Handle Google OAuth callback
  async handleGoogleCallback(code: string): Promise<TokenResponse> {
    try {
      console.log('Handling Google callback with code:', code);
      const response = await authApi.post<TokenResponse>('/auth/google/callback', {
        code,
      });
      
      console.log('Google callback successful, storing token');
      // Store token and user data
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      return response.data;
    } catch (error) {
      console.error('Error handling Google callback:', error);
      throw error;
    }
  },

  // Get current user
  async getCurrentUser(): Promise<User> {
    try {
      console.log('Getting current user');
      const response = await authApi.get<User>('/auth/me');
      return response.data;
    } catch (error) {
      console.error('Error getting current user:', error);
      throw error;
    }
  },

  // Logout
  async logout(): Promise<void> {
    try {
      console.log('Logging out');
      await authApi.post('/auth/logout');
    } catch (error) {
      console.error('Error during logout:', error);
    } finally {
      // Clear local storage regardless of API call success
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token');
    return !!token;
  },

  // Get stored user data
  getStoredUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch (error) {
        console.error('Error parsing stored user:', error);
        return null;
      }
    }
    return null;
  },

  // Get stored token
  getStoredToken(): string | null {
    return localStorage.getItem('access_token');
  },
};

export default authService;
