import AsyncStorage from '@react-native-async-storage/async-storage';
import { Config } from '../constants/Config';

export const storage = {
  async setItem(key: string, value: any): Promise<void> {
    const jsonValue = JSON.stringify(value);
    await AsyncStorage.setItem(key, jsonValue);
  },

  async getItem<T>(key: string): Promise<T | null> {
    try {
      const jsonValue = await AsyncStorage.getItem(key);
      return jsonValue != null ? JSON.parse(jsonValue) : null;
    } catch {
      // Return null on error to gracefully handle corrupted data
      return null;
    }
  },

  async removeItem(key: string): Promise<void> {
    await AsyncStorage.removeItem(key);
  },

  async clear(): Promise<void> {
    await AsyncStorage.clear();
  },

  // Token management
  async setTokens(accessToken: string, refreshToken: string): Promise<void> {
    await this.setItem(Config.STORAGE_KEYS.ACCESS_TOKEN, accessToken);
    await this.setItem(Config.STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
  },

  async getAccessToken(): Promise<string | null> {
    return this.getItem<string>(Config.STORAGE_KEYS.ACCESS_TOKEN);
  },

  async getRefreshToken(): Promise<string | null> {
    return this.getItem<string>(Config.STORAGE_KEYS.REFRESH_TOKEN);
  },

  async clearTokens(): Promise<void> {
    await this.removeItem(Config.STORAGE_KEYS.ACCESS_TOKEN);
    await this.removeItem(Config.STORAGE_KEYS.REFRESH_TOKEN);
  },

  // User management
  async setUser(user: any): Promise<void> {
    await this.setItem(Config.STORAGE_KEYS.USER, user);
  },

  async getUser<T>(): Promise<T | null> {
    return this.getItem<T>(Config.STORAGE_KEYS.USER);
  },

  async clearUser(): Promise<void> {
    await this.removeItem(Config.STORAGE_KEYS.USER);
  },
};
