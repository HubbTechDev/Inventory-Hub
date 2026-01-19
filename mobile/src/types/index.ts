export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
  updated_at?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  access_token: string;
  refresh_token: string;
}

export interface InventoryItem {
  id: number;
  user_id: number;
  job_id?: number;
  title: string;
  price: number;
  currency: string;
  quantity: number;
  sku: string;
  description?: string;
  category?: string;
  brand?: string;
  condition?: string;
  image_url?: string;
  product_url?: string;
  merchant: string;
  in_stock: boolean;
  custom_fields?: Record<string, any>;
  scraped_at?: string;
  created_at: string;
  updated_at: string;
}

export interface PaginationInfo {
  page: number;
  per_page: number;
  total_items: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface InventoryListResponse {
  items: InventoryItem[];
  pagination: PaginationInfo;
}

export interface InventoryFilters {
  search?: string;
  merchant?: string;
  category?: string;
  condition?: string;
  in_stock?: boolean;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface ScrapingJob {
  id: number;
  user_id: number;
  merchant: string;
  url: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  items_scraped: number;
  error_message?: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  duration_seconds?: number;
}

export interface ScrapingJobWithItems extends ScrapingJob {
  items: InventoryItem[];
}

export interface ScrapingJobsResponse {
  jobs: ScrapingJob[];
  pagination: PaginationInfo;
}

export interface ScrapeRequest {
  url: string;
  merchant: string;
  max_pages?: number;
}

export interface ScrapeResponse {
  message: string;
  job: ScrapingJob;
}

export interface Statistics {
  inventory: {
    total_items: number;
    items_in_stock: number;
    items_out_of_stock: number;
    total_value: number;
    items_last_week: number;
    items_last_month: number;
  };
  merchants: Array<{ merchant: string; count: number }>;
  conditions: Array<{ condition: string; count: number }>;
  categories: Array<{ category: string; count: number }>;
  scraping_jobs: {
    total_jobs: number;
    successful_jobs: number;
    failed_jobs: number;
    pending_jobs: number;
    recent_jobs: ScrapingJob[];
  };
}

export interface ApiError {
  error: string;
}

export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
};

export type AuthStackParamList = {
  Login: undefined;
  Register: undefined;
};

export type MainTabParamList = {
  Dashboard: undefined;
  Inventory: undefined;
  Scrape: undefined;
  History: undefined;
  Profile: undefined;
};

export type InventoryStackParamList = {
  InventoryList: undefined;
  InventoryDetail: { itemId: number };
};
