<template>
  <div class="relative" ref="selectRef">
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700 mb-2">
      {{ label }}
    </label>
    
    <!-- Input field -->
    <div class="relative">
      <input
        :id="inputId"
        v-model="searchQuery"
        @focus="showDropdown = true"
        @blur="handleBlur"
        @keydown="handleKeydown"
        :placeholder="placeholder"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white"
        autocomplete="off"
      />
      
      <!-- Dropdown arrow -->
      <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
        </svg>
      </div>
    </div>
    
    <!-- Dropdown -->
    <div 
      v-show="showDropdown" 
      class="absolute z-50 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-y-auto"
    >
      <!-- Clear option -->
      <div 
        v-if="allowClear"
        @mousedown.prevent="selectOption('')"
        class="px-3 py-2 text-sm text-gray-500 hover:bg-gray-100 cursor-pointer border-b border-gray-200"
      >
        {{ clearText }}
      </div>
      
      <!-- Filtered options -->
      <div
        v-for="(option, index) in filteredOptions"
        :key="option"
        @mousedown.prevent="selectOption(option)"
        :class="[
          'px-3 py-2 text-sm cursor-pointer transition-colors',
          index === highlightedIndex 
            ? 'bg-blue-100 text-blue-900' 
            : 'text-gray-900 hover:bg-gray-100'
        ]"
      >
        {{ option }}
      </div>
      
      <!-- No results -->
      <div 
        v-if="filteredOptions.length === 0" 
        class="px-3 py-2 text-sm text-gray-500 italic"
      >
        No options found
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

interface Props {
  modelValue: string
  options: string[]
  label?: string
  placeholder?: string
  allowClear?: boolean
  clearText?: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Search or select...',
  allowClear: true,
  clearText: 'All'
})

const emit = defineEmits<Emits>()

// Reactive data
const searchQuery = ref('')
const showDropdown = ref(false)
const highlightedIndex = ref(-1)
const selectRef = ref<HTMLElement>()
const inputId = ref(`searchable-select-${Math.random().toString(36).substr(2, 9)}`)

// Initialize search query with current value
onMounted(() => {
  searchQuery.value = props.modelValue
})

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  searchQuery.value = newValue
})

// Filtered options based on search query
const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options
  
  const query = searchQuery.value.toLowerCase()
  return props.options.filter(option => 
    option.toLowerCase().includes(query)
  )
})

// Handle option selection
function selectOption(option: string) {
  searchQuery.value = option
  showDropdown.value = false
  highlightedIndex.value = -1
  emit('update:modelValue', option)
}

// Handle input blur with delay to allow for option clicking
function handleBlur() {
  setTimeout(() => {
    showDropdown.value = false
    highlightedIndex.value = -1
  }, 150)
}

// Handle keyboard navigation
function handleKeydown(event: KeyboardEvent) {
  if (!showDropdown.value) {
    if (event.key === 'ArrowDown' || event.key === 'Enter') {
      showDropdown.value = true
      return
    }
  }
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      highlightedIndex.value = Math.min(highlightedIndex.value + 1, filteredOptions.value.length - 1)
      break
    case 'ArrowUp':
      event.preventDefault()
      highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
      break
    case 'Enter':
      event.preventDefault()
      if (highlightedIndex.value >= 0 && filteredOptions.value[highlightedIndex.value]) {
        selectOption(filteredOptions.value[highlightedIndex.value])
      } else if (filteredOptions.value.length === 1) {
        selectOption(filteredOptions.value[0])
      }
      break
    case 'Escape':
      showDropdown.value = false
      highlightedIndex.value = -1
      break
  }
}

// Close dropdown when clicking outside
function handleClickOutside(event: Event) {
  if (selectRef.value && !selectRef.value.contains(event.target as Node)) {
    showDropdown.value = false
    highlightedIndex.value = -1
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script> 