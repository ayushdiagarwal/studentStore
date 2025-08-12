import React, { createContext, useContext, useReducer, useEffect, type ReactNode } from 'react';
import type { AuthState, User } from '../types/auth';
import authService from '../services/auth';

// Initial state
const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
};

// Action types
type AuthAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_USER'; payload: User }
  | { type: 'SET_TOKEN'; payload: string }
  | { type: 'SET_AUTHENTICATED'; payload: boolean }
  | { type: 'LOGOUT' }
  | { type: 'INITIALIZE_AUTH' };

// Reducer function
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_USER':
      return { ...state, user: action.payload, isAuthenticated: true };
    case 'SET_TOKEN':
      return { ...state, token: action.payload };
    case 'SET_AUTHENTICATED':
      return { ...state, isAuthenticated: action.payload };
    case 'LOGOUT':
      return { ...initialState, isLoading: false };
    case 'INITIALIZE_AUTH':
      return { ...state, isLoading: false };
    default:
      return state;
  }
};

// Context interface
interface AuthContextType {
  state: AuthState;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Initialize authentication state
  useEffect(() => {
    const initializeAuth = async () => {
      console.log('Initializing authentication...');
      try {
        if (authService.isAuthenticated()) {
          console.log('User appears to be authenticated, checking stored data...');
          const token = authService.getStoredToken();
          const user = authService.getStoredUser();
          
          if (token && user) {
            console.log('Found stored token and user, setting state...');
            dispatch({ type: 'SET_TOKEN', payload: token });
            dispatch({ type: 'SET_USER', payload: user });
            
            // Verify token is still valid by fetching current user
            try {
              console.log('Verifying token validity...');
              const currentUser = await authService.getCurrentUser();
              dispatch({ type: 'SET_USER', payload: currentUser });
              console.log('Token verified successfully');
            } catch {
              console.log('Token verification failed, clearing auth state');
              // Token is invalid, clear everything
              await authService.logout();
              dispatch({ type: 'LOGOUT' });
            }
          }
        } else {
          console.log('No stored authentication found');
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
      } finally {
        console.log('Authentication initialization complete');
        dispatch({ type: 'INITIALIZE_AUTH' });
      }
    };

    initializeAuth();
  }, []);

  // Login function
  const login = async () => {
    try {
      console.log('Login function called, setting loading state...');
      dispatch({ type: 'SET_LOADING', payload: true });
      console.log('Requesting Google OAuth URL...');
      const authUrl = await authService.getGoogleAuthUrl();
      console.log('Received Google OAuth URL, redirecting to:', authUrl);
      window.location.href = authUrl;
    } catch (error) {
      console.error('Login error:', error);
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Logout function
  const logout = async () => {
    try {
      console.log('Logout function called');
      dispatch({ type: 'SET_LOADING', payload: true });
      await authService.logout();
      dispatch({ type: 'LOGOUT' });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Refresh user data
  const refreshUser = async () => {
    try {
      if (state.isAuthenticated) {
        console.log('Refreshing user data...');
        const user = await authService.getCurrentUser();
        dispatch({ type: 'SET_USER', payload: user });
      }
    } catch (error) {
      console.error('Error refreshing user:', error);
    }
  };

  const value: AuthContextType = {
    state,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
