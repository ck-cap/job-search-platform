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
            <span class="text-sm text-gray-500">
              {{ filteredCompanies.length }} {{ filteredCompanies.length === 1 ? 'company' : 'companies' }} found
            </span>
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
                  class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Search by company name or industry..."
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
              <label for="industry" class="block text-sm font-medium text-gray-700 mb-2">
                Industry
              </label>
              <select
                id="industry"
                v-model="selectedIndustry"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Industries</option>
                <option v-for="industry in industries" :key="industry" :value="industry">
                  {{ industry }}
                </option>
              </select>
            </div>

            <!-- Company Size Filter -->
            <div>
              <label for="size" class="block text-sm font-medium text-gray-700 mb-2">
                Company Size
              </label>
              <select
                id="size"
                v-model="selectedSize"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Sizes</option>
                <option value="Startup (<100)">Startup (< 100)</option>
                <option value="Mid-size (100-500)">Mid-size (100-500)</option>
                <option value="Large (500+)">Large (500+)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Company Grid -->
      <div class="px-4 sm:px-0">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="company in filteredCompanies"
            :key="company.id"
            class="bg-white rounded-lg shadow hover:shadow-md transition-shadow overflow-hidden"
          >
            <!-- Company Header -->
            <div class="p-6 border-b border-gray-200">
              <div class="flex items-start justify-between">
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                    <span class="text-white font-bold text-lg">{{ company.name.charAt(0) }}</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">{{ company.name }}</h3>
                    <p class="text-sm text-gray-600">{{ company.industry }}</p>
                  </div>
                </div>
                <div class="flex flex-col items-end space-y-1">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ company.match }}% match
                  </span>
                  <span class="text-xs text-gray-500">{{ company.size }}</span>
                </div>
              </div>
            </div>

            <!-- Company Content -->
            <div class="p-6">
              <p class="text-gray-700 text-sm mb-4">{{ company.description }}</p>
              
              <!-- Required Skills -->
              <div class="mb-4">
                <h4 class="text-sm font-medium text-gray-900 mb-2">Required Skills</h4>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="skill in company.requiredSkills"
                    :key="skill"
                    class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {{ skill }}
                  </span>
                </div>
              </div>

              <!-- Experience Level -->
              <div class="mb-4">
                <div class="flex items-center text-sm">
                  <svg class="w-4 h-4 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span class="text-gray-600">Experience: {{ company.experienceLevel }}</span>
                </div>
              </div>

              <!-- Location if available -->
              <div v-if="company.location" class="mb-4">
                <div class="flex items-center text-sm">
                  <svg class="w-4 h-4 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  <span class="text-gray-600">{{ company.location }}</span>
                </div>
              </div>
            </div>

            <!-- Company Actions -->
            <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
              <div class="flex space-x-2">
                <button class="flex-1 bg-blue-600 text-white text-sm font-medium py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
                  View Details
                </button>
                <button class="px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-50 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredCompanies.length === 0" class="text-center py-12">
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
import { ref, computed } from 'vue'
import AppNavigation from '~/components/AppNavigation.vue'

// Search and filter state
const searchQuery = ref('')
const selectedIndustry = ref('')
const selectedSize = ref('')

// Company data
const companies = ref([
  {
    id: 1,
    name: 'TechCorp Solutions',
    industry: 'Technology',
    size: 'Mid-size (100-500)',
    match: 92,
    description: 'Leading software development company specializing in enterprise solutions and digital transformation.',
    requiredSkills: ['JavaScript', 'Python', 'React', 'Node.js', 'AWS'],
    experienceLevel: '2-5 years',
    location: 'San Francisco, CA'
  },
  {
    id: 2,
    name: 'DataMinds Analytics',
    industry: 'Data Science',
    size: 'Large (500+)',
    match: 88,
    description: 'Data analytics and machine learning company helping businesses make data-driven decisions.',
    requiredSkills: ['Python', 'SQL', 'Machine Learning', 'Data Analysis', 'TensorFlow'],
    experienceLevel: '3-6 years',
    location: 'New York, NY'
  },
  {
    id: 3,
    name: 'CloudFirst Technologies',
    industry: 'Cloud Computing',
    size: 'Startup (<100)',
    match: 85,
    description: 'Innovative cloud infrastructure solutions for modern businesses and scalable applications.',
    requiredSkills: ['AWS', 'Docker', 'Kubernetes', 'DevOps', 'Terraform'],
    experienceLevel: '1-4 years',
    location: 'Austin, TX'
  },
  {
    id: 4,
    name: 'InnovateLab Inc',
    industry: 'Research & Development',
    size: 'Mid-size (100-500)',
    match: 82,
    description: 'R&D company focused on emerging technologies, innovation, and breakthrough solutions.',
    requiredSkills: ['Research', 'Innovation', 'Project Management', 'Analysis', 'Prototyping'],
    experienceLevel: '2-5 years',
    location: 'Boston, MA'
  },
  {
    id: 5,
    name: 'GrowthTech Ventures',
    industry: 'FinTech',
    size: 'Large (500+)',
    match: 79,
    description: 'Financial technology company revolutionizing digital payments and banking solutions.',
    requiredSkills: ['Finance', 'Technology', 'Security', 'Compliance', 'Blockchain'],
    experienceLevel: '3-7 years',
    location: 'London, UK'
  },
  {
    id: 6,
    name: 'NextGen Robotics',
    industry: 'Robotics & AI',
    size: 'Mid-size (100-500)',
    match: 76,
    description: 'Cutting-edge robotics and AI solutions for industrial automation and smart manufacturing.',
    requiredSkills: ['AI', 'Robotics', 'Programming', 'Engineering', 'Computer Vision'],
    experienceLevel: '1-5 years',
    location: 'Tokyo, Japan'
  },
  {
    id: 7,
    name: 'GreenTech Solutions',
    industry: 'Sustainability',
    size: 'Startup (<100)',
    match: 74,
    description: 'Sustainable technology solutions for environmental challenges and clean energy.',
    requiredSkills: ['Sustainability', 'Clean Energy', 'Engineering', 'Data Analysis', 'IoT'],
    experienceLevel: '2-4 years',
    location: 'Copenhagen, Denmark'
  },
  {
    id: 8,
    name: 'HealthTech Innovations',
    industry: 'Healthcare',
    size: 'Large (500+)',
    match: 71,
    description: 'Healthcare technology company developing innovative medical devices and digital health solutions.',
    requiredSkills: ['Healthcare', 'Medical Devices', 'Regulatory', 'Software Development', 'Data Privacy'],
    experienceLevel: '2-6 years',
    location: 'Berlin, Germany'
  }
])

// Get unique industries for filter
const industries = computed(() => {
  const uniqueIndustries = [...new Set(companies.value.map(c => c.industry))]
  return uniqueIndustries.sort()
})

// Filter companies based on search and filters
const filteredCompanies = computed(() => {
  return companies.value.filter(company => {
    const matchesSearch = searchQuery.value === '' || 
      company.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      company.industry.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      company.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesIndustry = selectedIndustry.value === '' || company.industry === selectedIndustry.value
    const matchesSize = selectedSize.value === '' || company.size === selectedSize.value
    
    return matchesSearch && matchesIndustry && matchesSize
  }).sort((a, b) => b.match - a.match) // Sort by match percentage
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style> 