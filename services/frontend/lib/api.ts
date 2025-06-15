// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000',
  ENDPOINTS: {
    COMPANIES: '/companies',
    COMPANY_DETAILS: '/companies/:slug',
    JOBS: '/jobs',
    REVIEWS: '/reviews/:companyName',
    INDUSTRIES: '/industries',
    RELOAD_DATA: '/reload-data'
  }
}

// API Helper functions
export class ApiService {
  private baseUrl: string

  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL
  }

  async get(endpoint: string, params?: Record<string, string>): Promise<any> {
    const url = new URL(endpoint, this.baseUrl)
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, value)
      })
    }

    const response = await fetch(url.toString())
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`)
    }
    
    return response.json()
  }

  async post(endpoint: string, data?: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    })

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`)
    }

    return response.json()
  }

  // Company-specific methods
  async getCompanies(filters?: {
    industry?: string
    size?: string
    search?: string
    page?: number
    limit?: number
  }) {
    const params: Record<string, string> = {}
    if (filters?.industry) params.industry = filters.industry
    if (filters?.size) params.size = filters.size
    if (filters?.search) params.search = filters.search
    if (filters?.page) params.page = filters.page.toString()
    if (filters?.limit) params.limit = filters.limit.toString()

    return this.get(API_CONFIG.ENDPOINTS.COMPANIES, Object.keys(params).length ? params : undefined)
  }

  async getCompanyDetails(companySlug: string) {
    const endpoint = API_CONFIG.ENDPOINTS.COMPANY_DETAILS.replace(':slug', companySlug)
    return this.get(endpoint)
  }

  async getJobs(filters?: {
    company?: string
    category?: string
    location?: string
    limit?: number
  }) {
    const params: Record<string, string> = {}
    if (filters?.company) params.company = filters.company
    if (filters?.category) params.category = filters.category
    if (filters?.location) params.location = filters.location
    if (filters?.limit) params.limit = filters.limit.toString()

    return this.get(API_CONFIG.ENDPOINTS.JOBS, Object.keys(params).length ? params : undefined)
  }

  async getCompanyReviews(companyName: string, limit?: number) {
    const endpoint = API_CONFIG.ENDPOINTS.REVIEWS.replace(':companyName', companyName)
    const params = limit ? { limit: limit.toString() } : undefined
    return this.get(endpoint, params)
  }

  async getIndustries() {
    return this.get(API_CONFIG.ENDPOINTS.INDUSTRIES)
  }

  async reloadData() {
    return this.post(API_CONFIG.ENDPOINTS.RELOAD_DATA)
  }
}

// Export singleton instance
export const apiService = new ApiService() 