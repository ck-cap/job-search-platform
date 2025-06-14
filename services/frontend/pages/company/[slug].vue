<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Breadcrumb -->
      <nav class="flex mb-8" aria-label="Breadcrumb">
        <ol class="inline-flex items-center space-x-1 md:space-x-3">
          <li class="inline-flex items-center">
            <NuxtLink to="/" class="text-gray-600 hover:text-indigo-600 transition-colors">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
              </svg>
            </NuxtLink>
          </li>
          <li>
            <div class="flex items-center">
              <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd"/>
              </svg>
              <span class="ml-1 text-gray-900 font-medium">{{ companyData.name }}</span>
            </div>
          </li>
        </ol>
      </nav>

      <!-- Back to Results Banner (only shown if user has session data) -->
      <div v-if="hasResumeAnalysis" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
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

      <!-- Company Header -->
      <div class="bg-white rounded-xl shadow-soft p-6 mb-8">
        <div class="flex items-start space-x-6">
          <div class="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white text-2xl font-bold shadow-medium">
            {{ companyData.name.charAt(0) }}
          </div>
          <div class="flex-1">
            <div class="flex items-start justify-between">
              <div>
                <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ companyData.name }}</h1>
                <p class="text-lg text-gray-600 mb-4">{{ companyData.tagline }}</p>
                <div class="flex items-center space-x-4 text-sm text-gray-500">
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    {{ companyData.location }}
                  </div>
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2m-2 0H7m14 0v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5"/>
                    </svg>
                    {{ companyData.industry }}
                  </div>
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
                    </svg>
                    {{ companyData.size }}
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <div class="flex items-center bg-green-100 text-green-800 px-3 py-2 rounded-full">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                  <span class="font-medium">{{ companyData.rating }}/5</span>
                  <span class="text-sm ml-1">({{ companyData.reviewCount }} reviews)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-8">
          <!-- About Section -->
          <div class="bg-white rounded-xl shadow-soft p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">About {{ companyData.name }}</h2>
            <div class="prose prose-gray max-w-none">
              <p class="text-gray-700 leading-relaxed mb-4">{{ companyData.description }}</p>
              <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">Mission & Values</h3>
              <p class="text-gray-700 leading-relaxed">{{ companyData.mission }}</p>
            </div>
          </div>

          <!-- Open Jobs Section -->
          <div class="bg-white rounded-xl shadow-soft p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-2xl font-bold text-gray-900">Open Positions</h2>
              <span class="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
                {{ companyData.openJobs.length }} positions
              </span>
            </div>
            <div class="space-y-4">
              <div v-for="job in companyData.openJobs" :key="job.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">{{ job.title }}</h3>
                    <p class="text-sm text-gray-600">{{ job.department }} • {{ job.location }}</p>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                      {{ job.type }}
                    </span>
                    <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                      {{ job.salary }}
                    </span>
                  </div>
                </div>
                <p class="text-sm text-gray-700 mb-3">{{ job.description }}</p>
                <div class="flex justify-between items-center">
                  <div class="flex flex-wrap gap-1">
                    <span v-for="skill in job.skills" :key="skill" class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                      {{ skill }}
                    </span>
                  </div>
                  <button class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                    Apply Now
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Reviews Section -->
          <div class="bg-white rounded-xl shadow-soft p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-2xl font-bold text-gray-900">Summarize reviews</h2>
            </div>
            
            <!-- Reviews Summary -->
            <div class="bg-gray-50 rounded-lg p-4 mb-6">
              <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="text-center">
                  <div class="text-3xl font-bold text-indigo-600 mb-1">{{ companyData.rating }}</div>
                  <div class="flex justify-center mb-1">
                    <div v-for="i in 5" :key="i" class="text-yellow-400">
                      <svg class="w-4 h-4" :class="i <= companyData.rating ? 'fill-current' : 'text-gray-300'" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                    </div>
                  </div>
                  <div class="text-sm text-gray-600">Overall Rating</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-green-600 mb-1">{{ companyData.workLifeBalance }}/5</div>
                  <div class="text-sm text-gray-600">Work-Life Balance</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-blue-600 mb-1">{{ companyData.culture }}/5</div>
                  <div class="text-sm text-gray-600">Culture & Values</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-purple-600 mb-1">{{ companyData.careerOpportunities }}/5</div>
                  <div class="text-sm text-gray-600">Career Opportunities</div>
                </div>
              </div>
            </div>

            <!-- Individual Reviews -->
            <div class="space-y-6">
              <div v-for="review in companyData.reviews" :key="review.id" class="border-b border-gray-200 pb-6 last:border-b-0">
                <div class="flex items-start justify-between mb-6">
                  <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-3">
                      <div class="flex">
                        <div v-for="i in 5" :key="i" class="text-yellow-400">
                          <svg class="w-5 h-5" :class="i <= review.rating ? 'fill-current' : 'text-gray-300'" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                          </svg>
                        </div>
                      </div>
                      <h3 class="text-lg font-semibold text-gray-900">{{ review.title }}</h3>
                    </div>
                    <div class="flex items-center text-sm text-gray-600 space-x-2 pl-7">
                      <span>{{ review.position }}</span>
                      <span>•</span>
                      <span>{{ review.location }}</span>
                      <span>•</span>
                      <span>{{ review.date }}</span>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2 ml-4">
                    <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">
                      {{ review.employment }}
                    </span>
                  </div>
                </div>
                <div class="space-y-6">
                  <div>
                    <h4 class="text-lg font-semibold text-green-800 mb-3 flex items-center">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L9 7v3m-3 10v-5a2 2 0 012-2h2.5a2 2 0 011.732 1z"/>
                      </svg>
                      Pros
                    </h4>
                    <p class="text-gray-700 leading-relaxed pl-7">{{ review.pros }}</p>
                  </div>
                  <div>
                    <h4 class="text-lg font-semibold text-red-800 mb-3 flex items-center">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 13l3 3 7-7m-8-6a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      Cons
                    </h4>
                    <p class="text-gray-700 leading-relaxed pl-7">{{ review.cons }}</p>
                  </div>
                  <div>
                    <h4 class="text-lg font-semibold text-blue-800 mb-3 flex items-center">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                      </svg>
                      Advice to Management
                    </h4>
                    <p class="text-gray-700 leading-relaxed pl-7">{{ review.advice }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-8">
          <!-- Company Stats -->
          <div class="bg-white rounded-xl shadow-soft p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Company Stats</h3>
            <div class="space-y-4">
              <div class="flex justify-between items-center">
                <span class="text-gray-600">Founded</span>
                <span class="font-medium text-gray-900">{{ companyData.founded }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600">Employees</span>
                <span class="font-medium text-gray-900">{{ companyData.employeeCount }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600">Headquarters</span>
                <span class="font-medium text-gray-900">{{ companyData.headquarters }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600">Website</span>
                <a :href="companyData.website" target="_blank" class="text-indigo-600 hover:text-indigo-700 font-medium">
                  Visit Site
                </a>
              </div>
            </div>
          </div>

          <!-- Benefits -->
          <div class="bg-white rounded-xl shadow-soft p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Benefits & Perks</h3>
            <div class="space-y-3">
              <div v-for="benefit in companyData.benefits" :key="benefit" class="flex items-center space-x-2">
                <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                </svg>
                <span class="text-sm text-gray-700">{{ benefit }}</span>
              </div>
            </div>
          </div>

          <!-- Similar Companies -->
          <div class="bg-white rounded-xl shadow-soft p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Similar Companies</h3>
            <div class="space-y-3">
              <div v-for="company in companyData.similarCompanies" :key="company.name" class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">
                    {{ company.name.charAt(0) }}
                  </div>
                  <div>
                    <div class="font-medium text-gray-900">{{ company.name }}</div>
                    <div class="text-xs text-gray-600">{{ company.industry }}</div>
                  </div>
                </div>
                <div class="flex items-center text-yellow-400">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                  <span class="text-sm font-medium text-gray-900">{{ company.rating }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import AppNavigation from '~/components/AppNavigation.vue';

// Get the company slug from the route
const route = useRoute();
const companySlug = route.params.slug as string;

// Convert slug back to company name (this is a simple example)
const companyName = companySlug
  .split('-')
  .map(word => word.charAt(0).toUpperCase() + word.slice(1))
  .join(' ');

// Check if user has resume analysis data in session
const hasResumeAnalysis = computed(() => {
  if (process.client) {
    const hasAnalysisData = sessionStorage.getItem('resume_analyzer_current_view') === 'results' &&
                           sessionStorage.getItem('resume_analyzer_parsed_data');
    return hasAnalysisData;
  }
  return false;
});

// Dummy company data - in a real app, this would come from an API
const companyData = {
  name: companyName,
  tagline: "Innovating the future of technology",
  location: "Kuala Lumpur, Malaysia",
  industry: "Technology",
  size: "500-1000 employees",
  rating: 4.2,
  reviewCount: 156,
  workLifeBalance: 4.1,
  culture: 4.3,
  careerOpportunities: 4.0,
  founded: "2010",
  employeeCount: "750+",
  headquarters: "Kuala Lumpur, Malaysia",
  website: "https://example.com",
  description: "We are a leading technology company focused on developing innovative solutions for businesses worldwide. Our team of talented professionals works on cutting-edge projects that make a real impact in various industries including finance, healthcare, and e-commerce.",
  mission: "To empower businesses through innovative technology solutions while fostering a collaborative and inclusive work environment that enables our team members to grow and thrive.",
  benefits: [
    "Health Insurance",
    "Dental Coverage",
    "Flexible Working Hours",
    "Remote Work Options",
    "Professional Development",
    "Annual Bonus",
    "Stock Options",
    "Gym Membership",
    "Free Meals",
    "Transportation Allowance"
  ],
  openJobs: [
    {
      id: "1",
      title: "Senior Software Engineer",
      department: "Engineering",
      location: "Kuala Lumpur",
      type: "Full-time",
      salary: "RM 8,000 - 12,000",
      description: "We're looking for a senior software engineer to join our growing team and help build scalable applications.",
      skills: ["JavaScript", "React", "Node.js", "AWS", "MongoDB"]
    },
    {
      id: "2",
      title: "Data Analyst",
      department: "Analytics",
      location: "Kuala Lumpur",
      type: "Full-time",
      salary: "RM 5,000 - 8,000",
      description: "Join our data team to help derive insights from large datasets and support business decisions.",
      skills: ["Python", "SQL", "Tableau", "Statistics", "Machine Learning"]
    },
    {
      id: "3",
      title: "UX Designer",
      department: "Design",
      location: "Remote",
      type: "Contract",
      salary: "RM 4,000 - 6,000",
      description: "Create exceptional user experiences for our digital products and work closely with product teams.",
      skills: ["Figma", "User Research", "Prototyping", "Design Systems", "HTML/CSS"]
    }
  ],
  reviews: [
    {
      id: 1,
      rating: 4,
      title: "Great place to grow your career",
      position: "Software Engineer",
      location: "Kuala Lumpur",
      date: "Dec 2023",
      employment: "Current Employee",
      pros: "Excellent learning opportunities, supportive management, and great work-life balance. The company invests heavily in employee development and provides cutting-edge technology to work with.",
      cons: "Sometimes projects can be overwhelming due to tight deadlines. Office space could be improved for better collaboration.",
      advice: "Continue investing in employee development programs and consider expanding the office space to accommodate the growing team."
    },
    {
      id: 2,
      rating: 5,
      title: "Amazing company culture",
      position: "Product Manager",
      location: "Kuala Lumpur",
      date: "Nov 2023",
      employment: "Current Employee",
      pros: "The company has an incredible culture that promotes innovation and collaboration. Management is transparent and employees are valued. Great benefits package.",
      cons: "Fast-paced environment might not be suitable for everyone. Sometimes communication between departments could be better.",
      advice: "Keep up the great work! Maybe implement cross-departmental workshops to improve communication."
    },
    {
      id: 3,
      rating: 3,
      title: "Good experience overall",
      position: "Data Analyst",
      location: "Kuala Lumpur", 
      date: "Oct 2023",
      employment: "Former Employee",
      pros: "Good salary, interesting projects, and decent work-life balance. Learned a lot during my time here.",
      cons: "Limited career advancement opportunities in my department. Some processes could be more streamlined.",
      advice: "Focus on creating clearer career progression paths and streamlining internal processes."
    }
  ],
  similarCompanies: [
    { name: "TechCorp Solutions", industry: "Software Development", rating: 4.1 },
    { name: "DataMinds Analytics", industry: "Data Science", rating: 4.3 },
    { name: "CloudFirst Technologies", industry: "Cloud Computing", rating: 4.0 }
  ]
};

// SEO
useHead({
  title: `${companyData.name} - Company Profile & Reviews`,
  meta: [
    { name: 'description', content: `Learn about ${companyData.name}, read employee reviews, and explore open positions. ${companyData.tagline}` }
  ]
});
</script>

<style scoped>
.prose {
  max-width: none;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 