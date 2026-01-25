import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { User, LoginRequest, RegisterRequest } from '../types';
import { authApi } from '../api/auth';
import { storage } from '../utils/storage';
import { handleApiError } from '../api/client';

interface AuthContextData {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStoredUser();
  }, []);

  const loadStoredUser = async () => {
    try {
      const storedUser = await storage.getUser<User>();
      const token = await storage.getAccessToken();

      if (storedUser && token) {
        setUser(storedUser);
        // Optionally refresh user data from server
        try {
          const currentUser = await authApi.getCurrentUser();
          setUser(currentUser);
          await storage.setUser(currentUser);
        } catch {
          // Token might be expired, user will need to login
        }
      }
    } catch {
      // Error loading stored user - will show login screen
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials: LoginRequest) => {
    try {
      const response = await authApi.login(credentials);
      
      // Store tokens and user
      await storage.setTokens(response.access_token, response.refresh_token);
      await storage.setUser(response.user);
      
      setUser(response.user);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  };

  const register = async (userData: RegisterRequest) => {
    try {
      const response = await authApi.register(userData);
      
      // Store tokens and user
      await storage.setTokens(response.access_token, response.refresh_token);
      await storage.setUser(response.user);
      
      setUser(response.user);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  };

  const logout = async () => {
    // Clear all stored data
    await storage.clearTokens();
    await storage.clearUser();
    
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const currentUser = await authApi.getCurrentUser();
      setUser(currentUser);
      await storage.setUser(currentUser);
    } catch (error) {
      // Error refreshing user data
      throw new Error(handleApiError(error));
    }
  };

  const value: AuthContextData = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
