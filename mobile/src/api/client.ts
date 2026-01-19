import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { Config } from '../constants/Config';
import { storage } from '../utils/storage';

let apiBaseUrl = Config.API_BASE_URL;

export const setApiBaseUrl = (url: string) => {
  apiBaseUrl = url;
  apiClient.defaults.baseURL = url;
};

export const getApiBaseUrl = () => apiBaseUrl;

const apiClient: AxiosInstance = axios.create({
  baseURL: apiBaseUrl,
  timeout: Config.API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const token = await storage.getAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = await storage.getRefreshToken();
        
        if (!refreshToken) {
          // No refresh token, user needs to login
          await storage.clearTokens();
          return Promise.reject(error);
        }

        // Try to refresh the token
        const response = await axios.post(
          `${apiBaseUrl}/api/auth/refresh`,
          {},
          {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          }
        );

        const { access_token } = response.data;
        await storage.setItem(Config.STORAGE_KEYS.ACCESS_TOKEN, access_token);

        // Retry the original request with new token
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed, clear tokens and reject
        await storage.clearTokens();
        await storage.clearUser();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const handleApiError = (error: any): string => {
  if (error.response) {
    // Server responded with error
    return error.response.data?.error || error.response.data?.message || 'Server error occurred';
  } else if (error.request) {
    // Request made but no response
    return 'Network error. Please check your connection.';
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred';
  }
};

export default apiClient;
