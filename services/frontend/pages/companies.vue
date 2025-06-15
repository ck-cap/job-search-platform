<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="px-4 py-6 sm:px-0">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Company Directory</h1>
            <p class="mt-2 text-sm text-gray-600">
              Discover companies that match your skills and career goals
            </p>
          </div>
          <div class="mt-4 sm:mt-0">
            <span v-if="!isLoading && !error" class="text-sm text-gray-500">
              {{ pagination.total_companies }} {{ pagination.total_companies === 1 ? 'company' : 'companies' }} found
              <span v-if="pagination.total_pages > 1" class="ml-2">
                • Page {{ pagination.current_page }} of {{ pagination.total_pages }}
              </span>
            </span>
          </div>
        </div>

        <!-- Back to Results Banner (only shown if user has session data) -->
        <div v-if="hasResumeAnalysis" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
          <div class="flex items-start space-x-3">
            <svg class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div class="flex-1">
              <p class="text-sm font-medium text-blue-800 mb-1">Resume Analysis Available</p>
              <p class="text-xs text-blue-700 mb-3">You can return to your resume analysis results without re-uploading your resume.</p>
              <NuxtLink 
                to="/" 
                class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors shadow-sm hover:shadow-md"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                </svg>
                Back to Resume Analysis
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Search and Filters -->
      <div class="px-4 sm:px-0 mb-6">
                <div class="bg-white rounded-lg shadow p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Search -->
            <div>
              <label for="search" class="block text-sm font-medium text-gray-700 mb-2">
                Search Companies
              </label>
              <div class="relative">
                <input
                  id="search"
                  v-model="searchQuery"
                  type="text"
                  class="block w-full h-10 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Search by company name..."
                />
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Industry Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Industries
              </label>
              <div class="relative">
                <div 
                  @click="toggleIndustryDropdown"
                  class="block w-full h-10 px-3 py-2 border border-gray-300 rounded-md bg-white cursor-pointer focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 flex items-center justify-between"
                >
                  <span class="text-gray-900 truncate">
                    {{ selectedIndustries.length === 0 ? 'Select industries...' : 
                       selectedIndustries.length === 1 ? selectedIndustries[0] : 
                       `${selectedIndustries.length} industries selected` }}
                  </span>
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </div>
                
                <!-- Dropdown -->
                <div v-if="showIndustryDropdown" class="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                  <div class="p-2">
                    <input
                      v-model="industrySearch"
                      type="text"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Search industries..."
                    />
                  </div>
                  <div class="max-h-48 overflow-auto">
                    <div
                      v-for="industry in filteredIndustries"
                      :key="industry"
                      @click="toggleIndustry(industry)"
                      class="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center"
                    >
                      <input
                        type="checkbox"
                        :checked="selectedIndustries.includes(industry)"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded mr-3"
                        readonly
                      />
                      <span class="text-sm text-gray-900">{{ industry }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Clear All Button -->
            <div class="flex items-end">
              <button
                @click="clearAllFilters"
                class="w-full h-10 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-md transition-colors flex items-center justify-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
                Clear All
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="px-4 sm:px-0 text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading companies...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="px-4 sm:px-0 text-center py-12">
        <div class="text-red-600 mb-4">
          <svg class="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Failed to load companies</h3>
          <p class="text-gray-600 mb-4">{{ error }}</p>
          <button 
            @click="fetchCompanies"
            class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>

      <!-- Company Grid -->
      <div v-else class="px-4 sm:px-0">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch">
          <div
            v-for="company in companies"
            :key="company.id"
            class="bg-white rounded-lg shadow hover:shadow-md transition-shadow overflow-hidden flex flex-col"
          >
            <!-- Company Content -->
            <div class="p-6 flex-1 flex flex-col">
              <!-- Header -->
              <div class="flex items-center space-x-3 mb-4">
                <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                  <span class="text-white font-bold text-sm">{{ company.name.charAt(0) }}</span>
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-base font-semibold text-gray-900 truncate">{{ company.name }}</h3>
                  <p class="text-sm text-gray-500">{{ company.industry }}</p>
                </div>
              </div>
              
              <!-- Description -->
              <div class="text-gray-600 text-sm mb-4 flex-1">
                <p class="line-clamp-3 leading-relaxed">{{ company.description || 'No description available' }}</p>
              </div>
              
              <!-- Location -->
              <div class="flex items-center text-sm text-gray-500 mb-4">
                <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <span>{{ company.location || 'Malaysia' }}</span>
              </div>
            </div>

            <!-- Company Actions -->
            <div class="px-6 pb-6">
              <NuxtLink 
                :to="`/company/${company.name.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '')}`"
                class="block w-full bg-blue-600 text-white text-sm font-medium py-2.5 px-4 rounded-lg hover:bg-blue-700 transition-colors text-center"
              >
                View Details
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total_pages > 1" class="mt-8 flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="prevPage"
              :disabled="!pagination.has_prev"
              :class="[
                'relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md transition-colors',
                pagination.has_prev 
                  ? 'text-gray-700 bg-white hover:bg-gray-50' 
                  : 'text-gray-400 bg-gray-50 cursor-not-allowed'
              ]"
            >
              Previous
            </button>
            <button
              @click="nextPage"
              :disabled="!pagination.has_next"
              :class="[
                'ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md transition-colors',
                pagination.has_next 
                  ? 'text-gray-700 bg-white hover:bg-gray-50' 
                  : 'text-gray-400 bg-gray-50 cursor-not-allowed'
              ]"
            >
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing
                <span class="font-medium">{{ ((pagination.current_page - 1) * pagination.per_page) + 1 }}</span>
                to
                <span class="font-medium">{{ Math.min(pagination.current_page * pagination.per_page, pagination.total_companies) }}</span>
                of
                <span class="font-medium">{{ pagination.total_companies }}</span>
                results
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button
                  @click="prevPage"
                  :disabled="!pagination.has_prev"
                  :class="[
                    'relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 text-sm font-medium transition-colors',
                    pagination.has_prev 
                      ? 'text-gray-500 bg-white hover:bg-gray-50' 
                      : 'text-gray-300 bg-gray-50 cursor-not-allowed'
                  ]"
                >
                  <span class="sr-only">Previous</span>
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                
                <!-- Page numbers -->
                <template v-for="page in getPageNumbers()" :key="page">
                  <button
                    v-if="page !== '...'"
                    @click="goToPage(page)"
                    :class="[
                      'relative inline-flex items-center px-4 py-2 border text-sm font-medium transition-colors',
                      page === pagination.current_page
                        ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                        : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                    ]"
                  >
                    {{ page }}
                  </button>
                  <span
                    v-else
                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
                  >
                    ...
                  </span>
                </template>
                
                <button
                  @click="nextPage"
                  :disabled="!pagination.has_next"
                  :class="[
                    'relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 text-sm font-medium transition-colors',
                    pagination.has_next 
                      ? 'text-gray-500 bg-white hover:bg-gray-50' 
                      : 'text-gray-300 bg-gray-50 cursor-not-allowed'
                  ]"
                >
                  <span class="sr-only">Next</span>
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="companies.length === 0 && !isLoading" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No companies found</h3>
          <p class="mt-1 text-sm text-gray-500">Try adjusting your search criteria.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import AppNavigation from '~/components/AppNavigation.vue'

// Search and filter state
const searchQuery = ref('')
const selectedIndustries = ref([])
const showIndustryDropdown = ref(false)
const industrySearch = ref('')

// API Configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000'

// Company data
const companies = ref([])
const industries = ref([])
const isLoading = ref(false)
const error = ref(null)
const pagination = ref({
  current_page: 1,
  total_pages: 0,
  total_companies: 0,
  per_page: 12,
  has_next: false,
  has_prev: false
})

// Expanded descriptions tracking
const expandedDescriptions = ref(new Set())

// Current page
const currentPage = ref(1)



// Fetch companies from API
async function fetchCompanies() {
  isLoading.value = true
  error.value = null
  
  try {
    const params = new URLSearchParams()
    if (selectedIndustries.value.length > 0) {
      selectedIndustries.value.forEach(industry => {
        params.append('industry', industry)
      })
    }
    if (searchQuery.value) params.append('search', searchQuery.value)
    params.append('page', currentPage.value.toString())
    params.append('limit', '12')
    
    const response = await fetch(`${API_BASE_URL}/companies?${params}`)
    if (!response.ok) throw new Error('Failed to fetch companies')
    
    const data = await response.json()
    
    // Handle both old format (array) and new format (object with pagination)
    if (Array.isArray(data)) {
      // Old format - just an array of companies
      // This means pagination is happening server-side but not returning metadata
      companies.value = data
      
      // For old format, we need to make another call to get total count
      // But for now, let's assume there are more companies if we got exactly the limit
      const hasMoreCompanies = data.length === 12
      const estimatedTotal = hasMoreCompanies ? (currentPage.value * 12) + 1 : (currentPage.value - 1) * 12 + data.length
      const totalPages = Math.ceil(estimatedTotal / 12)
      
      pagination.value = {
        current_page: currentPage.value,
        total_pages: totalPages,
        total_companies: estimatedTotal,
        per_page: 12,
        has_next: hasMoreCompanies,
        has_prev: currentPage.value > 1
      }
      
    } else {
      // New format - object with companies and pagination
      companies.value = data.companies || []
      pagination.value = data.pagination || pagination.value
    }
  } catch (err) {
    error.value = err.message
    console.error('Error fetching companies:', err)
    // Fallback to empty array
    companies.value = []
    pagination.value = {
      current_page: 1,
      total_pages: 0,
      total_companies: 0,
      per_page: 12,
      has_next: false,
      has_prev: false
    }
  } finally {
    isLoading.value = false
  }
}

// Pagination functions
function goToPage(page: number) {
  if (page < 1 || page > pagination.value.total_pages) return
  currentPage.value = page
  fetchCompanies()
  // Scroll to top when changing pages
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function nextPage() {
  if (pagination.value.has_next) {
    goToPage(currentPage.value + 1)
  }
}

function prevPage() {
  if (pagination.value.has_prev) {
    goToPage(currentPage.value - 1)
  }
}

// Description expansion functions
function toggleDescription(companyId: number) {
  if (expandedDescriptions.value.has(companyId)) {
    expandedDescriptions.value.delete(companyId)
  } else {
    expandedDescriptions.value.add(companyId)
  }
}

function isDescriptionExpanded(companyId: number) {
  return expandedDescriptions.value.has(companyId)
}

function truncateDescription(description: string, maxLength: number = 150) {
  if (!description) return ''
  if (description.length <= maxLength) return description
  return description.substring(0, maxLength) + '...'
}

// Generate page numbers for pagination
function getPageNumbers() {
  const current = pagination.value.current_page
  const total = pagination.value.total_pages
  const delta = 2 // Number of pages to show on each side of current page
  
  if (total <= 7) {
    // Show all pages if total is small
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  
  const pages = []
  
  // Always show first page
  pages.push(1)
  
  if (current - delta > 2) {
    pages.push('...')
  }
  
  // Show pages around current
  for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
    pages.push(i)
  }
  
  if (current + delta < total - 1) {
    pages.push('...')
  }
  
  // Always show last page if more than 1 page
  if (total > 1) {
    pages.push(total)
  }
  
  return pages
}

// Industry dropdown functions
function toggleIndustryDropdown() {
  showIndustryDropdown.value = !showIndustryDropdown.value
}

function toggleIndustry(industry: string) {
  const index = selectedIndustries.value.indexOf(industry)
  if (index > -1) {
    selectedIndustries.value.splice(index, 1)
  } else {
    selectedIndustries.value.push(industry)
  }
}

function clearAllFilters() {
  searchQuery.value = ''
  selectedIndustries.value = []
  showIndustryDropdown.value = false
  industrySearch.value = ''
}

// Computed property for filtered industries
const filteredIndustries = computed(() => {
  if (!industrySearch.value) return industries.value
  return industries.value.filter(industry => 
    industry.toLowerCase().includes(industrySearch.value.toLowerCase())
  )
})

// Fetch industries from API
async function fetchIndustries() {
  try {
    const response = await fetch(`${API_BASE_URL}/industries`)
    if (!response.ok) throw new Error('Failed to fetch industries')
    
    industries.value = await response.json()
  } catch (err) {
    console.error('Error fetching industries:', err)
    // Fallback industries
    industries.value = ['Technology', 'Data Science', 'Cloud Computing', 'FinTech', 'Healthcare']
  }
}

// Watch for filter changes and refetch data
watch([selectedIndustries, searchQuery], () => {
  currentPage.value = 1 // Reset to first page when filters change
  fetchCompanies()
}, { debounce: 300, deep: true })

// Close dropdown when clicking outside
function handleClickOutside(event: Event) {
  const target = event.target as Element
  if (!target.closest('.relative')) {
    showIndustryDropdown.value = false
  }
}

// Load data on mount
onMounted(async () => {
  await Promise.all([fetchCompanies(), fetchIndustries()])
  
  // Add click outside listener
  document.addEventListener('click', handleClickOutside)
})

// Cleanup on unmount
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Companies are now filtered and paginated by the API

// Check if user has resume analysis data in session
const hasResumeAnalysis = computed(() => {
  if (process.client) {
    const hasAnalysisData = sessionStorage.getItem('resume_analyzer_current_view') === 'results' &&
                           sessionStorage.getItem('resume_analyzer_parsed_data');
    return hasAnalysisData;
  }
  return false;
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 