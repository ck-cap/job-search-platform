<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <main class="max-w-6xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Progress Indicator -->
      <div class="mb-8 sm:mb-12 animate-fade-in">
        <!-- Horizontal Progress (lg and up) -->
        <div class="hidden lg:flex items-center justify-center space-x-2 sm:space-x-4">
          <div v-for="(step, index) in progressSteps" :key="index" class="flex items-center flex-shrink-0">
            <div class="flex items-center space-x-2 sm:space-x-3">
              <div :class="[
                'w-8 h-8 sm:w-10 sm:h-10 rounded-full flex items-center justify-center text-xs sm:text-sm font-medium transition-all duration-300 shadow-soft',
                currentView === step.view 
                  ? 'bg-primary-500 text-white ring-2 sm:ring-4 ring-primary-100' :
                isStepCompleted(step.view) 
                  ? 'bg-green-500 text-white' :
                'bg-gray-200 text-gray-500'
              ]">
                <svg v-if="isStepCompleted(step.view)" class="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span v-else class="font-semibold">{{ index + 1 }}</span>
              </div>
              <span :class="[
                'text-xs sm:text-sm font-medium transition-colors duration-300 whitespace-nowrap',
                currentView === step.view ? 'text-primary-600' :
                isStepCompleted(step.view) ? 'text-green-600' :
                'text-gray-500'
              ]">{{ step.label }}</span>
            </div>
            <div v-if="index < progressSteps.length - 1" :class="[
              'w-8 sm:w-16 h-0.5 mx-3 sm:mx-6 transition-colors duration-300 rounded-full flex-shrink-0',
              isStepCompleted(step.view) ? 'bg-green-500' : 'bg-gray-200'
            ]"></div>
          </div>
        </div>

        <!-- Vertical Progress (below lg) -->
        <div class="lg:hidden flex flex-col space-y-3 max-w-sm mx-auto px-4">
          <div v-for="(step, index) in progressSteps" :key="index" class="vertical-progress-step flex flex-col items-center">
            <div class="flex items-center w-full relative">
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium transition-all duration-300 shadow-soft flex-shrink-0 relative z-10',
                currentView === step.view 
                  ? 'bg-primary-500 text-white ring-2 ring-primary-100 shadow-md' :
                isStepCompleted(step.view) 
                  ? 'bg-green-500 text-white shadow-md' :
                'bg-gray-200 text-gray-500'
              ]">
                <svg v-if="isStepCompleted(step.view)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span v-else class="font-semibold">{{ index + 1 }}</span>
              </div>
              <div class="ml-4 flex-1 min-w-0">
                <span :class="[
                  'text-sm font-semibold transition-colors duration-300 block',
                  currentView === step.view ? 'text-primary-600' :
                  isStepCompleted(step.view) ? 'text-green-600' :
                  'text-gray-500'
                ]">{{ step.label }}</span>
                <div v-if="currentView === step.view" class="text-xs text-primary-500 mt-1 font-medium animate-pulse">
                  ● Active
                </div>
                <div v-else-if="isStepCompleted(step.view)" class="text-xs text-green-500 mt-1 font-medium">
                  ✓ Complete
                </div>
              </div>
            </div>
            <!-- Vertical connector line -->
            <div v-if="index < progressSteps.length - 1" class="relative flex justify-start w-full ml-4 mt-2">
              <div :class="[
                'w-0.5 h-8 vertical-progress-connector rounded-full ml-4',
                isStepCompleted(step.view) ? 'bg-green-500' : 'bg-gray-200'
              ]"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upload Step -->
      <div v-if="currentView === 'upload'" class="card animate-slide-up">
        <div class="card-header">
          <div class="flex items-start sm:items-center space-x-3">
            <div class="w-8 h-8 sm:w-10 sm:h-10 bg-primary-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h2 class="text-lg sm:text-xl font-semibold text-gray-900">Upload Your Resume</h2>
              <p class="text-sm text-gray-600 mt-1">Upload your resume and get AI-powered analysis with job recommendations</p>
            </div>
          </div>
        </div>
        
        <div class="card-body space-y-4 sm:space-y-6">
          <!-- File Upload Area -->
          <div class="relative">
            <input
              ref="fileInput"
              type="file"
              @change="handleFileUpload"
              accept=".pdf,.doc,.docx"
              class="absolute inset-0 w-full h-full opacity-0 cursor-pointer focus-ring"
            />
            <div :class="[
              'upload-area',
              selectedFile ? 'has-file' : 'default'
            ]">
              <svg class="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-3 sm:mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <div v-if="!selectedFile">
                <p class="text-lg sm:text-xl font-medium text-gray-700 mb-2">Drop your resume here</p>
                <p class="text-gray-500 mb-3 sm:mb-4">or click to browse files</p>
                <p class="text-xs sm:text-sm text-gray-400">Supports PDF, DOC, DOCX (max 10MB)</p>
              </div>
              <div v-else class="space-y-2 sm:space-y-3">
                <div class="flex items-center justify-center space-x-2">
                  <svg class="w-5 h-5 sm:w-6 sm:h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <span class="font-medium text-green-700 text-base sm:text-lg break-all">{{ selectedFile.name }}</span>
                </div>
                <p class="text-gray-500 text-sm">{{ formatFileSize(selectedFile.size) }}</p>
                <button
                  @click="clearFile"
                  class="text-red-600 hover:text-red-700 transition-colors font-medium focus-ring rounded px-2 py-1 text-sm"
                >
                  Remove file
                </button>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="parseError" class="p-3 sm:p-4 bg-red-50 border border-red-200 rounded-xl animate-slide-up">
            <div class="flex items-start space-x-2">
              <svg class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <p class="text-sm font-medium text-red-700 flex-1">{{ parseError }}</p>
            </div>
          </div>

          <!-- Process Button -->
          <button
            @click="processResume"
            :disabled="!selectedFile || isLoadingParse"
            :class="[
              'w-full py-3 sm:py-4 px-4 sm:px-6 rounded-xl font-semibold text-base sm:text-lg transition-all duration-300 flex items-center justify-center focus-ring min-h-[3rem] sm:min-h-[3.5rem]',
              selectedFile && !isLoadingParse
                ? 'btn-primary'
                : 'bg-gray-200 text-gray-500 cursor-not-allowed'
            ]"
          >
            <svg v-if="isLoadingParse" class="animate-spin w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isLoadingParse ? 'Processing Resume...' : 'Process Resume' }}</span>
          </button>
        </div>
      </div>

      <!-- Confirmation Step -->
      <div v-if="currentView === 'confirmation'" class="card animate-slide-up">
        <div class="card-header">
          <div class="flex items-start sm:items-center space-x-3">
            <div class="w-8 h-8 sm:w-10 sm:h-10 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h2 class="text-lg sm:text-xl font-semibold text-gray-900">Resume Processed Successfully</h2>
              <p class="text-sm text-gray-600 mt-1">Review extracted information and proceed with analysis</p>
            </div>
          </div>
        </div>
        
        <div class="card-body space-y-6 sm:space-y-8">


          <!-- Key Information Preview -->
          <div class="space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h3 class="text-base sm:text-lg font-semibold text-gray-900">Resume Preview</h3>
              <p class="text-xs sm:text-sm text-gray-500">Review and edit your information as needed</p>
            </div>
            
            <div v-if="hasStructuredData">
              <!-- Debug info for structured display -->
              <StructuredResumeDisplay 
                :resume-data="(parsedData?.parsed_data || parsedData) as any" 
                v-model="editableData"
                @update:modelValue="handleStructuredDataUpdate"
              />
            </div>
            
            <!-- Fallback to old flat display -->
            <div v-else class="grid gap-3 sm:gap-4">
              <div class="text-sm text-gray-600 mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <strong>Debug Info:</strong> Showing flat display because structured data not detected.<br>
                <strong>Data keys:</strong> {{ parsedData ? Object.keys(parsedData).join(', ') : 'No data' }}<br>
                <strong>Has structured data:</strong> {{ hasStructuredData }}
              </div>
              <div v-for="(content, section) in safePreviewSections" :key="section" class="section-preview">
                <div class="section-header">
                  <div class="flex items-center justify-between">
                    <h4 class="font-medium text-gray-900 capitalize text-sm sm:text-base">{{ formatSectionName(String(section)) }}</h4>
                    <div class="flex items-center space-x-2">
                      <button
                        v-if="!isEditing[String(section)]"
                        @click="toggleEdit(String(section))"
                        class="edit-button p-2 text-gray-500 hover:text-blue-600 transition-colors rounded-lg hover:bg-blue-50 border border-transparent hover:border-blue-200"
                        :title="`Edit ${formatSectionName(String(section))}`"
                      >
                        <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>
                      <div v-else class="flex items-center space-x-1">
                        <button
                          @click="saveEdit(String(section))"
                          class="p-2 text-green-600 hover:text-green-700 transition-colors rounded-lg hover:bg-green-50 border border-green-200"
                          title="Save changes"
                        >
                          <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"/>
                          </svg>
                        </button>
                        <button
                          @click="cancelEdit(String(section))"
                          class="p-2 text-red-600 hover:text-red-700 transition-colors rounded-lg hover:bg-red-50 border border-red-200"
                          title="Cancel changes"
                        >
                          <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="section-content">
                  <div v-if="!isEditing[String(section)]">
                    <p class="text-xs sm:text-sm text-gray-700 line-clamp-3">{{ safeSubstring(getDisplayData(String(section)), 150) }}</p>
                  </div>
                  <div v-else>
                    <!-- Special handling for contact information -->
                    <div v-if="section === 'contact_information' || section === 'contact_info'" class="space-y-3">
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                          <label class="block text-xs font-medium text-gray-700 mb-1">Name</label>
                          <input 
                            v-model="contactEditFields.name"
                            type="text" 
                            class="w-full p-2 border border-gray-300 rounded-lg text-xs focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            placeholder="Enter your full name"
                          />
                        </div>
                        <div>
                          <label class="block text-xs font-medium text-gray-700 mb-1">Email</label>
                          <input 
                            v-model="contactEditFields.email"
                            type="email" 
                            class="w-full p-2 border border-gray-300 rounded-lg text-xs focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            placeholder="Enter your email address"
                          />
                        </div>
                        <div>
                          <label class="block text-xs font-medium text-gray-700 mb-1">Phone</label>
                          <input 
                            v-model="contactEditFields.phone"
                            type="tel" 
                            class="w-full p-2 border border-gray-300 rounded-lg text-xs focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            placeholder="Enter your phone number"
                          />
                        </div>
                        <div>
                          <label class="block text-xs font-medium text-gray-700 mb-1">Location</label>
                          <input 
                            v-model="contactEditFields.location"
                            type="text" 
                            class="w-full p-2 border border-gray-300 rounded-lg text-xs focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            placeholder="Enter your location"
                          />
                        </div>
                      </div>
                      <div class="mt-2 text-xs text-gray-500">
                        Press <kbd>Cmd/Ctrl + Enter</kbd> to save, <kbd>Esc</kbd> to cancel
                      </div>
                    </div>
                    <!-- Default textarea for other sections -->
                    <div v-else>
                      <textarea
                        v-model="editableData[String(section)]"
                        class="editable-textarea w-full p-2 sm:p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-xs sm:text-sm"
                        rows="4"
                        :placeholder="`Enter ${formatSectionName(String(section)).toLowerCase()}...`"
                        @keydown.meta.enter="saveEdit(String(section))"
                        @keydown.ctrl.enter="saveEdit(String(section))"
                        @keydown.esc="cancelEdit(String(section))"
                      ></textarea>
                      <div class="mt-2 text-xs text-gray-500">
                        Press <kbd>Cmd/Ctrl + Enter</kbd> to save, <kbd>Esc</kbd> to cancel
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col gap-3 sm:flex-row sm:gap-4 pt-4">
            <button
              @click="proceedToAnalysis"
              :disabled="isLoadingAnalyze"
              class="flex-1 btn-primary focus-ring flex items-center justify-center text-sm sm:text-base py-3 sm:py-4"
            >
              <svg v-if="isLoadingAnalyze" class="animate-spin w-4 h-4 sm:w-5 sm:h-5 mr-3" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ isLoadingAnalyze ? 'Analyzing...' : 'Proceed with Analysis' }}</span>
            </button>
            <button
              @click="goBackToUpload"
              class="flex-1 btn-secondary focus-ring flex items-center justify-center text-sm sm:text-base py-3 sm:py-4"
            >
              <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
              </svg>
              <span>Upload Different Resume</span>
            </button>
          </div>

          <!-- Error Message -->
          <div v-if="analyzeError" class="p-3 sm:p-4 bg-red-50 border border-red-200 rounded-xl animate-slide-up">
            <div class="flex items-start space-x-2">
              <svg class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <p class="text-sm font-medium text-red-700 flex-1">{{ analyzeError }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Step -->
      <div v-if="currentView === 'results'" class="space-y-6 sm:space-y-8 animate-slide-up">


        <!-- Summary Recommendations (from original uploaded resume) -->
        <div v-if="originalParsedData?.summary_recommendations?.length" class="card">
          <div class="card-header">
            <div class="flex items-center justify-between">
              <div class="flex items-start sm:items-center space-x-3">
                <div class="w-8 h-8 sm:w-10 sm:h-10 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-5 h-5 sm:w-6 sm:h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <h2 class="text-lg sm:text-xl font-semibold text-gray-900">Resume Improvement Recommendations</h2>
                  <p class="text-sm text-gray-600 mt-1">Based on your original uploaded resume content</p>
                </div>
              </div>
              <button 
                @click="isSummaryRecsExpanded = !isSummaryRecsExpanded"
                class="p-2 rounded-lg hover:bg-gray-100 transition-colors focus-ring flex-shrink-0"
                :title="isSummaryRecsExpanded ? 'Collapse section' : 'Expand section'"
              >
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-gray-500 transition-transform duration-200" :class="{ 'rotate-180': !isSummaryRecsExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </div>
          </div>
          
          <Transition name="slide-down" mode="out-in">
            <div v-show="isSummaryRecsExpanded" class="card-body">
              <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6">
                <div class="flex items-start space-x-3">
                  <svg class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-amber-800 mb-1">About these recommendations</p>
                    <p class="text-xs text-amber-700">These recommendations are based on your original uploaded resume, not the edited data in the review stage. They help identify areas for improvement in your resume content and structure.</p>
                  </div>
                </div>
              </div>
              
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <div class="flex items-center space-x-2 mb-4">
                  <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                  <h3 class="text-lg font-semibold text-gray-900">Improvement Suggestions</h3>
                </div>
                <div class="space-y-3">
                  <div v-for="(recommendation, index) in originalParsedData.summary_recommendations" :key="index" class="flex items-start space-x-3">
                    <div class="w-6 h-6 bg-amber-600 text-white rounded-full flex items-center justify-center text-xs font-bold mt-0.5 flex-shrink-0">
                      {{ index + 1 }}
                    </div>
                    <p class="text-sm text-gray-700 leading-relaxed flex-1">{{ recommendation }}</p>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Job Recommendations -->
        <div v-if="jobMatches?.length" class="card">
          <div class="card-header">
            <div class="flex items-center justify-between">
              <div class="flex items-start sm:items-center space-x-3">
                <div class="w-8 h-8 sm:w-10 sm:h-10 bg-indigo-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-5 h-5 sm:w-6 sm:h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2h8z"/>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <h2 class="text-lg sm:text-xl font-semibold text-gray-900">Job Recommendations</h2>
                  <p class="text-sm text-gray-600 mt-1">Jobs that match your profile and experience level</p>
                </div>
              </div>
              <button 
                @click="isJobRecsExpanded = !isJobRecsExpanded"
                class="p-2 rounded-lg hover:bg-gray-100 transition-colors focus-ring flex-shrink-0"
                :title="isJobRecsExpanded ? 'Collapse section' : 'Expand section'"
              >
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-gray-500 transition-transform duration-200" :class="{ 'rotate-180': !isJobRecsExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </div>
          </div>
          
          <Transition name="slide-down" mode="out-in">
            <div v-show="isJobRecsExpanded" class="card-body">
              <div class="space-y-4">
                <div v-for="job in jobMatches" :key="job.job_id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div class="flex justify-between items-start mb-3">
                    <div class="flex-1">
                      <div class="flex items-center space-x-2 mb-1">
                        <h3 class="text-lg font-semibold text-gray-900">{{ job.job_title }}</h3>
                        <span class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-mono">ID: {{ job.job_id }}</span>
                      </div>
                      <p class="text-sm text-gray-600">{{ job.company }} • {{ job.location }}</p>
                    </div>
                    <div class="flex items-center space-x-2 ml-4">
                      <div class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                        {{ Math.round(job.score * 100) }}% match
                      </div>
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <p class="text-sm text-gray-700 leading-relaxed" 
                       :class="{ 'line-clamp-2': !expandedDescriptions[job.job_id] }">
                      {{ job.job_description }}
                    </p>
                    <button 
                      v-if="job.job_description && job.job_description.length > 150"
                      @click="toggleDescription(job.job_id)"
                      class="text-sm text-indigo-600 hover:text-indigo-800 font-medium mt-1 transition-colors"
                    >
                      {{ expandedDescriptions[job.job_id] ? 'Show Less' : 'Show More' }}
                    </button>
                  </div>
                  
                  <div class="flex flex-wrap gap-2 mb-3">
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {{ job.category }}
                    </span>
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                      {{ job.type }}
                    </span>
                    <span v-if="job.salary" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {{ job.salary }}
                    </span>
                  </div>
                  
                  <div class="flex justify-between items-center mb-3">
                    <div class="text-xs text-gray-500">
                      <span>{{ job.subcategory }} • {{ job.role }}</span>
                      <br>
                      <span>Listed: {{ new Date(job.listingDate).toLocaleDateString() }}</span>
                    </div>
                    <div class="flex space-x-2">
                      <NuxtLink 
                        :to="`/company/${job.company.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '')}`"
                        class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        View Company
                      </NuxtLink>
                      <NuxtLink 
                        :to="`/apply/${job.job_id}`"
                        class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center space-x-2 transition-colors"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                        </svg>
                        <span>Apply Now</span>
                      </NuxtLink>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Company Recommendations (fallback for backward compatibility) -->
        <div v-else-if="companyRecommendations?.length" class="card">
          <div class="card-header">
            <div class="flex items-center justify-between">
              <div class="flex items-start sm:items-center space-x-3">
                <div class="w-8 h-8 sm:w-10 sm:h-10 bg-indigo-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-5 h-5 sm:w-6 sm:h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2m-2 0H7m14 0v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5"/>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <h2 class="text-lg sm:text-xl font-semibold text-gray-900">Company Recommendations</h2>
                  <p class="text-sm text-gray-600 mt-1">Companies that match your profile and experience level</p>
                </div>
              </div>
              <button 
                @click="isCompanyRecsExpanded = !isCompanyRecsExpanded"
                class="p-2 rounded-lg hover:bg-gray-100 transition-colors focus-ring flex-shrink-0"
                :title="isCompanyRecsExpanded ? 'Collapse section' : 'Expand section'"
              >
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-gray-500 transition-transform duration-200" :class="{ 'rotate-180': !isCompanyRecsExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </div>
          </div>
          
          <Transition name="slide-down" mode="out-in">
            <div v-show="isCompanyRecsExpanded" class="card-body">
              <div class="grid gap-4 sm:gap-6 md:grid-cols-2 xl:grid-cols-3">
                <CompanyCard 
                  v-for="company in companyRecommendations" 
                  :key="company.id" 
                  :company="company"
                  class="h-full"
                />
              </div>
            </div>
          </Transition>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col gap-3 sm:flex-row sm:gap-4 pt-4">
          <button
            @click="downloadReport"
            class="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-3 sm:py-4 px-4 sm:px-6 rounded-xl font-semibold transition-all duration-300 flex items-center justify-center shadow-soft hover:shadow-medium transform hover:-translate-y-0.5 focus-ring min-h-[3rem] sm:min-h-[3.5rem] text-sm sm:text-base"
          >
            <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <span>Download Full Report</span>
          </button>
          <button
            @click="startOver"
            class="flex-1 btn-secondary focus-ring flex items-center justify-center text-sm sm:text-base py-3 sm:py-4"
          >
            <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <span>Analyze Another Resume</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, reactive } from 'vue';
import StructuredResumeDisplay from '~/components/StructuredResumeDisplay.vue';
import AppNavigation from '~/components/AppNavigation.vue';

// SEO and Meta
useHead({
  title: 'Smart Resume Analyzer - AI-Powered Resume Analysis & Job Matching',
  meta: [
    { name: 'description', content: 'Analyze and optimize your resume with AI-powered insights and get personalized company recommendations.' }
  ]
});

const config = useRuntimeConfig();
const apiBaseUrl = computed(() => {
  const url = config.public.apiBaseUrl;
  return url === 'undefined' || !url ? 'http://localhost:8000' : url;
});

// Reactive state
const currentView = ref<'upload' | 'confirmation' | 'results'>('upload');
const selectedFile = ref<File | null>(null);
const parsedData = ref<Record<string, any> | null>(null);
const analysisResult = ref<any | null>(null);
const originalParsedData = ref<any | null>(null);
const jobMatches = ref<any[]>([]);

const isLoadingParse = ref(false);
const isLoadingAnalyze = ref(false);

const parseError = ref<string | null>(null);
const analyzeError = ref<string | null>(null);

const backendStatus = ref<string>('checking...');

// Collapsible section states
const isAnalysisExpanded = ref(true);
const isCompanyRecsExpanded = ref(true);
const isSummaryRecsExpanded = ref(true);
const isJobRecsExpanded = ref(true);

// Job description expansion states
const expandedDescriptions = ref<Record<string, boolean>>({});

// Session storage keys
const SESSION_KEYS = {
  currentView: 'resume_analyzer_current_view',
  parsedData: 'resume_analyzer_parsed_data',
  analysisResult: 'resume_analyzer_analysis_result',
  originalParsedData: 'resume_analyzer_original_parsed_data',
  jobMatches: 'resume_analyzer_job_matches',
  editableData: 'resume_analyzer_editable_data',
  fileName: 'resume_analyzer_file_name'
};

// Safe computed property for preview sections
const safePreviewSections = computed(() => {
  try {
    return getPreviewSections();
  } catch (error) {
    console.error('Error getting preview sections:', error);
    parseError.value = 'Error displaying resume data. Please try uploading again.';
    return {};
  }
});

// Computed property to detect structured data
const hasStructuredData = computed(() => {
  if (!parsedData.value) return false;
  
  // The data might be nested under parsed_data key if we stored the whole response
  const actualData = parsedData.value.parsed_data || parsedData.value;
  
  console.log('🔍 Full parsedData.value:', parsedData.value);
  console.log('🔍 Actual data to check:', actualData);
  console.log('🔍 Checking structured data:', {
    hasContactInfo: !!actualData.contact_info,
    hasSummary: !!actualData.summary,
    summaryType: typeof actualData.summary,
    actualDataKeys: Object.keys(actualData)
  });
  
  // Check for new structured format in the actual data
  const isStructured = actualData.contact_info || 
    (actualData.summary && typeof actualData.summary === 'object');
  
  console.log('🔍 Is structured:', isStructured);
  return isStructured;
});

// Editing states for review section
const isEditing = ref<Record<string, boolean>>({});
const editableData = ref<Record<string, string>>({});
const contactEditFields = reactive({
  name: '',
  email: '',
  phone: '',
  location: ''
});

// Progress steps configuration
const progressSteps = [
  { view: 'upload', label: 'Upload Resume' },
  { view: 'confirmation', label: 'Review & Confirm' },
  { view: 'results', label: 'Results & Recommendations' }
];

// File input ref
const fileInput = ref<HTMLInputElement | null>(null);

// Company recommendations data
const companyRecommendations = ref([]);
const isLoadingCompanyRecommendations = ref(false);

// Function to fetch personalized company recommendations
async function fetchCompanyRecommendations() {
  if (!parsedData.value) {
    companyRecommendations.value = [];
    return;
  }
  
  isLoadingCompanyRecommendations.value = true;
  
  try {
    // Generate recommendations based on parsed data
    const skills = extractSkills(parsedData.value.skills || {});
    const experienceYears = extractExperienceYears(parsedData.value.experience || {});
    
    // Fetch companies from API
    const API_BASE_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000'
    const response = await fetch(`${API_BASE_URL}/companies?limit=6&page=1`)
    
    if (response.ok) {
      const data = await response.json()
      // Handle both old format (array) and new format (object with pagination)
      const companies = Array.isArray(data) ? data : (data.companies || [])
      
      // Filter based on user skills if available
      if (skills.length > 0) {
        companyRecommendations.value = companies.filter(company => {
          const hasRelevantIndustry = skills.some(skill => 
            company.industry.toLowerCase().includes(skill.toLowerCase()) ||
            company.description.toLowerCase().includes(skill.toLowerCase())
          );
          return hasRelevantIndustry || company.match > 75;
        }).slice(0, 6);
      } else {
        companyRecommendations.value = companies.slice(0, 6);
      }
    } else {
      throw new Error('Failed to fetch companies');
    }
  } catch (error) {
    console.error('Error fetching companies:', error)
    
    // Fallback data if API fails
    companyRecommendations.value = [
      {
        id: 1,
        name: 'TechCorp Solutions',
        industry: 'Technology',
        size: 'Mid-size (100-500)',
        match: 92,
        description: 'Leading software development company specializing in enterprise solutions.'
      }
    ];
  } finally {
    isLoadingCompanyRecommendations.value = false;
  }
}

// Session storage functions
function saveToSession() {
  if (process.client) {
    try {
      sessionStorage.setItem(SESSION_KEYS.currentView, currentView.value);
      if (parsedData.value) {
        sessionStorage.setItem(SESSION_KEYS.parsedData, JSON.stringify(parsedData.value));
      }
      if (analysisResult.value) {
        sessionStorage.setItem(SESSION_KEYS.analysisResult, JSON.stringify(analysisResult.value));
      }
      if (originalParsedData.value) {
        sessionStorage.setItem(SESSION_KEYS.originalParsedData, JSON.stringify(originalParsedData.value));
      }
      if (jobMatches.value?.length) {
        sessionStorage.setItem(SESSION_KEYS.jobMatches, JSON.stringify(jobMatches.value));
      }
      if (editableData.value) {
        sessionStorage.setItem(SESSION_KEYS.editableData, JSON.stringify(editableData.value));
      }
      if (selectedFile.value) {
        sessionStorage.setItem(SESSION_KEYS.fileName, selectedFile.value.name);
      }
    } catch (error) {
      console.warn('Failed to save to session storage:', error);
    }
  }
}

function loadFromSession() {
  if (process.client) {
    try {
      const savedView = sessionStorage.getItem(SESSION_KEYS.currentView);
      const savedParsedData = sessionStorage.getItem(SESSION_KEYS.parsedData);
      const savedAnalysisResult = sessionStorage.getItem(SESSION_KEYS.analysisResult);
      const savedOriginalParsedData = sessionStorage.getItem(SESSION_KEYS.originalParsedData);
      const savedJobMatches = sessionStorage.getItem(SESSION_KEYS.jobMatches);
      const savedEditableData = sessionStorage.getItem(SESSION_KEYS.editableData);
      const savedFileName = sessionStorage.getItem(SESSION_KEYS.fileName);

      if (savedView) currentView.value = savedView as 'upload' | 'confirmation' | 'results';
      if (savedParsedData) parsedData.value = JSON.parse(savedParsedData);
      if (savedAnalysisResult) analysisResult.value = JSON.parse(savedAnalysisResult);
      if (savedOriginalParsedData) originalParsedData.value = JSON.parse(savedOriginalParsedData);
      if (savedJobMatches) jobMatches.value = JSON.parse(savedJobMatches);
      if (savedEditableData) editableData.value = JSON.parse(savedEditableData);
      
      // Create a mock file object if we have a saved filename
      if (savedFileName && !selectedFile.value) {
        // We can't recreate the actual file, but we can show the name
        // This is mainly for display purposes
      }
    } catch (error) {
      console.warn('Failed to load from session storage:', error);
    }
  }
}

function clearSession() {
  if (process.client) {
    Object.values(SESSION_KEYS).forEach(key => {
      sessionStorage.removeItem(key);
    });
  }
}

// Methods
function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      parseError.value = "File size must be less than 10MB.";
      return;
    }
    
    selectedFile.value = file;
    parseError.value = null;
  }
}

function clearFile() {
  selectedFile.value = null;
  parsedData.value = null;
  analysisResult.value = null;
  originalParsedData.value = null;
  jobMatches.value = [];
  parseError.value = null;
  analyzeError.value = null;
  currentView.value = 'upload';
  
  // Reset expanded states
  isAnalysisExpanded.value = true;
  isCompanyRecsExpanded.value = true;
  isSummaryRecsExpanded.value = true;
  isJobRecsExpanded.value = true;
  
  if (fileInput.value) {
    fileInput.value.value = '';
  }
  
  // Clear session storage
  clearSession();
}

// Toggle job description expansion
function toggleDescription(jobId: string) {
  expandedDescriptions.value[jobId] = !expandedDescriptions.value[jobId];
}

async function processResume() {
  if (!selectedFile.value) {
    parseError.value = "Please select a file.";
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  isLoadingParse.value = true;
  parseError.value = null;

  try {
    const response = await $fetch<{ filename: string; parsed_data: Record<string, any> }>(
      `${apiBaseUrl.value}/parse_resume`,
      {
        method: 'POST',
        body: formData,
      }
    );
    
    if (response.parsed_data) {
      console.log('📋 Parsed data structure:', response.parsed_data);
      console.log('📋 Data keys:', Object.keys(response.parsed_data));
      
      parsedData.value = response.parsed_data;
      
      // Initialize editable data (exclude summary_recommendations and full_text from editable fields)
      editableData.value = { ...response.parsed_data };
      delete editableData.value.full_text; // Remove full_text from editable fields
      delete editableData.value.summary_recommendations; // Remove summary_recommendations from editable fields
      
      // Reset editing states
      isEditing.value = {};
      
      // Clear any previous errors
      parseError.value = null;
      
      // Fetch company recommendations
      await fetchCompanyRecommendations();
      
      currentView.value = 'confirmation';
      scrollToTop(); // Scroll to top for better UX
    } else {
      throw new Error("Parsed data is empty or not in expected format.");
    }
  } catch (e: any) {
    console.error("Error parsing resume:", e);
    parseError.value = e.data?.detail || e.message || "Failed to parse resume. Please ensure the backend is running and the file is valid.";
    // Reset to upload view on error
    currentView.value = 'upload';
  } finally {
    isLoadingParse.value = false;
  }
}

async function proceedToAnalysis() {
  console.log('🚀 proceedToAnalysis called');
  if (!parsedData.value) {
    analyzeError.value = "Please parse a resume first.";
    return;
  }

  isLoadingAnalyze.value = true;
  analyzeError.value = null;

  try {
    // Use edited data for analysis
    const payload = { ...parsedData.value, ...editableData.value };
    console.log('📤 Sending payload:', payload);

    const response = await $fetch<{ analysis: any; original_parsed_data: any }>(
      `${apiBaseUrl.value}/analyze_resume`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: payload, 
      }
    );
    console.log('📥 Received response:', response);
    
    // Handle the new response structure
    analysisResult.value = response.analysis;
    originalParsedData.value = response.original_parsed_data;
    
    // Extract job matches from analysis
    if (response.analysis?.job_matches) {
      jobMatches.value = response.analysis.job_matches;
    }
    
    console.log('✅ Analysis result set:', analysisResult.value);
    console.log('✅ Original parsed data set:', originalParsedData.value);
    console.log('✅ Job matches set:', jobMatches.value);
    
    currentView.value = 'results';
    console.log('🎯 Current view set to:', currentView.value);
    scrollToTop(); // Scroll to top for better UX
  } catch (e: any) {
    console.error("❌ Error analyzing resume:", e);
    analyzeError.value = e.message || "Failed to analyze resume.";
  } finally {
    isLoadingAnalyze.value = false;
  }
}

function goBackToUpload() {
  currentView.value = 'upload';
  scrollToTop()
  clearFile();
}

function isStepCompleted(step: string): boolean {
  const stepOrder = ['upload', 'confirmation', 'results'];
  const currentIndex = stepOrder.indexOf(currentView.value);
  const stepIndex = stepOrder.indexOf(step);
  return currentIndex > stepIndex;
}



function formatSectionName(section: string): string {
  return section.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  return 'text-red-600';
}

function getScoreBarColor(score: number): string {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  return 'bg-red-500';
}

function getScoreBadgeColor(score: number): string {
  if (score >= 80) return 'bg-green-100 text-green-800';
  if (score >= 60) return 'bg-yellow-100 text-yellow-800';
  return 'bg-red-100 text-red-800';
}

function getScoreLabel(score: number): string {
  if (score >= 80) return 'Excellent';
  if (score >= 60) return 'Good';
  return 'Needs Improvement';
}

function getScoreBadgeStyles(score: number): string {
  if (score >= 80) return 'background: #dcfce7; color: #166534;';
  if (score >= 60) return 'background: #fef3c7; color: #92400e;';
  return 'background: #fee2e2; color: #991b1b;';
}

function downloadReport() {
  if (!analysisResult.value || !parsedData.value) return;
  
  const currentDate = new Date().toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  
  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Analysis Report - ${selectedFile.value?.name || 'Resume'}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            line-height: 1.6; 
            color: #1f2937; 
            background: #f9fafb;
            padding: 1rem;
        }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        .header { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: white; padding: 3rem 2rem; text-align: center; }
        .header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
        .header p { opacity: 0.9; font-size: 1.2rem; margin-bottom: 1rem; }
        .meta { opacity: 0.8; font-size: 1rem; }
        .content { padding: 2.5rem; }
        .section { margin-bottom: 3rem; }
        .section-title { font-size: 1.75rem; font-weight: 700; color: #1f2937; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem; }
        .divider { height: 3px; background: linear-gradient(to right, #6366f1, #8b5cf6); border-radius: 2px; margin: 2rem 0; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; }
        .card { border: 1px solid #e5e7eb; border-radius: 16px; padding: 2rem; background: white; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
        .card.highlight { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-color: #0284c7; }
        .card.success { background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-color: #16a34a; }
        .card.warning { background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-color: #d97706; }
        .score-display { text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 12px; margin-bottom: 2rem; }
        .score-number { font-size: 4rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; }
        .score-label { font-size: 1.1rem; font-weight: 600; padding: 0.75rem 1.5rem; border-radius: 50px; background: #6366f1; color: white; display: inline-block; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .stat-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; }
        .stat-number { font-size: 2rem; font-weight: 700; color: #1e293b; margin-bottom: 0.5rem; }
        .stat-label { color: #64748b; font-weight: 500; }
        .recommendation-list { display: flex; flex-direction: column; gap: 1.5rem; }
        .recommendation-item { display: flex; gap: 1rem; padding: 1.5rem; background: #f8fafc; border-radius: 12px; border-left: 4px solid #10b981; }
        .rec-number { width: 2rem; height: 2rem; background: #10b981; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0; }
        .job-card { border: 1px solid #e5e7eb; border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem; background: white; }
        .job-header { display: flex; justify-content: between; align-items: start; margin-bottom: 1.5rem; }
        .job-title { font-size: 1.25rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem; }
        .job-company { color: #6b7280; font-weight: 500; }
        .job-match { background: #dcfce7; color: #166534; padding: 0.5rem 1rem; border-radius: 50px; font-weight: 600; }
        .job-tags { display: flex; gap: 0.75rem; flex-wrap: wrap; margin: 1rem 0; }
        .tag { padding: 0.5rem 1rem; border-radius: 50px; font-size: 0.875rem; font-weight: 500; }
        .tag.blue { background: #dbeafe; color: #1e40af; }
        .tag.green { background: #dcfce7; color: #166534; }
        .tag.purple { background: #e9d5ff; color: #7c3aed; }
        .contact-info { background: #f8fafc; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
        .info-row { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0; }
        .info-row:last-child { border-bottom: none; }
        .info-label { font-weight: 600; color: #374151; }
        .info-value { color: #6b7280; }
        .key-highlights { background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 20%, #f59e0b 100%); border-radius: 16px; padding: 2rem; margin-bottom: 2rem; }
        .highlight-title { font-size: 1.5rem; font-weight: 700; color: #92400e; margin-bottom: 1rem; }
        .highlight-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
        .highlight-item { background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 8px; }
        .footer { text-align: center; color: #6b7280; font-size: 0.875rem; padding: 2rem; border-top: 1px solid #e5e7eb; background: #f9fafb; }
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; }
            .no-print { display: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Professional Resume Analysis Report</h1>
            <p>AI-Powered Career Intelligence & Recommendations</p>
            <div class="meta">
                📄 ${selectedFile.value?.name || 'Resume'} • 📅 Generated on ${currentDate}
            </div>
        </div>
        
        <div class="content">
            <!-- Contact Information -->
            ${parsedData.value?.contact_info || parsedData.value?.contact_information ? `
            <div class="section">
                <h2 class="section-title">👤 Contact Information</h2>
                <div class="contact-info">
                    ${Object.entries(parsedData.value?.contact_info || parsedData.value?.contact_information || {}).map(([key, value]) => 
                        value ? `<div class="info-row">
                            <span class="info-label">${key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ')}</span>
                            <span class="info-value">${value}</span>
                        </div>` : ''
                    ).join('')}
                </div>
            </div>
            ` : ''}

            <!-- Resume Improvement Recommendations -->
            ${originalParsedData.value?.summary_recommendations?.length ? `
            <div class="section">
                <h2 class="section-title">💡 Resume Improvement Recommendations</h2>
                <p style="color: #6b7280; margin-bottom: 1.5rem; font-size: 1rem; line-height: 1.6;">Based on your original uploaded resume content</p>
                
                <div style="background: #fff7ed; border: 1px solid #fed7aa; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                        <span style="color: #92400e;">📄</span>
                        <p style="color: #92400e; font-weight: 600; margin: 0; font-size: 0.875rem;">About these recommendations</p>
                    </div>
                    <p style="color: #92400e; font-size: 0.75rem; margin: 0; line-height: 1.5;">These recommendations are based on your original uploaded resume, not the edited data in the review stage. They help identify areas for improvement in your resume content and structure.</p>
                </div>
                
                <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 2rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem;">
                        <span style="color: #f59e0b; font-size: 1.25rem;">💡</span>
                        <h3 style="color: #1f2937; font-size: 1.125rem; font-weight: 600; margin: 0;">Improvement Suggestions</h3>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        ${originalParsedData.value.summary_recommendations.map((recommendation: string, index: number) =>
                            `<div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                                <div style="width: 1.5rem; height: 1.5rem; background: #f59e0b; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; margin-top: 0.125rem;">${index + 1}</div>
                                <p style="color: #374151; line-height: 1.6; margin: 0; flex: 1;">${recommendation}</p>
                            </div>`
                        ).join('')}
                    </div>
                </div>
            </div>
            ` : ''}

            <div class="divider"></div>

            <!-- Job Recommendations -->
            ${jobMatches.value?.length ? `
            <div class="section">
                <h2 class="section-title">🎯 Job Recommendations</h2>
                <p style="margin-bottom: 2rem; color: #6b7280; font-size: 1.1rem;">Based on your profile, here are positions that align with your experience and skills:</p>
                ${jobMatches.value.slice(0, 6).map(job => 
                    `<div class="job-card">
                        <div class="job-header">
                            <div style="flex: 1;">
                                <div class="job-title">${job.job_title}</div>
                                <div class="job-company">${job.company} • ${job.location}</div>
                            </div>
                            <div class="job-match">${Math.round(job.score * 100)}% match</div>
                        </div>
                        <p style="color: #4b5563; margin-bottom: 1rem; line-height: 1.6;">${job.job_description}</p>
                        <div class="job-tags">
                            <span class="tag blue">${job.category}</span>
                            <span class="tag purple">${job.type}</span>
                            ${job.salary ? `<span class="tag green">${job.salary}</span>` : ''}
                        </div>
                    </div>`
                ).join('')}
            </div>
            ` : companyRecommendations.value?.length ? `
            <div class="section">
                <h2 class="section-title">🏢 Company Recommendations</h2>
                <div class="grid">
                    ${companyRecommendations.value.slice(0, 6).map(company => 
                        `<div class="card highlight">
                            <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem;">${company.name}</h3>
                            <p style="color: #6b7280; margin-bottom: 1rem;">${company.industry}</p>
                            <div style="margin-bottom: 1rem;">
                                <span class="tag blue">${company.size}</span>
                                <span class="tag green">${company.match}% match</span>
                            </div>
                            <p style="color: #4b5563; font-size: 0.9rem; margin-bottom: 1rem;">${company.description}</p>
                                                          <div style="border-top: 1px solid #e5e7eb; padding-top: 1rem;">
                                  <strong style="color: #374151;">Company Details:</strong>
                                  <p style="color: #6b7280; font-size: 0.875rem;">${company.industry} • ${company.size}</p>
                              </div>
                        </div>`
                    ).join('')}
                </div>
            </div>
            ` : ''}


        </div>
        
        <div class="footer">
            <p><strong>Generated by Smart Resume Analyzer</strong> • ${currentDate}</p>
            <p style="margin-top: 0.5rem;">This comprehensive report provides AI-powered insights to accelerate your career growth.</p>
            <p style="margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.8;">💡 Keep this report for reference and track your progress as you implement the recommendations.</p>
        </div>
    </div>
</body>
</html>`;

  // Create and download the HTML file
  const blob = new Blob([htmlContent], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `resume-analysis-report-${new Date().toISOString().split('T')[0]}.html`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  
  // Show a helpful message
  setTimeout(() => {
    alert('📄 Report downloaded! Open the HTML file in your browser to view or print your professional resume analysis report.');
  }, 500);
}

function startOver() {
  scrollToTop();
  clearFile();
}

// Editing functions
function toggleEdit(section: string) {
  isEditing.value[section] = !isEditing.value[section];
  
  // If starting to edit, ensure the field has the current value
  if (isEditing.value[section]) {
    if (section === 'contact_information' || section === 'contact_info') {
      // Initialize contact fields from structured data
      const contactData = parsedData.value?.[section] || parsedData.value?.contact_info || {};
      if (typeof contactData === 'object') {
        contactEditFields.name = contactData.name || '';
        contactEditFields.email = contactData.email || '';
        contactEditFields.phone = contactData.phone || '';
        contactEditFields.location = contactData.location || '';
      } else if (typeof contactData === 'string') {
        // Parse string format if it exists
        const lines = contactData.split('\n');
        contactEditFields.name = lines[0] || '';
        contactEditFields.email = lines[1] || '';
        contactEditFields.phone = lines[2] || '';
        contactEditFields.location = lines[3] || '';
      }
    } else if (!editableData.value[section]) {
      editableData.value[section] = parsedData.value?.[section] || '';
    }
  }
}

function saveEdit(section: string) {
  isEditing.value[section] = false;
  
  if (section === 'contact_information' || section === 'contact_info') {
    // Update the parsed data with individual contact fields
    if (parsedData.value) {
      if (!parsedData.value[section]) {
        parsedData.value[section] = {};
      }
      
      // Handle both structured and string formats
      if (typeof parsedData.value[section] === 'object') {
        parsedData.value[section].name = contactEditFields.name;
        parsedData.value[section].email = contactEditFields.email;
        parsedData.value[section].phone = contactEditFields.phone;
        parsedData.value[section].location = contactEditFields.location;
      } else {
        // Convert to string format for compatibility
        parsedData.value[section] = `${contactEditFields.name}\n${contactEditFields.email}\n${contactEditFields.phone}\n${contactEditFields.location}`;
      }
      
      // Also update the main contact_info if we're editing contact_information
      if (section === 'contact_information' && parsedData.value.contact_info) {
        parsedData.value.contact_info.name = contactEditFields.name;
        parsedData.value.contact_info.email = contactEditFields.email;
        parsedData.value.contact_info.phone = contactEditFields.phone;
        parsedData.value.contact_info.location = contactEditFields.location;
      }
    }
  }
  // For other sections, the reactive data is automatically updated through v-model
}

function cancelEdit(section: string) {
  isEditing.value[section] = false;
  
  if (section === 'contact_information' || section === 'contact_info') {
    // Reset contact fields to original values
    const contactData = parsedData.value?.[section] || parsedData.value?.contact_info || {};
    if (typeof contactData === 'object') {
      contactEditFields.name = contactData.name || '';
      contactEditFields.email = contactData.email || '';
      contactEditFields.phone = contactData.phone || '';
      contactEditFields.location = contactData.location || '';
    } else if (typeof contactData === 'string') {
      const lines = contactData.split('\n');
      contactEditFields.name = lines[0] || '';
      contactEditFields.email = lines[1] || '';
      contactEditFields.phone = lines[2] || '';
      contactEditFields.location = lines[3] || '';
    }
  } else {
    // Restore original value for other sections
    editableData.value[section] = parsedData.value?.[section] || '';
  }
}

function getDisplayData(section: string): string {
  const data = editableData.value[section] || parsedData.value?.[section] || '';
  
  // Handle structured data format
  if (typeof data === 'object' && data !== null) {
    if (data.summary) return data.summary;
    if (data.full_text) return data.full_text;
    // Handle contact_info object
    if (section === 'contact_info' || section === 'contact_information') {
      return `${data.name || ''}\n${data.email || ''}\n${data.phone || ''}\n${data.location || ''}`.trim();
    }
    return JSON.stringify(data);
  }
  
  return String(data || '');
}

function safeSubstring(text: string, maxLength: number): string {
  try {
    const str = String(text || '');
    if (str.length <= maxLength) return str;
    return str.substring(0, maxLength) + '...';
  } catch (e) {
    console.error('Error in safeSubstring:', e);
    return 'Error displaying text';
  }
}

// Check backend status on mount
async function checkBackendStatus() {
  try {
    await $fetch(`${apiBaseUrl.value}/`);
    backendStatus.value = 'connected';
  } catch (e) {
    backendStatus.value = 'disconnected';
  }
}

// Utility function to scroll to top
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(() => {
  console.log('🎬 Component mounted');
  
  // Load saved state from session
  loadFromSession();
  
  console.log('📊 Initial state:', {
    currentView: currentView.value,
    analysisResult: analysisResult.value,
    parsedData: parsedData.value
  });
  checkBackendStatus();
});

// Watchers to save state automatically
watch([currentView, parsedData, analysisResult, originalParsedData, jobMatches, editableData], 
  () => {
    saveToSession();
  },
  { deep: true }
);

// Add watcher for currentView
watch(currentView, (newView, oldView) => {
  // Only log if there was a previous value (avoid initial undefined)
  if (oldView !== undefined) {
    console.log(`🔄 View changed from '${oldView}' to '${newView}'`);
  }
}, { immediate: true });

// Add utility functions for structured data display
function getStructuredSectionCount(): number {
  if (!parsedData.value) return 0;
  
  // Check if we have structured data (new format)
  if (parsedData.value.contact_info || (parsedData.value.summary && typeof parsedData.value.summary === 'object')) {
    let count = 0;
    if (parsedData.value.contact_info) count++;
    if (parsedData.value.summary && (parsedData.value.summary.summary || parsedData.value.summary.full_text)) count++;
    if (parsedData.value.experience && (parsedData.value.experience.summary || parsedData.value.experience.full_text)) count++;
    if (parsedData.value.education && (parsedData.value.education.summary || parsedData.value.education.full_text)) count++;
    if (parsedData.value.skills && (parsedData.value.skills.summary || parsedData.value.skills.full_text)) count++;
    if (parsedData.value.projects && (parsedData.value.projects.summary || parsedData.value.projects.full_text)) count++;
    if (parsedData.value.certificates && (parsedData.value.certificates.summary || parsedData.value.certificates.full_text)) count++;
    return count;
  }
  
  // Fallback to old flat structure
  return Object.keys(parsedData.value).filter(key => key !== 'full_text' && parsedData.value?.[key]).length;
}

function getStructuredExperienceWords(): number {
  if (!parsedData.value) return 0;
  
  // Check if we have structured experience data (new format)
  if (parsedData.value.experience && typeof parsedData.value.experience === 'object' && parsedData.value.experience.full_text) {
    return getWordCount(parsedData.value.experience.full_text);
  }
  
  // Fallback to old flat structure
  return getWordCount(parsedData.value?.experience || '');
}

// Add new utility functions for structured data
function extractSkillsFromStructured(skillsObj: any): string[] {
  if (!skillsObj || typeof skillsObj !== 'object') return [];
  
  // Handle new format with summary/full_text
  if (skillsObj.full_text) {
    return skillsObj.full_text
      .split(/[,\n•\-\*\|]/)
      .map((skill: string) => skill.trim())
      .filter((skill: string) => skill && skill.length > 1)
      .slice(0, 20);
  }
  
  if (skillsObj.summary) {
    return skillsObj.summary
      .split(/[,\n•\-\*\|]/)
      .map((skill: string) => skill.trim())
      .filter((skill: string) => skill && skill.length > 1)
      .slice(0, 20);
  }
  
  // Fallback for old array-based structure
  const allSkills: string[] = [];
  Object.values(skillsObj).forEach((category: any) => {
    if (Array.isArray(category)) {
      allSkills.push(...category);
    } else if (typeof category === 'string') {
      allSkills.push(...category.split(/[,\n•\-\*]/).map(s => s.trim()).filter(s => s));
    }
  });
  
  return allSkills.filter(skill => skill && skill.length > 1).slice(0, 20);
}

function extractExperienceYearsFromStructured(experienceData: any): number {
  if (!experienceData) return 0;
  
  // Handle new format with summary/full_text
  if (typeof experienceData === 'object' && (experienceData.full_text || experienceData.summary)) {
    const text = experienceData.full_text || experienceData.summary;
    const yearMatches = text.match(/(\d+)\s*(?:years?|yrs?)/gi);
    if (yearMatches) {
      const years = yearMatches.map((match: string) => parseInt(match.match(/\d+/)?.[0] || '0'));
      return Math.max(...years);
    }
    return 0;
  }
  
  // Fallback for old array structure
  if (Array.isArray(experienceData)) {
    const currentYear = new Date().getFullYear();
    let totalYears = 0;
    
    experienceData.forEach(exp => {
      if (exp.dates) {
        const yearMatches = exp.dates.match(/(\d{4})/g);
        if (yearMatches && yearMatches.length >= 1) {
          const startYear = parseInt(yearMatches[0]);
          const endYear = yearMatches.length > 1 && !exp.dates.toLowerCase().includes('present') 
            ? parseInt(yearMatches[yearMatches.length - 1]) 
            : currentYear;
          totalYears += Math.max(0, endYear - startYear);
        }
      }
    });
    
    return totalYears;
  }
  
  return 0;
}

function getStructuredPreviewSections() {
  if (!parsedData.value) return {};
  
  // Get the actual data (might be nested under parsed_data)
  const actualData = parsedData.value.parsed_data || parsedData.value;
  const sections: Record<string, any> = {};
  
  // Contact Information
  if (actualData.contact_info) {
    const contact = actualData.contact_info;
    sections.contact_information = `${contact.name || ''}\n${contact.email || ''}\n${contact.phone || ''}\n${contact.location || ''}`.trim();
  }
  
  // Summary
  if (actualData.summary) {
    sections.summary = actualData.summary.summary || actualData.summary.full_text || '';
  }
  
  // Experience
  if (actualData.experience) {
    sections.experience = actualData.experience.summary || actualData.experience.full_text || '';
  }
  
  // Education
  if (actualData.education) {
    sections.education = actualData.education.summary || actualData.education.full_text || '';
  }
  
  // Skills
  if (actualData.skills) {
    sections.skills = actualData.skills.summary || actualData.skills.full_text || '';
  }
  
  // Projects
  if (actualData.projects) {
    sections.projects = actualData.projects.summary || actualData.projects.full_text || '';
  }
  
  // Certificates
  if (actualData.certificates) {
    sections.certificates = actualData.certificates.summary || actualData.certificates.full_text || '';
  }
  
  // Filter out empty sections
  return Object.fromEntries(
    Object.entries(sections).filter(([key, content]) => {
      return content && String(content).trim().length > 0;
    })
  );
}

function getPreviewSections() {
  if (!parsedData.value) return {};
  
  // Get the actual data (might be nested under parsed_data)
  const actualData = parsedData.value.parsed_data || parsedData.value;
  
  console.log('🔍 getPreviewSections - actualData:', actualData);
  
  // Check if we have the new structured format
  if (hasStructuredData.value) {
    return getStructuredPreviewSections();
  }
  
  // Fallback to old flat structure
  const sections = { ...actualData };
  delete sections.full_text;
  
  // Return only non-empty sections and ensure we have the latest data
  const filteredSections = Object.fromEntries(
    Object.entries(sections).filter(([key, content]) => {
      const currentContent = editableData.value[key] || content;
      return currentContent && String(currentContent).trim();
    })
  );
  
  return filteredSections;
}

function getWordCount(text: string): number {
  return text ? text.trim().split(/\s+/).length : 0;
}

function getSkillCount(text: string | object): number {
  // Handle structured skills object (new format)
  if (typeof text === 'object' && text !== null) {
    if ((text as any).full_text) {
      const skills = (text as any).full_text.split(/[,\n•\-\*\|]/).filter((skill: string) => skill.trim().length > 0);
      return skills.length;
    }
    if ((text as any).summary) {
      const skills = (text as any).summary.split(/[,\n•\-\*\|]/).filter((skill: string) => skill.trim().length > 0);
      return skills.length;
    }
    
    // Fallback for old structure
    let count = 0;
    Object.values(text).forEach((category: any) => {
      if (Array.isArray(category)) {
        count += category.length;
      } else if (typeof category === 'object' && category !== null) {
        count += Object.keys(category).length; // For language skills
      }
    });
    return count;
  }
  
  // Handle flat text skills
  if (!text || typeof text !== 'string') return 0;
  const skills = text.split(/[,\n•]/).filter(skill => skill.trim().length > 0);
  return skills.length;
}

function getEducationLevel(education: string | any[] | object): string {
  // Handle structured education object (new format)
  if (typeof education === 'object' && education !== null && !Array.isArray(education)) {
    const text = (education as any).full_text || (education as any).summary || '';
    if (text) {
      const lower = text.toLowerCase();
      if (lower.includes('phd') || lower.includes('doctorate')) return 'Doctorate';
      if (lower.includes('master') || lower.includes('mba')) return 'Master\'s';
      if (lower.includes('bachelor') || lower.includes('degree')) return 'Bachelor\'s';
      if (lower.includes('associate')) return 'Associate';
      if (lower.includes('diploma')) return 'Diploma';
      return 'Degree';
    }
  }
  
  // Handle structured education array (old format)
  if (Array.isArray(education)) {
    const degrees = education.map(edu => edu.degree || '').join(' ').toLowerCase();
    if (degrees.includes('phd') || degrees.includes('doctorate')) return 'Doctorate';
    if (degrees.includes('master') || degrees.includes('mba')) return 'Master\'s';
    if (degrees.includes('bachelor') || degrees.includes('degree')) return 'Bachelor\'s';
    if (degrees.includes('associate')) return 'Associate';
    if (degrees.includes('diploma')) return 'Diploma';
    return education.length > 0 ? 'Multiple Degrees' : 'Not specified';
  }
  
  // Handle flat text education
  if (!education || typeof education !== 'string') return 'Not specified';
  const lower = education.toLowerCase();
  if (lower.includes('phd') || lower.includes('doctorate')) return 'Doctorate';
  if (lower.includes('master') || lower.includes('mba')) return 'Master\'s';
  if (lower.includes('bachelor') || lower.includes('degree')) return 'Bachelor\'s';
  if (lower.includes('associate')) return 'Associate';
  return 'Other';
}

function extractSkills(skillsData: string | object): string[] {
  // Handle structured skills object
  if (typeof skillsData === 'object' && skillsData !== null) {
    return extractSkillsFromStructured(skillsData);
  }
  
  // Handle flat text skills
  if (!skillsData || typeof skillsData !== 'string') return [];
  return skillsData.split(/[,\n•\-\*]/)
    .map(skill => skill.trim())
    .filter(skill => skill && skill.length > 1)
    .slice(0, 20); // Limit to top 20 skills
}

function extractExperienceYears(experienceData: string | any[] | object): number {
  // Handle structured experience object or array
  if (typeof experienceData === 'object' && experienceData !== null) {
    return extractExperienceYearsFromStructured(experienceData);
  }
  
  // Handle flat text experience
  if (!experienceData || typeof experienceData !== 'string') return 0;
  // Simple heuristic to extract years of experience
  const yearMatches = experienceData.match(/(\d+)\s*(?:years?|yrs?)/gi);
  if (yearMatches) {
    const years = yearMatches.map(match => parseInt(match.match(/\d+/)?.[0] || '0'));
    return Math.max(...years);
  }
  return 0;
}

// ... existing code ...

// Handle updates from StructuredResumeDisplay component
function handleStructuredDataUpdate(updatedData: Record<string, any>) {
  console.log('📝 Handling structured data update:', updatedData);
  
  if (parsedData.value) {
    // Update the parsedData with the new values
    Object.keys(updatedData).forEach(key => {
      if (parsedData.value) {
        parsedData.value[key] = updatedData[key];
      }
    });
    
    // Also update editableData for consistency
    editableData.value = { ...editableData.value, ...updatedData };
  }
}
</script>

<style scoped>
/* Smooth transitions */
* {
  transition: all 0.2s ease-in-out;
}

/* Vue Transition Animations */
.slide-down-enter-active {
  transition: all 0.3s ease-out;
}

.slide-down-leave-active {
  transition: all 0.3s ease-in;
}

.slide-down-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-down-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.fade-in {
  animation: fadeIn 0.6s ease-out;
}

.slide-up {
  animation: slideUp 0.6s ease-out;
}

.animate-bounce-subtle {
  animation: bounce-subtle 2s infinite;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce-subtle {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-3px);
  }
  60% {
    transform: translateY(-2px);
  }
}

/* Animation for progress bar */
@keyframes slideIn {
  from {
    width: 0%;
  }
  to {
    width: var(--target-width);
  }
}
</style>