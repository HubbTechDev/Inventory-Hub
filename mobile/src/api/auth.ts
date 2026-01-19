import apiClient from './client';
import { LoginRequest, RegisterRequest, AuthResponse, User } from '../types';

export const authApi = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post('/api/auth/login', credentials);
    return response.data;
  },

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post('/api/auth/register', userData);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get('/api/auth/me');
    return response.data;
  },

  async refreshToken(refreshToken: string): Promise<{ access_token: string }> {
    const response = await apiClient.post(
      '/api/auth/refresh',
      {},
      {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      }
    );
    return response.data;
  },
};
