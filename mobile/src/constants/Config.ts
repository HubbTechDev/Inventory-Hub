export const Config = {
  API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:5000',
  API_TIMEOUT: parseInt(process.env.API_TIMEOUT || '30000', 10),
  
  // Pagination
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
  
  // Scraping
  MAX_SCRAPING_PAGES: 10,
  DEFAULT_SCRAPING_PAGES: 1,
  
  // Supported merchants
  MERCHANTS: ['Mercari', 'Depop', 'Generic', 'Custom'],
  
  // Item conditions
  CONDITIONS: ['new', 'like new', 'used', 'fair', 'poor'],
  
  // Sort options
  SORT_OPTIONS: [
    { label: 'Newest First', value: 'created_at', order: 'desc' },
    { label: 'Oldest First', value: 'created_at', order: 'asc' },
    { label: 'Price: Low to High', value: 'price', order: 'asc' },
    { label: 'Price: High to Low', value: 'price', order: 'desc' },
    { label: 'Title: A-Z', value: 'title', order: 'asc' },
    { label: 'Title: Z-A', value: 'title', order: 'desc' },
  ],
  
  // Storage keys
  STORAGE_KEYS: {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    USER: 'user',
    API_URL: 'api_url',
    THEME: 'theme',
  },
  
  // Cache duration (ms)
  CACHE_DURATION: 5 * 60 * 1000, // 5 minutes
};

export default Config;
