import apiClient from './client';
import { InventoryItem, InventoryListResponse, InventoryFilters } from '../types';

export const inventoryApi = {
  async getItems(
    page: number = 1,
    perPage: number = 20,
    filters?: InventoryFilters
  ): Promise<InventoryListResponse> {
    const params: any = { page, per_page: perPage };
    
    if (filters) {
      if (filters.search) params.search = filters.search;
      if (filters.merchant) params.merchant = filters.merchant;
      if (filters.category) params.category = filters.category;
      if (filters.condition) params.condition = filters.condition;
      if (filters.in_stock !== undefined) params.in_stock = filters.in_stock;
      if (filters.sort_by) params.sort_by = filters.sort_by;
      if (filters.sort_order) params.sort_order = filters.sort_order;
    }

    const response = await apiClient.get('/api/inventory', { params });
    return response.data;
  },

  async getItem(id: number): Promise<InventoryItem> {
    const response = await apiClient.get(`/api/inventory/${id}`);
    return response.data;
  },

  async createItem(item: Partial<InventoryItem>): Promise<InventoryItem> {
    const response = await apiClient.post('/api/inventory', item);
    return response.data;
  },

  async updateItem(id: number, updates: Partial<InventoryItem>): Promise<InventoryItem> {
    const response = await apiClient.put(`/api/inventory/${id}`, updates);
    return response.data;
  },

  async deleteItem(id: number): Promise<{ message: string }> {
    const response = await apiClient.delete(`/api/inventory/${id}`);
    return response.data;
  },
};
