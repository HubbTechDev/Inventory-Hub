import AsyncStorage from '@react-native-async-storage/async-storage';
import { Config } from '../constants/Config';

export const storage = {
  async setItem(key: string, value: any): Promise<void> {
    try {
      const jsonValue = JSON.stringify(value);
      await AsyncStorage.setItem(key, jsonValue);
    } catch (error) {
      console.error(`Error saving ${key}:`, error);
      throw error;
    }
  },

  async getItem<T>(key: string): Promise<T | null> {
    try {
      const jsonValue = await AsyncStorage.getItem(key);
      return jsonValue != null ? JSON.parse(jsonValue) : null;
    } catch (error) {
      console.error(`Error reading ${key}:`, error);
      return null;
    }
  },

  async removeItem(key: string): Promise<void> {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error(`Error removing ${key}:`, error);
      throw error;
    }
  },

  async clear(): Promise<void> {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error('Error clearing storage:', error);
      throw error;
    }
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
