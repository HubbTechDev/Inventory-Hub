import apiClient from './client';
import {
  ScrapingJob,
  ScrapingJobWithItems,
  ScrapingJobsResponse,
  ScrapeRequest,
  ScrapeResponse,
} from '../types';

export const scrapingApi = {
  /**
   * Start a new upload/scraping job
   */
  async startScrape(request: ScrapeRequest): Promise<ScrapeResponse> {
    const response = await apiClient.post('/api/scraping/scrape', request);
    return response.data;
  },

  /**
   * Get list of upload/scraping jobs
   */
  async getJobs(
    page: number = 1,
    perPage: number = 20,
    status?: string
  ): Promise<ScrapingJobsResponse> {
    const params: any = { page, per_page: perPage };
    if (status) params.status = status;

    const response = await apiClient.get('/api/scraping/jobs', { params });
    return response.data;
  },

  /**
   * Get details of a specific upload/scraping job
   */
  async getJob(id: number): Promise<ScrapingJobWithItems> {
    const response = await apiClient.get(`/api/scraping/jobs/${id}`);
    return response.data;
  },
};
