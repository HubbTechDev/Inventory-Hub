import apiClient from './client';
import { Statistics } from '../types';

export const statsApi = {
  async getStatistics(): Promise<Statistics> {
    const response = await apiClient.get('/api/stats');
    return response.data;
  },
};
