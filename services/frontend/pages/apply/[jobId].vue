<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <main class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Back Button -->
      <div class="mb-6">
        <button
          @click="goBack"
          class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          Back to Job Recommendations
        </button>
      </div>

      <!-- Job Details Card -->
      <div v-if="jobDetails" class="bg-white rounded-xl shadow-soft p-6 mb-8">
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1">
            <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ jobDetails.job_title }}</h1>
            <div class="flex items-center space-x-4 text-gray-600 mb-4">
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2m-2 0H7m14 0v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5"/>
                </svg>
                {{ jobDetails.company }}
              </div>
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                {{ jobDetails.location }}
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <div class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              {{ Math.round(jobDetails.score * 100) }}% match
            </div>
          </div>
        </div>

        <div class="flex flex-wrap gap-2 mb-4">
          <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {{ jobDetails.category }}
          </span>
          <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
            {{ jobDetails.type }}
          </span>
          <span v-if="jobDetails.salary" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
            {{ jobDetails.salary }}
          </span>
        </div>

        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-3">Job Description</h3>
          <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ jobDetails.job_description }}</p>
        </div>

        <div class="text-sm text-gray-500">
          <span>{{ jobDetails.subcategory }} • {{ jobDetails.role }}</span>
          <br>
          <span>Listed: {{ new Date(jobDetails.listingDate).toLocaleDateString() }}</span>
        </div>
      </div>

      <!-- Application Form -->
      <div class="bg-white rounded-xl shadow-soft p-6">
        <div class="mb-6">
          <h2 class="text-xl font-bold text-gray-900 mb-2">Apply for this Position</h2>
          <p class="text-gray-600">Fill out the form below to submit your application.</p>
        </div>

        <form @submit.prevent="submitApplication" class="space-y-6">
          <!-- Auto-fill notification -->
          <div v-if="hasAutoFilledData" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div class="flex items-start space-x-3">
              <svg class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <div>
                <p class="text-sm font-medium text-blue-800 mb-1">Information Auto-filled</p>
                <p class="text-xs text-blue-700">
                  We've pre-filled your personal details from your resume analysis. Please review and update if needed.
                </p>
              </div>
            </div>
          </div>

          <!-- Personal Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700 mb-2">
                First Name
                <span v-if="autoFilledFields.includes('name')" class="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  Auto-filled
                </span>
              </label>
              <input
                id="firstName"
                v-model="applicationForm.firstName"
                type="text"
                required
                :class="[
                  'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                  autoFilledFields.includes('name') ? 'border-blue-300 bg-blue-50' : 'border-gray-300'
                ]"
                placeholder="Enter your first name"
              />
            </div>
            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700 mb-2">
                Last Name
                <span v-if="autoFilledFields.includes('name')" class="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  Auto-filled
                </span>
              </label>
              <input
                id="lastName"
                v-model="applicationForm.lastName"
                type="text"
                required
                :class="[
                  'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                  autoFilledFields.includes('name') ? 'border-blue-300 bg-blue-50' : 'border-gray-300'
                ]"
                placeholder="Enter your last name"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                Email Address
                <span v-if="autoFilledFields.includes('email')" class="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  Auto-filled
                </span>
              </label>
              <input
                id="email"
                v-model="applicationForm.email"
                type="email"
                required
                :class="[
                  'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                  autoFilledFields.includes('email') ? 'border-blue-300 bg-blue-50' : 'border-gray-300'
                ]"
                placeholder="Enter your email"
              />
            </div>
            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
                Phone Number
                <span v-if="autoFilledFields.includes('phone')" class="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  Auto-filled
                </span>
              </label>
              <input
                id="phone"
                v-model="applicationForm.phone"
                type="tel"
                required
                :class="[
                  'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                  autoFilledFields.includes('phone') ? 'border-blue-300 bg-blue-50' : 'border-gray-300'
                ]"
                placeholder="Enter your phone number"
              />
            </div>
          </div>

          <!-- Resume Upload -->
          <div>
            <label for="resume" class="block text-sm font-medium text-gray-700 mb-2">Resume/CV</label>
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
              <input
                id="resume"
                type="file"
                @change="handleResumeUpload"
                accept=".pdf,.doc,.docx"
                class="hidden"
                ref="resumeInput"
              />
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div v-if="!applicationForm.resume">
                <button
                  type="button"
                  @click="$refs.resumeInput.click()"
                  class="text-indigo-600 hover:text-indigo-500 font-medium"
                >
                  Upload your resume
                </button>
                <p class="text-gray-500 text-sm mt-1">PDF, DOC, or DOCX up to 10MB</p>
              </div>
              <div v-else class="text-center">
                <div class="flex items-center justify-center space-x-2 text-green-600 mb-2">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <span class="font-medium">{{ applicationForm.resume.name }}</span>
                </div>
                <button
                  type="button"
                  @click="removeResume"
                  class="text-red-600 hover:text-red-500 text-sm font-medium"
                >
                  Remove file
                </button>
              </div>
            </div>
          </div>

          <!-- Cover Letter -->
          <div>
            <label for="coverLetter" class="block text-sm font-medium text-gray-700 mb-2">Cover Letter</label>
            <textarea
              id="coverLetter"
              v-model="applicationForm.coverLetter"
              rows="6"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Tell us why you're interested in this position and what makes you a great fit..."
            ></textarea>
          </div>

          <!-- Additional Information -->
          <div>
            <label for="additionalInfo" class="block text-sm font-medium text-gray-700 mb-2">Additional Information (Optional)</label>
            <textarea
              id="additionalInfo"
              v-model="applicationForm.additionalInfo"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Any additional information you'd like to share..."
            ></textarea>
          </div>

          <!-- Terms and Conditions -->
          <div class="flex items-start space-x-3">
            <input
              id="terms"
              v-model="applicationForm.agreeToTerms"
              type="checkbox"
              required
              class="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label for="terms" class="text-sm text-gray-700">
              I agree to the <a href="#" class="text-indigo-600 hover:text-indigo-500 font-medium">Terms and Conditions</a> and 
              <a href="#" class="text-indigo-600 hover:text-indigo-500 font-medium">Privacy Policy</a>
            </label>
          </div>

          <!-- Submit Button -->
          <div class="flex space-x-4">
            <button
              type="submit"
              :disabled="isSubmitting || !isFormValid"
              class="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <span v-if="isSubmitting" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Submitting Application...
              </span>
              <span v-else>Submit Application</span>
            </button>
          </div>
        </form>

        <!-- Success Message (hidden, now using popup) -->
        <div v-if="false" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            <div>
              <h3 class="text-sm font-medium text-green-800">Application Submitted Successfully!</h3>
              <p class="text-sm text-green-700 mt-1">
                Thank you for your application. We'll review it and get back to you within 3-5 business days.
              </p>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="applicationError" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <div>
              <h3 class="text-sm font-medium text-red-800">Error Submitting Application</h3>
              <p class="text-sm text-red-700 mt-1">{{ applicationError }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Success Popup Modal -->
    <div v-if="showSuccessModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4" @click="closeSuccessModal">
      <div class="relative bg-white rounded-xl shadow-2xl max-w-md w-full mx-auto transform transition-all duration-200 ease-out scale-100 opacity-100" @click.stop>
        <!-- Modal Header -->
        <div class="bg-green-500 rounded-t-xl px-6 py-4">
          <div class="flex items-center justify-center">
            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Modal Body -->
        <div class="px-6 py-6 text-center">
          <h3 class="text-xl font-bold text-gray-900 mb-2">Application Submitted Successfully!</h3>
          <p class="text-gray-600 mb-6 leading-relaxed">
            Thank you for your application to <strong>{{ jobDetails?.job_title }}</strong> at <strong>{{ jobDetails?.company }}</strong>. 
            We'll review your application and get back to you within 3-5 business days.
          </p>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div class="flex items-start space-x-3">
              <svg class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <div class="text-left">
                <p class="text-sm font-medium text-blue-800 mb-1">What's Next?</p>
                <ul class="text-xs text-blue-700 space-y-1">
                  <li>• Our hiring team will review your application</li>
                  <li>• You'll receive an email confirmation shortly</li>
                  <li>• We'll contact you if your profile matches our needs</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="flex space-x-3">
            <button
              @click="closeSuccessModal"
              class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              Close
            </button>
            <button
              @click="goBackToRecommendations"
              class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              View More Jobs
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppNavigation from '~/components/AppNavigation.vue'

// SEO
useHead({
  title: 'Apply for Job - Smart Resume Analyzer',
  meta: [
    { name: 'description', content: 'Apply for this job position through our smart application system.' }
  ]
})

// Router and route
const route = useRoute()
const router = useRouter()

// Reactive state
const jobDetails = ref<any>(null)
const isSubmitting = ref(false)
const applicationSubmitted = ref(false)
const showSuccessModal = ref(false)
const applicationError = ref<string | null>(null)
const resumeInput = ref<HTMLInputElement>()
const autoFilledFields = ref<string[]>([])

// Application form data
const applicationForm = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  resume: null as File | null,
  coverLetter: '',
  additionalInfo: '',
  agreeToTerms: false
})

// Form validation
const isFormValid = computed(() => {
  return (
    applicationForm.value.firstName.trim() !== '' &&
    applicationForm.value.lastName.trim() !== '' &&
    applicationForm.value.email.trim() !== '' &&
    applicationForm.value.phone.trim() !== '' &&
    applicationForm.value.resume !== null &&
    applicationForm.value.agreeToTerms
  )
})

// Check if any data was auto-filled
const hasAutoFilledData = computed(() => {
  return autoFilledFields.value.length > 0
})

// Methods
const goBack = () => {
  router.push('/')
}

const handleResumeUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    applicationForm.value.resume = target.files[0]
  }
}

const removeResume = () => {
  applicationForm.value.resume = null
  if (resumeInput.value) {
    resumeInput.value.value = ''
  }
}

const submitApplication = async () => {
  if (!isFormValid.value) return

  isSubmitting.value = true
  applicationError.value = null

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // In a real application, you would submit the form data to your backend API
    console.log('Submitting application:', {
      jobId: route.params.jobId,
      formData: applicationForm.value
    })

    // Scroll to top of page
    window.scrollTo({ top: 0, behavior: 'smooth' })
    
    // Show success modal after a brief delay to allow scroll
    setTimeout(() => {
      applicationSubmitted.value = true
      showSuccessModal.value = true
    }, 500)
    
    // Reset form after successful submission
    setTimeout(() => {
      applicationForm.value = {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        resume: null,
        coverLetter: '',
        additionalInfo: '',
        agreeToTerms: false
      }
      if (resumeInput.value) {
        resumeInput.value.value = ''
      }
    }, 3000)

  } catch (error) {
    console.error('Error submitting application:', error)
    applicationError.value = 'Failed to submit application. Please try again.'
    // Scroll to top to show error message
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    isSubmitting.value = false
  }
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
}

const goBackToRecommendations = () => {
  showSuccessModal.value = false
  router.push('/')
}

const autoFillUserDetails = () => {
  try {
    // Reset auto-filled fields tracker
    autoFilledFields.value = []
    
    // Get parsed resume data from session storage
    const storedParsedData = sessionStorage.getItem('resume_analyzer_parsed_data')
    if (storedParsedData) {
      const parsedData = JSON.parse(storedParsedData)
      
      // Get contact info from the parsed data
      const contactInfo = parsedData.contact_info || parsedData.parsed_data?.contact_info
      
      if (contactInfo) {
        // Split full name into first and last name
        if (contactInfo.name) {
          const nameParts = contactInfo.name.trim().split(' ')
          applicationForm.value.firstName = nameParts[0] || ''
          applicationForm.value.lastName = nameParts.slice(1).join(' ') || ''
          autoFilledFields.value.push('name')
        }
        
        // Fill email and phone
        if (contactInfo.email) {
          applicationForm.value.email = contactInfo.email
          autoFilledFields.value.push('email')
        }
        
        if (contactInfo.phone) {
          applicationForm.value.phone = contactInfo.phone
          autoFilledFields.value.push('phone')
        }
        
        console.log('✅ Auto-filled user details from resume:', {
          name: contactInfo.name,
          email: contactInfo.email,
          phone: contactInfo.phone,
          fieldsAutoFilled: autoFilledFields.value
        })
      }
    } else {
      console.log('ℹ️ No resume data found in session storage for auto-fill')
    }
  } catch (error) {
    console.error('❌ Error auto-filling user details:', error)
  }
}

// Load job details and auto-fill user data on mount
onMounted(() => {
  const jobId = route.params.jobId
  
  // Try to get job details from session storage (from job recommendations)
  const storedJobMatches = sessionStorage.getItem('resume_analyzer_job_matches')
  if (storedJobMatches) {
    try {
      const jobMatches = JSON.parse(storedJobMatches)
      jobDetails.value = jobMatches.find((job: any) => job.job_id === jobId)
    } catch (error) {
      console.error('Error parsing stored job matches:', error)
    }
  }

  // If job not found in storage, create a mock job for demo purposes
  if (!jobDetails.value) {
    jobDetails.value = {
      job_id: jobId,
      job_title: 'Senior Software Developer',
      company: 'Tech Solutions Inc.',
      location: 'Kuala Lumpur, Malaysia',
      category: 'Information Technology',
      type: 'Full-time',
      salary: 'RM 8,000 - RM 12,000',
      subcategory: 'Software Development',
      role: 'Senior',
      score: 0.95,
      listingDate: new Date().toISOString(),
      job_description: 'We are looking for a Senior Software Developer to join our dynamic team. The ideal candidate will have strong experience in full-stack development, modern frameworks, and agile methodologies. You will be responsible for designing, developing, and maintaining web applications while collaborating with cross-functional teams to deliver high-quality software solutions.'
    }
  }

  // Auto-fill user details from resume data
  autoFillUserDetails()

  // Handle Escape key to close modal
  const handleEscape = (event: KeyboardEvent) => {
    if (event.key === 'Escape' && showSuccessModal.value) {
      closeSuccessModal()
    }
  }
  
  document.addEventListener('keydown', handleEscape)
  
  // Cleanup event listener on unmount
  return () => {
    document.removeEventListener('keydown', handleEscape)
  }
})
</script> 