<template>
  <div class="card hover:shadow-medium transition-all duration-300 hover:border-primary-300 group h-full flex flex-col">
    <div class="card-body flex-1 flex flex-col">
      <div class="flex items-start space-x-3 sm:space-x-4 mb-3 sm:mb-4">
        <div class="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-base sm:text-lg shadow-soft flex-shrink-0">
          {{ company.name.charAt(0) }}
        </div>
        <div class="flex-1 min-w-0">
          <h3 class="font-semibold text-gray-900 mb-1 group-hover:text-primary-700 transition-colors line-clamp-2 text-sm sm:text-base">{{ company.name }}</h3>
          <p class="text-xs sm:text-sm text-gray-600 mb-2 sm:mb-3">{{ company.industry }}</p>
          <div class="flex flex-col space-y-1 sm:flex-row sm:items-center sm:space-y-0 sm:space-x-2 mb-2 sm:mb-3">
            <span class="px-2 py-1 bg-primary-100 text-primary-800 text-xs rounded-full font-medium self-start">{{ company.size }}</span>
            <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full font-medium self-start">{{ company.match }}% match</span>
          </div>
        </div>
      </div>
      
      <div class="flex-1 flex flex-col justify-between">
        <div class="space-y-3 sm:space-y-4 mb-3 sm:mb-4">
          <p class="text-xs sm:text-sm text-gray-700 leading-relaxed line-clamp-3">{{ company.description }}</p>
          
          <div class="space-y-2 sm:space-y-3">
            <div class="text-xs text-gray-600">
              <span class="font-semibold text-gray-700">Industry:</span> 
              <span class="ml-1">{{ company.industry }}</span>
            </div>
            <div class="text-xs text-gray-600">
              <span class="font-semibold text-gray-700">Company Size:</span> 
              <span class="ml-1">{{ company.size }}</span>
            </div>
          </div>
        </div>
        
        <div class="pt-3 sm:pt-4 border-t border-gray-100 mt-auto">
          <button 
            @click="viewOpportunities"
            class="w-full py-2 sm:py-3 px-3 sm:px-4 bg-primary-600 hover:bg-primary-700 text-white font-semibold text-xs sm:text-sm rounded-lg transition-all duration-300 shadow-soft hover:shadow-medium transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 min-h-[2.5rem] sm:min-h-[3rem] flex items-center justify-center"
          >
            View Opportunities
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Company {
  id: number;
  name: string;
  industry: string;
  size: string;
  match: number;
  description: string;
}

interface Props {
  company: Company;
}

const props = defineProps<Props>();

function viewOpportunities() {
  // In a real application, this would navigate to the company's opportunities page
  // For now, we'll just show an alert
  alert(`Opening opportunities for ${props.company.name}...`);
}
</script> 